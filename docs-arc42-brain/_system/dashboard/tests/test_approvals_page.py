"""/approvals: the ADR-0006 register as a page — read the diff, then approve.

The braingen calls are stubbed. What is tested here is the dashboard's own
contract: unapproved entries come first, the write is facilitator-gated and
JSON-only, and a missing field is refused before anything is recorded.
"""
import json

import pytest

from actions import Approvals, approvals_view

PENDING = [
    {"rel": "_pages/section-9.md", "fingerprint": "abc", "diff": "--- as ingested\n+new line",
     "approved": {"issue": "ISS-002", "date": "2026-09-23", "reason": "date row"}},
    {"rel": "_posts/06-runtime/2016-03-01-t-6-6.md", "fingerprint": "def",
     "diff": "--- as ingested\n+corrected", "approved": None},
]


class FakeProc:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode, self.stdout, self.stderr = returncode, stdout, stderr


@pytest.fixture
def approvals(repo, monkeypatch):
    a = Approvals(repo)
    calls = []

    def fake_run(argv):
        calls.append(argv)
        if "pending-edits" in argv:
            return FakeProc(stdout=json.dumps(PENDING))
        return FakeProc(stdout="recorded in _system/approved-body-edits.tsv")

    monkeypatch.setattr(a, "_run", fake_run)
    a.calls = calls
    return a


def test_unapproved_entries_come_first(approvals):
    view = approvals_view(approvals)
    assert [i["rel"] for i in view["items"]][0].endswith("t-6-6.md")
    assert view["waiting"] == 1


def test_a_broken_braingen_call_is_an_empty_list_not_a_crash(repo, monkeypatch):
    a = Approvals(repo)
    monkeypatch.setattr(a, "_run", lambda argv: FakeProc(returncode=2, stderr="boom"))
    assert a.pending() == []
    monkeypatch.setattr(a, "_run", lambda argv: FakeProc(stdout="not json"))
    assert a.pending() == []


def test_approve_passes_the_reason_through_as_one_argument(approvals):
    ok, _ = approvals.approve("_pages/section-9.md", "ISS-002", "a reason with spaces")
    assert ok
    argv = approvals.calls[-1]
    assert "--yes" in argv
    assert argv[argv.index("--reason") + 1] == "a reason with spaces"


def test_the_page_renders_and_links_from_actions(client):
    assert client.get("/approvals").status_code == 200
    assert 'href="/approvals"' in client.get("/actions").get_data(as_text=True)


def test_approving_needs_json(client):
    r = client.post("/approvals/approve", data="rel=x")
    assert r.status_code == 415


def test_approving_needs_the_facilitator(client):
    """The facilitator is the earliest live tab, so "second" must be refused."""
    client.post("/ping", data=json.dumps({"client_id": "first"}), content_type="application/json")
    client.post("/ping", data=json.dumps({"client_id": "second"}), content_type="application/json")
    r = client.post("/approvals/approve", content_type="application/json",
                    data=json.dumps({"client_id": "second", "rel": "_pages/section-9.md",
                                     "issue": "ISS-002", "reason": "why"}))
    assert r.status_code == 403


def test_the_page_sends_the_client_id_so_the_facilitator_is_recognised(client):
    """Regression: without client_id in the body presence sees "anon" and the
    facilitator's own click is refused."""
    html = client.get("/approvals").get_data(as_text=True)
    assert "client_id: window.brainClientId" in html


def test_a_missing_field_is_refused(client):
    client.post("/ping", data=json.dumps({"client_id": "only"}), content_type="application/json")
    r = client.post("/approvals/approve", content_type="application/json",
                    data=json.dumps({"client_id": "only", "rel": "_pages/section-9.md",
                                     "issue": "ISS-002", "reason": "   "}))
    assert r.status_code == 400
    assert "required" in r.get_json()["error"]
