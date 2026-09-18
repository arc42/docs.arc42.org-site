"""External link checking: URLs found in the vault, a single HEAD probe, and
a `LinkChecker` that caches results for a day and can run in the background.

Reads the model only through `model.Brain` (D21); writes only its own cache
file, whose path is chosen by the caller (dashboard build output, D18).
"""
from __future__ import annotations

import json
import os
import tempfile
import threading
import time
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re

from model import Brain

URL_RE = re.compile(r"https?://[^\s)<>\]\"'`|…]+")  # "…" (ellipsis) is a terminator, never part of a URL

_USER_AGENT = "docs-arc42-brain-linkcheck"
_RETRY_CODES = (403, 405)
_WORKERS = 8


def _walk_strings(value):
    """Yield every string found in `value`, recursing through dicts and
    lists/tuples (meta values can nest, e.g. a source's `files` list)."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _walk_strings(v)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _walk_strings(item)


def external_urls(b: Brain) -> dict[str, list[str]]:
    """url (trailing `.,;:` stripped) -> sorted slugs of pages naming it,
    from page bodies and any string meta value (walked recursively)."""
    found: dict[str, set[str]] = defaultdict(set)
    for page in b.vault.pages.values():
        texts = [page.body, *_walk_strings(page.meta)]
        for text in texts:
            for m in URL_RE.finditer(text):
                url = m.group(0).rstrip(".,;:")
                found[url].add(page.slug)
    return {url: sorted(slugs) for url, slugs in found.items()}


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Refuses every redirect, so a 3xx response surfaces as an HTTPError
    (status + Location header) instead of being followed."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D102
        return None


def _opener() -> urllib.request.OpenerDirector:
    return urllib.request.build_opener(_NoRedirectHandler)


def _fetch_once(url: str, method: str, timeout: float) -> tuple[int, str | None]:
    req = urllib.request.Request(url, method=method, headers={"User-Agent": _USER_AGENT})
    resp = _opener().open(req, timeout=timeout)
    try:
        return resp.status, resp.headers.get("Location")
    finally:
        resp.close()


def head_status(url: str, timeout: float = 10.0) -> dict:
    """{"status", "location", "error"}. HEAD via `urllib.request`, redirects
    not followed (a 3xx comes back as its status and Location). A 403/405
    is retried once with GET."""
    try:
        status, location = _fetch_once(url, "HEAD", timeout)
        return {"status": status, "location": location, "error": None}
    except urllib.error.HTTPError as e:
        if e.code in _RETRY_CODES:
            try:
                status, location = _fetch_once(url, "GET", timeout)
                return {"status": status, "location": location, "error": None}
            except urllib.error.HTTPError as e2:
                location = e2.headers.get("Location") if e2.headers else None
                return {"status": e2.code, "location": location, "error": None}
            except Exception as e2:  # noqa: BLE001 - report as a failed check, don't raise
                return {"status": None, "location": None, "error": str(e2)}
        location = e.headers.get("Location") if e.headers else None
        return {"status": e.code, "location": location, "error": None}
    except Exception as e:  # noqa: BLE001 - report as a failed check, don't raise
        return {"status": None, "location": None, "error": str(e)}


def link_summary(rows: list[dict]) -> dict | None:
    """{"failures", "redirects", "ok"} counts over `results()`/`check()`
    rows, or None when there are no rows (the checker hasn't run yet)."""
    if not rows:
        return None
    failures = sum(1 for r in rows if r["status"] is None or r["status"] >= 400)
    redirects = sum(1 for r in rows if r["status"] is not None and 300 <= r["status"] < 400)
    return {"failures": failures, "redirects": redirects, "ok": len(rows) - failures - redirects}


def _group(status: int | None) -> int:
    """Sort group: 0 failures (None or >=400), 1 redirects (3xx), 2 the rest."""
    if status is None or status >= 400:
        return 0
    if 300 <= status < 400:
        return 1
    return 2


class LinkChecker:
    """Checks external URLs with a 1-day-cached HEAD probe (`fetch`), either
    synchronously (`check`) or in a background thread (`start`)."""

    def __init__(self, cache_file: Path, fetch=head_status, clock=time.time, ttl: float = 86400.0):
        self.cache_file = Path(cache_file)
        self.fetch = fetch
        self.clock = clock
        self.ttl = ttl
        self.running = False
        self._start_lock = threading.Lock()
        # url -> sorted pages, from the most recent check() (this process only).
        self._pages: dict[str, list[str]] = {}

    def _load_cache(self) -> dict:
        if not self.cache_file.is_file():
            return {}
        try:
            return json.loads(self.cache_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

    def _write_cache(self, cache: dict) -> None:
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(
            dir=self.cache_file.parent, prefix=f".{self.cache_file.name}.", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(cache, f)
            os.replace(tmp_name, self.cache_file)
        except BaseException:
            try:
                os.remove(tmp_name)
            except OSError:
                pass
            raise

    @staticmethod
    def _sort(rows: list[dict]) -> list[dict]:
        return sorted(rows, key=lambda r: (_group(r["status"]), r["url"]))

    @staticmethod
    def _row(url: str, entry: dict, pages: list[str]) -> dict:
        """One result row from a cache entry (possibly {}) and its pages;
        shared by `check()` and `results()` so the shape is defined once."""
        return {
            "url": url,
            "status": entry.get("status"),
            "location": entry.get("location"),
            "error": entry.get("error"),
            "checked": entry.get("checked"),
            "pages": pages,
        }

    def check(self, urls: dict[str, list[str]]) -> list[dict]:
        """Synchronous: fetch what the cache doesn't have fresh, write the
        cache, and return the (sorted) rows for exactly `urls`."""
        now = self.clock()
        cache = self._load_cache()

        def is_stale(url: str) -> bool:
            entry = cache.get(url)
            return entry is None or now - entry.get("checked", 0.0) >= self.ttl

        stale = [url for url in urls if is_stale(url)]
        if stale:
            with ThreadPoolExecutor(max_workers=_WORKERS) as ex:
                fetched = dict(zip(stale, ex.map(self.fetch, stale)))
            for url, result in fetched.items():
                cache[url] = {
                    "status": result["status"],
                    "location": result["location"],
                    "error": result["error"],
                    "checked": now,
                }
            self._write_cache(cache)

        self._pages = {url: sorted(pages) for url, pages in urls.items()}
        rows = [self._row(url, cache.get(url, {}), self._pages[url]) for url in urls]
        return self._sort(rows)

    def start(self, urls: dict[str, list[str]]) -> bool:
        """Run `check(urls)` in a background thread. False (does nothing)
        when a check is already running."""
        with self._start_lock:
            if self.running:
                return False
            self.running = True

        def body() -> None:
            try:
                self.check(urls)
            finally:
                self.running = False

        threading.Thread(target=body, daemon=True).start()
        return True

    def results(self) -> list[dict]:
        """The cache file's rows, sorted; `pages` from the most recent
        `check()` in this process, or [] for a url only known from disk."""
        cache = self._load_cache()
        rows = [self._row(url, entry, self._pages.get(url, [])) for url, entry in cache.items()]
        return self._sort(rows)
