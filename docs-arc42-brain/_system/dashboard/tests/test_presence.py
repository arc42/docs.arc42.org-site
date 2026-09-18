from presence import Presence, nickname


class Clock:
    def __init__(self): self.t = 1000.0
    def __call__(self): return self.t


def test_first_live_tab_is_facilitator_and_role_passes_on():
    c = Clock(); p = Presence(clock=c)
    assert p.ping("a")["is_facilitator"] is True
    c.t += 1; assert p.ping("b")["is_facilitator"] is False
    assert p.live() == ["a", "b"]
    c.t += 60; p.ping("b")            # a silent for 61 s: still live (limit 90 s)
    assert p.facilitator() == "a"
    c.t += 40; p.ping("b")            # a silent for 101 s: gone
    assert p.live() == ["b"] and p.facilitator() == "b"


def test_leaving_then_ping_keeps_first_seen_navigation():
    c = Clock(); p = Presence(clock=c)
    p.ping("a"); c.t += 1; p.ping("b")
    p.leaving("a"); c.t += 2; p.ping("a")   # next page of the same tab
    assert p.facilitator() == "a"


def test_leaving_without_return_drops_after_grace():
    c = Clock(); p = Presence(clock=c)
    p.ping("a"); c.t += 1; p.ping("b")
    p.leaving("a"); c.t += 6
    assert p.live() == ["b"] and p.is_facilitator("b")


def test_count_and_who():
    c = Clock(); p = Presence(clock=c)
    p.ping("a"); c.t += 5
    r = p.ping("b")
    assert r["count"] == 2 and r["nickname"] == nickname("b")
    who = p.who()
    assert [w["is_facilitator"] for w in who] == [True, False]
    assert who[0]["connected_seconds"] == 5


def test_nickname_is_stable_and_two_words():
    assert nickname("x1") == nickname("x1") and len(nickname("x1").split()) == 2


def test_routes(client):
    r = client.post("/ping", json={"client_id": "tab-1"})
    assert r.get_json()["is_facilitator"] is True
    assert client.post("/leaving", json={"client_id": "tab-1"}).status_code == 204
    assert "connected" in client.get("/who").get_data(as_text=True)
