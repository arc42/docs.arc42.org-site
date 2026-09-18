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


# -- cross-origin guard (final-review Important #1) --------------------------


def test_cross_origin_post_is_rejected(app_):
    c = app_.test_client()
    r = c.post("/ping", json={"client_id": "x"}, headers={"Origin": "http://evil.example"})
    assert r.status_code == 403 and r.get_json()["error"] == "cross-origin request refused"


def test_matching_origin_is_allowed(app_):
    c = app_.test_client()
    r = c.post("/ping", json={"client_id": "x"}, headers={"Origin": "http://localhost"})
    assert r.status_code == 200


def test_cross_site_via_sec_fetch_site_is_rejected_without_origin(app_):
    c = app_.test_client()
    r = c.post("/ping", json={"client_id": "x"}, headers={"Sec-Fetch-Site": "cross-site"})
    assert r.status_code == 403


def test_same_site_via_sec_fetch_site_is_also_rejected(app_):
    # same-site (a sibling subdomain) is not same-origin: still refused.
    c = app_.test_client()
    r = c.post("/ping", json={"client_id": "x"}, headers={"Sec-Fetch-Site": "same-site"})
    assert r.status_code == 403


def test_same_origin_via_sec_fetch_site_is_allowed_without_origin(app_):
    c = app_.test_client()
    r = c.post("/ping", json={"client_id": "x"}, headers={"Sec-Fetch-Site": "same-origin"})
    assert r.status_code == 200


def test_no_origin_and_no_sec_fetch_site_is_allowed(app_):
    # curl, server-to-server calls, and (as it happens) most test clients.
    c = app_.test_client()
    assert c.post("/ping", json={"client_id": "x"}).status_code == 200


def test_reload_rejects_cross_origin(app_):
    c = app_.test_client()
    r = c.post("/reload", headers={"Origin": "http://evil.example"})
    assert r.status_code == 403


def test_reload_form_post_from_the_nav_still_works(app_):
    # A plain <form method=post> submit: no JSON body, but same-origin.
    c = app_.test_client()
    r = c.post("/reload", headers={"Origin": "http://localhost"})
    assert r.status_code in (302, 303)


def test_leaving_sendbeacon_json_blob_still_works(app_):
    # sendBeacon posts a JSON Blob same-origin: no explicit headers beyond
    # what the browser sets, which the test client mirrors here.
    c = app_.test_client()
    r = c.post("/leaving", data='{"client_id": "x"}', content_type="application/json")
    assert r.status_code == 204


# -- generate/preview: JSON body required (final-review Important #1) -------


def test_generate_requires_json_body(app_):
    c1 = app_.test_client()
    c1.post("/ping", json={"client_id": "first"})
    r = c1.post("/actions/generate", data="client_id=first", content_type="text/plain")
    assert r.status_code == 415


def test_preview_requires_json_body(app_):
    c1 = app_.test_client()
    c1.post("/ping", json={"client_id": "first"})
    r = c1.post("/actions/preview", data="client_id=first", content_type="text/plain")
    assert r.status_code == 415


# -- "anon" can never be facilitator (final-review Important #1) ------------


def test_anon_fallback_client_id_is_never_facilitator(app_):
    c = app_.test_client()
    # No client_id in the body at all -> presence.client_id() falls back to "anon".
    r = c.post("/ping", json={})
    assert r.get_json()["is_facilitator"] is False
    r2 = c.post("/actions/generate", json={})
    assert r2.status_code == 403


# -- Runner.start race: a None job must not crash the route -----------------


class NoneJobRunner(StubRunner):
    def start(self, kind):
        self.started.append(kind)
        return None, False


def test_generate_returns_202_not_500_when_runner_reports_none(repo):
    app_ = create_app(repo, runner=NoneJobRunner())
    c = app_.test_client()
    c.post("/ping", json={"client_id": "f"})
    r = c.post("/actions/generate", json={"client_id": "f"})
    assert r.status_code == 202
    assert r.get_json() == {"started": False, "job": None}
