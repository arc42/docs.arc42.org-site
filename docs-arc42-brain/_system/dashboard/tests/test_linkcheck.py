import json
import time
import urllib.error
from dataclasses import dataclass, field

import pytest

import linkcheck
from linkcheck import LinkChecker, external_urls, head_status, link_summary
from model import Model


# -- external_urls -----------------------------------------------------------


def test_external_urls(repo):
    assert external_urls(Model(repo).get()) == {"https://adr.github.io/": ["tip-9-1"]}


@dataclass
class FakePage:
    slug: str
    body: str = ""
    meta: dict = field(default_factory=dict)


@dataclass
class FakeVault:
    pages: dict


@dataclass
class FakeBrain:
    vault: FakeVault


def test_external_urls_walks_nested_meta_and_strips_trailing_punctuation():
    pages = {
        "a": FakePage(
            "a",
            body="See https://example.com/a, and also (https://example.com/c).",
            meta={"sources": [{"path": "https://example.com/b."}, {"other": 1}], "n": 3},
        ),
        "b": FakePage("b", body="", meta={"related": ["https://example.com/a"]}),
    }
    b = FakeBrain(FakeVault(pages))
    assert external_urls(b) == {
        "https://example.com/a": ["a", "b"],
        "https://example.com/b": ["a"],
        "https://example.com/c": ["a"],
    }


# -- head_status ---------------------------------------------------------


class _FakeResponse:
    def __init__(self, status, headers=None):
        self.status = status
        self.headers = headers or {}
        self.closed = False

    def close(self):
        self.closed = True


class _FakeOpener:
    def __init__(self, plan):
        # plan: list of callables(req) -> _FakeResponse, or raising an exception
        self.plan = list(plan)
        self.calls = []

    def open(self, req, timeout=None):
        self.calls.append((req.get_method(), req.full_url))
        step = self.plan.pop(0)
        return step()


def test_head_status_ok(monkeypatch):
    opener = _FakeOpener([lambda: _FakeResponse(200, {"Location": None})])
    monkeypatch.setattr(linkcheck, "_opener", lambda: opener)
    result = head_status("https://ok")
    assert result == {"status": 200, "location": None, "error": None}
    assert opener.calls == [("HEAD", "https://ok")]


def test_head_status_redirect_not_followed(monkeypatch):
    def raise_redirect():
        raise urllib.error.HTTPError("https://moved", 301, "Moved", {"Location": "https://new"}, None)

    opener = _FakeOpener([raise_redirect])
    monkeypatch.setattr(linkcheck, "_opener", lambda: opener)
    result = head_status("https://moved")
    assert result == {"status": 301, "location": "https://new", "error": None}


def test_head_status_retries_405_with_get(monkeypatch):
    def raise_405():
        raise urllib.error.HTTPError("https://x", 405, "Method Not Allowed", {}, None)

    opener = _FakeOpener([raise_405, lambda: _FakeResponse(200, {})])
    monkeypatch.setattr(linkcheck, "_opener", lambda: opener)
    result = head_status("https://x")
    assert result == {"status": 200, "location": None, "error": None}
    assert opener.calls == [("HEAD", "https://x"), ("GET", "https://x")]


def test_head_status_network_error(monkeypatch):
    def raise_url_error():
        raise urllib.error.URLError("timed out")

    opener = _FakeOpener([raise_url_error])
    monkeypatch.setattr(linkcheck, "_opener", lambda: opener)
    result = head_status("https://dead")
    assert result["status"] is None and result["location"] is None
    assert "timed out" in result["error"]


# -- LinkChecker.check: cache use and sort order (from the brief) -----------


def test_check_uses_cache_and_sorts(tmp_path):
    t = [1000.0]
    seen = []

    def fetch(url):
        seen.append(url)
        return {"https://ok": {"status": 200, "location": None, "error": None},
                "https://moved": {"status": 301, "location": "https://new", "error": None},
                "https://dead": {"status": None, "location": None, "error": "timeout"}}[url]

    lc = LinkChecker(tmp_path / "links.json", fetch=fetch, clock=lambda: t[0])
    urls = {"https://ok": ["a"], "https://moved": ["b"], "https://dead": ["c"]}
    rows = lc.check(urls)
    assert [r["url"] for r in rows] == ["https://dead", "https://moved", "https://ok"]
    assert rows[0]["pages"] == ["c"]
    t[0] += 3600; seen.clear(); lc.check(urls)
    assert seen == []
    t[0] += 86400; lc.check(urls)
    assert sorted(seen) == ["https://dead", "https://moved", "https://ok"]


