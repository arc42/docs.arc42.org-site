"""Presence tracking for the docs-arc42-brain dashboard: who currently has
the dashboard open, and who among them is the facilitator (whichever tab
connected first and is still around). Ported from eTSU's
`_system/apps/dashboard/app.py` (`_facilitator_client_id`, `/ping`,
`/leaving`, `_nickname`) — see that file's ADR-0022 for the design
rationale. Nothing here is persisted: a server restart clears all presence.
"""
from __future__ import annotations

import threading
import time
import zlib

_NICKNAME_ADJECTIVES = ["Curious", "Swift", "Quiet", "Bold", "Sunny", "Clever",
                         "Gentle", "Brisk", "Merry", "Wandering", "Sharp", "Calm"]
_NICKNAME_ANIMALS = ["Otter", "Falcon", "Fox", "Heron", "Lynx", "Puffin",
                      "Badger", "Wren", "Marten", "Ibex", "Hare", "Tern"]


def nickname(cid: str) -> str:
    """A stable, fun, non-identifying label for a client_id: deterministic
    (the same tab always gets the same nickname across polls) but derived
    from nothing more than the random id the tab already generated itself,
    so there's no real identity behind it."""
    h = zlib.crc32(cid.encode("utf-8"))
    adjective = _NICKNAME_ADJECTIVES[h % len(_NICKNAME_ADJECTIVES)]
    animal = _NICKNAME_ANIMALS[(h // len(_NICKNAME_ADJECTIVES)) % len(_NICKNAME_ANIMALS)]
    return f"{adjective} {animal}"


def client_id(request) -> str:
    """The per-tab id a page sends with /ping and /leaving (kept in
    sessionStorage by static/app.js, so it survives in-tab navigation but
    not a closed tab). Defaulted and length-capped so a missing or
    malformed body can't wedge the presence dicts."""
    try:
        data = request.get_json(silent=True, force=True) or {}
    except Exception:
        data = {}
    cid = str(data.get("client_id") or "").strip()[:64]
    return cid or "anon"


class Presence:
    """In-memory presence: which client_ids have pinged recently, and which
    of them is the facilitator (the live cid with the smallest first-seen
    time). State is three dicts — `_last`, `_first`, `_leaving` — all keyed
    by client_id and guarded by one lock. Eviction runs at the start of
    every public call, so a caller never sees a stale entry."""

    def __init__(self, clock=time.monotonic, live_after: float = 90.0,
                 leave_grace: float = 5.0):
        self._clock = clock
        self._live_after = live_after
        self._leave_grace = leave_grace
        self._lock = threading.Lock()
        self._last: dict[str, float] = {}
        self._first: dict[str, float] = {}
        self._leaving: dict[str, float] = {}

    def _forget(self, cid: str) -> None:
        self._last.pop(cid, None)
        self._first.pop(cid, None)
        self._leaving.pop(cid, None)

    def _evict(self, now: float) -> None:
        """Drop a cid that has gone silent past `live_after`, or that said
        goodbye (`/leaving`) more than `leave_grace` ago without a fresher
        ping cancelling it. Call under the lock."""
        for cid in list(self._last):
            if now - self._last[cid] > self._live_after:
                self._forget(cid)
                continue
            left_at = self._leaving.get(cid)
            if left_at is not None and now - left_at > self._leave_grace:
                self._forget(cid)

    def _facilitator_locked(self) -> str | None:
        """The earliest-seen live client_id, excluding "anon" — the
        fallback id `presence.client_id()` hands out for a missing or
        malformed body. A cross-origin caller that can't set a real
        client_id (e.g. a `text/plain` no-cors POST with no readable
        response) must never be able to win the facilitator role by
        showing up as "anon"."""
        candidates = {cid: t for cid, t in self._first.items() if cid != "anon"}
        if not candidates:
            return None
        return min(candidates, key=candidates.get)

    def ping(self, cid: str) -> dict:
        with self._lock:
            now = self._clock()
            self._evict(now)
            if cid not in self._first:
                self._first[cid] = now
            self._last[cid] = now
            self._leaving.pop(cid, None)
            is_facilitator = cid == self._facilitator_locked()
            count = len(self._last)
        return {"nickname": nickname(cid), "is_facilitator": is_facilitator, "count": count}

    def leaving(self, cid: str) -> None:
        with self._lock:
            now = self._clock()
            self._evict(now)
            if cid in self._last:   # a goodbye from a tab that never pinged has nothing to end
                self._leaving[cid] = now

    def live(self) -> list[str]:
        with self._lock:
            now = self._clock()
            self._evict(now)
            return sorted(self._first, key=self._first.get)

    def facilitator(self) -> str | None:
        with self._lock:
            now = self._clock()
            self._evict(now)
            return self._facilitator_locked()

    def is_facilitator(self, cid: str) -> bool:
        return cid == self.facilitator()

    def who(self) -> list[dict]:
        with self._lock:
            now = self._clock()
            self._evict(now)
            fac = self._facilitator_locked()
            cids = sorted(self._first, key=self._first.get)
            return [
                {
                    "nickname": nickname(cid),
                    "is_facilitator": cid == fac,
                    "connected_seconds": int(now - self._first[cid]),
                }
                for cid in cids
            ]
