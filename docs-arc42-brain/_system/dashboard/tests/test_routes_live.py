import pytest

from app import create_app
from actions import Job


class StubRunner:
    def __init__(self): self.current = None; self.last = None; self.started = []; self.on_finish = None
    def start(self, kind):
        self.started.append(kind); job = Job(kind, "t"); return job, True
    def parity(self): return {"9": "PASS"}


@pytest.fixture
def app_(repo):
    return create_app(repo, runner=StubRunner())


def test_generate_needs_facilitator(app_):
    c1, c2 = app_.test_client(), app_.test_client()
    c1.post("/ping", json={"client_id": "first"})
    c2.post("/ping", json={"client_id": "second"})
    r = c2.post("/actions/generate", json={"client_id": "second"})
    assert r.status_code == 403 and "facilitator" in r.get_json()["error"]
    r = c1.post("/actions/generate", json={"client_id": "first"})
    assert r.status_code == 202 and r.get_json()["started"] is True
    assert app_.extensions["brain"]["runner"].started == ["generate"]


def test_preview_and_job_status(app_):
    c = app_.test_client()
    c.post("/ping", json={"client_id": "f"})
    assert c.post("/actions/preview", json={"client_id": "f"}).status_code == 202
    assert c.get("/actions/job").get_json() == {"current": None, "last": None}


@pytest.mark.parametrize("path", ["/actions", "/links", "/suggestions", "/graph", "/graph?kind=terms",
                                  "/search?q=adr"])
def test_pages(app_, path):
    assert app_.test_client().get(path).status_code == 200


def test_graph_json_and_search(app_):
    c = app_.test_client()
    assert c.get("/graph.json?kind=terms").get_json()["edges"][0]["weight"] == 1
    assert "tip-9-1" in c.get("/search?q=adr.github").get_data(as_text=True)


def test_reload_and_linkcheck(app_, monkeypatch):
    c = app_.test_client()
    assert c.post("/reload").status_code in (302, 303)
    lc = app_.extensions["brain"]["linkchecker"]
    monkeypatch.setattr(lc, "start", lambda urls: True)
    assert c.post("/actions/linkcheck", json={}).get_json() == {"started": True}


def test_no_cdn_anywhere(app_):
    c = app_.test_client()
    for path in ["/", "/graph", "/actions"]:
        html = c.get(path).get_data(as_text=True)
        assert "https://" not in "".join(l for l in html.splitlines() if "<script" in l or "<link" in l)