def test_check_writes_cache_file_atomically(tmp_path):
    cache_file = tmp_path / "nested" / "links.json"

    def fetch(url):
        return {"status": 200, "location": None, "error": None}

    lc = LinkChecker(cache_file, fetch=fetch, clock=lambda: 1000.0)
    lc.check({"https://ok": ["a"]})
    assert cache_file.is_file()
    data = json.loads(cache_file.read_text())
    assert data["https://ok"] == {"status": 200, "location": None, "error": None, "checked": 1000.0}
    # no leftover temp files
    assert list(cache_file.parent.glob(".*")) == []


def test_check_multiple_pages_for_one_url_sorted(tmp_path):
    def fetch(url):
        return {"status": 200, "location": None, "error": None}

    lc = LinkChecker(tmp_path / "links.json", fetch=fetch, clock=lambda: 1000.0)
    rows = lc.check({"https://ok": ["z", "a"]})
    assert rows[0]["pages"] == ["a", "z"]


# -- LinkChecker.results -----------------------------------------------------


def test_results_after_check_has_pages(tmp_path):
    def fetch(url):
        return {"status": 200, "location": None, "error": None}

    lc = LinkChecker(tmp_path / "links.json", fetch=fetch, clock=lambda: 1000.0)
    lc.check({"https://ok": ["a"]})
    assert lc.results() == [
        {"url": "https://ok", "status": 200, "location": None, "error": None,
         "checked": 1000.0, "pages": ["a"]}
    ]


def test_results_from_cache_file_only_has_empty_pages(tmp_path):
    cache_file = tmp_path / "links.json"
    cache_file.write_text(json.dumps({
        "https://ok": {"status": 200, "location": None, "error": None, "checked": 1000.0},
        "https://dead": {"status": None, "location": None, "error": "timeout", "checked": 900.0},
    }))
    lc = LinkChecker(cache_file, fetch=lambda url: None, clock=lambda: 2000.0)
    rows = lc.results()
    assert [r["url"] for r in rows] == ["https://dead", "https://ok"]
    assert rows[0]["pages"] == [] and rows[1]["pages"] == []


def test_results_empty_when_no_cache_file(tmp_path):
    lc = LinkChecker(tmp_path / "links.json", fetch=lambda url: None, clock=lambda: 2000.0)
    assert lc.results() == []


# -- LinkChecker.start --------------------------------------------------------


def test_start_runs_in_background_and_returns_true(tmp_path):
    def fetch(url):
        return {"status": 200, "location": None, "error": None}

    lc = LinkChecker(tmp_path / "links.json", fetch=fetch, clock=lambda: 1000.0)
    started = lc.start({"https://ok": ["a"]})
    assert started is True
    for _ in range(100):
        if not lc.running:
            break
        time.sleep(0.05)
    assert lc.running is False
    assert lc.results()[0]["url"] == "https://ok"


def test_start_returns_false_when_already_running(tmp_path):
    lc = LinkChecker(tmp_path / "links.json", fetch=lambda url: None, clock=lambda: 1000.0)
    lc.running = True
    assert lc.start({"https://ok": ["a"]}) is False


# -- link_summary --------------------------------------------------------


def test_link_summary_none_when_no_rows():
    assert link_summary([]) is None


def test_link_summary_counts_failures_redirects_and_ok():
    rows = [
        {"url": "https://dead", "status": None},
        {"url": "https://gone", "status": 404},
        {"url": "https://moved", "status": 301},
        {"url": "https://ok", "status": 200},
        {"url": "https://also-ok", "status": 204},
    ]
    assert link_summary(rows) == {"failures": 2, "redirects": 1, "ok": 2}
