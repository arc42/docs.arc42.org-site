"""Small vaults for the emitter, generator and parity tests.

Every page is written with the importer's write_page, so it looks exactly like
an imported page. Defaults describe a published section 9 with one callout, an
examples directive and the examples-link directive.
"""
from __future__ import annotations

from pathlib import Path

from braingen.importer import write_page

DAY = "2026-09-18"
SOURCE = "[[SRC-001-test]]"
SECTION_BODY = (
    "# 9. Architecture Decisions\n\n"
    "> [!arc42-help]\n"
    "> ## Background (on ADRs)\n"
    "> Text.\n"
    ">\n"
    "> %% examples: decisions %%\n"
    ">\n\n"
    "%% examples-link %%\n\n"
    "_&lt;describe here >_\n"
)


def _common(id_: str, type_: str, title: str, status: str) -> dict:
    return {"id": id_, "type": type_, "title": title, "status": status, "created": DAY,
            "updated": DAY, "sources": [SOURCE], "related": []}


def source(root: Path) -> None:
    meta = {"id": "SRC-001", "type": "source", "title": "Test source", "status": "ingested",
            "created": DAY, "updated": DAY, "origin": "raw/test/", "files": []}
    write_page(root / "raw/sources/SRC-001-test.md", meta, "Test.\n")


def section(root: Path, n: int = 9, body: str = SECTION_BODY, status: str = "published", **extra) -> None:
    meta = _common(f"section-{n}", "section", f"{n} - Architecture decisions", status)
    meta.update({"number": n, "name": "Architecture Decisions", "category": "decisions",
                 "posts-dir": f"{n:02d}-decisions", "permalink": f"/section-{n}/", "order": n + 4,
                 "faq-topic": "fundamental architecture and design decisions"})
    meta.update(extra)
    write_page(root / "wiki/sections" / f"section-{n}.md", meta, body)


def tip(root: Path, id_: str = "9-1", body: str = "Some tip.\n", status: str = "published", **extra) -> None:
    meta = _common(id_, "tip", f"Tip {id_}: Do it!", status)
    meta.update({"section": "[[section-9]]", "keywords": [], "terms": [], "legacy-tags": [],
                 "date": "2016-03-01", "permalink": f"/tips/{id_}/"})
    meta.update(extra)
    write_page(root / "wiki/tips" / f"tip-{id_}.md", meta, body)


def example(root: Path, id_: str = "09-decision-example-x", body: str = "An example.\n",
            status: str = "published", **extra) -> None:
    meta = _common(id_, "example", "Example Decision: X", status)
    meta.update({"section": "[[section-9]]", "system": "", "example-category": "decisions",
                 "keywords": [], "terms": [], "legacy-tags": [], "permalink": "/examples/decision-x/"})
    meta.update(extra)
    write_page(root / "wiki/examples" / f"{id_}.md", meta, body)


def term(root: Path, slug: str, display: str, status: str = "review", legacy=(), aliases=()) -> None:
    meta = _common(slug, "term", display, status)
    meta.update({"term": display, "aliases": list(aliases), "legacy-tags": list(legacy), "home": "[[section-9]]"})
    write_page(root / "wiki/terms" / f"{slug}.md", meta, "A definition.\n")


def keyword(root: Path, slug: str, status: str = "draft") -> None:
    meta = _common(slug, "keyword", slug, status)
    meta.update({"description": "A facet.", "featured": False})
    write_page(root / "wiki/keywords" / f"{slug}.md", meta, "")


def system(root: Path, slug: str, name: str, url: str = "") -> None:
    meta = _common(slug, "system", name, "draft")
    meta.update({"name": name, "url": url})
    write_page(root / "wiki/systems" / f"{slug}.md", meta, "A system.\n")


def asset(root: Path, rel: str, data: bytes = b"\x89PNG test") -> None:
    """rel is below wiki/assets/, e.g. "sections/09/d.png"."""
    p = root / "wiki/assets" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
