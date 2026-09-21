"""Fixture repo for dashboard tests.

Builds a small, self-contained docs.arc42.org-site checkout with a
docs-arc42-brain vault inside it: enough pages, of enough types, to exercise
lint, parity and the dashboard views without depending on the real vault.

Every wiki/raw page is written with braingen's own `importer.write_page`, so
it is byte-for-byte what the real importer produces. Section 9's body is
copied verbatim from braingen's own `tests/vaultkit.SECTION_BODY` (not
imported — the two projects stay independent). `_system/workflows/ingest.md`
is a verbatim copy of the real workflow file, embedded below.

Lint of this fixture gives exactly 1 error (rule `example-category`, page
`09-decision-example-y`) and 2 warnings (rule `reciprocity`, pages `ISS-001`
and `ISS-002`); `tests/test_kit.py` pins this.
"""
from __future__ import annotations

from pathlib import Path

from braingen.importer import write_page

DAY = "2026-09-18"
SOURCE = "[[SRC-001-test]]"

# Copied verbatim from docs-arc42-brain/_system/generate/tests/vaultkit.SECTION_BODY.
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

SECTION_3_BODY = "# 3. Context and Scope\n\n## Business Context\n\nText.\n"

# Verbatim copy of docs-arc42-brain/_system/workflows/ingest.md.
INGEST_WORKFLOW = """# Workflow: Ingest

Turn one raw batch into typed, linked wiki pages. For the bootstrap of
existing site content this is audit-style: type, link, flag. Grilling is
reserved for new content and for the FAQ merge.

1. **Batch.** `make brain-raw SECTION=N WHAT=content` (the section page already
   exists from bootstrap; use `WHAT=all` only when it does not). Confirm the
   batch under `raw/section-N-content/`.
2. **Import.** `make brain-import BATCH=section-N-content`. Every tip and
   example now exists as a draft with `legacy-tags` filled and a `SRC` record.
3. **Read.** Read every imported page. Note near-duplicates, outdated
   statements, dead external links, statements that contradict a section page.
4. **Vocabulary.** For every entry in `legacy-tags` on every page: decide
   keyword or term. Existing page: reference it (`keywords: ["[[lean]]"]`,
   `terms: ["[[decision]]"]`). Missing: create it from the template with a
   real definition and `home`. Ambiguous or near-duplicate of an existing
   term: add it to that term's `legacy-tags`/`aliases` and reference the term;
   when unsure raise an issue. Empty `legacy-tags` when done.
5. **Links.** Fill `related:` on every page. Look for: tips of the same
   section that build on each other, the example that shows what the tip
   says, the subsection the tip elaborates (link by heading), the term the
   tip is about. Add the reverse link on tips, examples and terms; not on
   sections.
6. **Issues.** One `ISS-NNN` page per finding from step 3, `related:` to every
   affected page.
7. **Status.** Set `status: review` on every page whose `legacy-tags` is
   empty and whose `related` is filled.
8. **Bookkeeping.** Update `_system/index.md`; append to `_system/log.md`:
   `## [YYYY-MM-DD] ingest | section N content`, listing pages created,
   terms/keywords created, issues raised. Move the batch to `raw/ingested/`
   and update the `SRC` record's `origin:`.
9. **Gate.** `make brain-lint` must report zero errors. Warnings about
   reciprocity are allowed but should be deliberate.

Quality bar: a section's ingest that creates no term page and raises no
issue has almost certainly under-read the content.
"""

# Header and format comment of the real _system/log.md, verbatim.
LOG_HEADER = """# Log

Append-only. One entry per operation, prefix exact so it stays greppable:
`grep '^## \\[' _system/log.md | tail -5`.

<!-- Format:
## [YYYY-MM-DD] <bootstrap|ingest|audit|report|cutover|generate> | <subject>
- created: …
- updated: …
- issues: …
-->
"""

LOG_ENTRIES = [
    ("2026-09-10", "bootstrap", "one"),
    ("2026-09-11", "ingest", "two"),
    ("2026-09-12", "ingest", "three"),
    ("2026-09-13", "audit", "four"),
    ("2026-09-14", "cutover", "five"),
    ("2026-09-15", "generate", "six"),
]


def _common(id_: str, type_: str, title: str, status: str, created: str = DAY, updated: str = DAY) -> dict:
    return {
        "id": id_, "type": type_, "title": title, "status": status,
        "created": created, "updated": updated,
        "sources": [SOURCE], "related": [],
    }


def _section(root: Path, n: int, name: str, category: str, posts_dir: str, permalink: str,
             order: int, faq_topic: str, status: str, body: str) -> None:
    meta = _common(f"section-{n}", "section", f"{n} - {name}", status)
    meta.update({
        "number": n, "name": name, "category": category, "posts-dir": posts_dir,
        "permalink": permalink, "order": order, "faq-topic": faq_topic,
    })
    write_page(root / "wiki/sections" / f"section-{n}.md", meta, body)


def _tip(root: Path, id_: str, status: str, section: str, related: list[str],
          terms: list[str], keywords: list[str] | None = None,
          legacy_tags: list[str] | None = None, body: str = "Some tip.\n",
          updated: str | None = None, date: str = "2016-03-01") -> None:
    meta = _common(id_, "tip", f"Tip {id_}: Do it!", status, updated=updated or DAY)
    meta.update({
        "section": section,
        "keywords": keywords or [],
        "terms": terms,
        "legacy-tags": legacy_tags or [],
        "date": date,
        "permalink": f"/tips/{id_}/",
        "related": related,
    })
    write_page(root / "wiki/tips" / f"tip-{id_}.md", meta, body)


def _example(root: Path, id_: str, status: str, system: str, category: str,
             related: list[str], body: str = "An example.\n") -> None:
    meta = _common(id_, "example", f"Example {id_}", status)
    meta.update({
        "section": "[[section-9]]",
        "system": system,
        "example-category": category,
        "keywords": [],
        "terms": [],
        "legacy-tags": [],
        "permalink": f"/examples/{id_}/",
        "related": related,
    })
    write_page(root / "wiki/examples" / f"{id_}.md", meta, body)


def _term(root: Path, slug: str, display: str, status: str, legacy_tags: list[str],
          home: str, body: str, updated: str | None = None) -> None:
    meta = _common(slug, "term", display, status, updated=updated or DAY)
    meta.update({"term": display, "aliases": [], "legacy-tags": legacy_tags, "home": home})
    write_page(root / "wiki/terms" / f"{slug}.md", meta, body)


def _keyword(root: Path, slug: str, status: str = "draft") -> None:
    meta = _common(slug, "keyword", slug, status)
    meta.update({"description": "A facet.", "featured": False})
    write_page(root / "wiki/keywords" / f"{slug}.md", meta, "")


def _system_page(root: Path, slug: str, name: str, status: str = "draft") -> None:
    meta = _common(slug, "system", name, status)
    meta.update({"name": name})
    write_page(root / "wiki/systems" / f"{slug}.md", meta, "A system.\n")


def _issue(root: Path, id_: str, status: str, severity: str, kind: str, created: str,
           related: list[str]) -> None:
    meta = _common(id_, "issue", f"{kind.capitalize()} on {', '.join(t[2:-2] for t in related) or 'the vault'}",
                    status, created=created, updated=created)
    meta.update({"severity": severity, "kind": kind, "raised-by": "agent", "resolved": None,
                 "related": related})
    write_page(root / "wiki/issues" / f"{id_}.md", meta, f"An issue of kind {kind}.\n")


def _source(root: Path) -> None:
    meta = {"id": "SRC-001", "type": "source", "title": "Test source", "status": "ingested",
            "created": DAY, "updated": DAY, "sources": [], "related": [],
            "origin": "raw/test/", "files": []}
    write_page(root / "raw/sources/SRC-001-test.md", meta, "Test.\n")


def _log(vault: Path) -> None:
    lines = [LOG_HEADER, ""]
    for date, kind, subject in LOG_ENTRIES:
        lines.append(f"## [{date}] {kind} | {subject}")
        lines.append("- notes: x")
        lines.append("")
    (vault / "_system" / "log.md").parent.mkdir(parents=True, exist_ok=True)
    (vault / "_system" / "log.md").write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")


def _ingest_workflow(vault: Path) -> None:
    path = vault / "_system" / "workflows" / "ingest.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(INGEST_WORKFLOW, encoding="utf-8")


def _placeholder(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\ntitle: x\n---\n", encoding="utf-8")


def add_tip(root: Path, id_: str, section: str, status: str = "review",
            date: str = "2016-03-01") -> None:
    """Add one tip to an already-built fixture repo, for a section state
    `build_repo` does not set up (a partly or fully ingested one). The
    generated post is `_posts/<posts-dir>/<date>-t-<id>.md`, so `date` is
    what decides whether it matches a site file placed by `add_site_post`."""
    _tip(root / "docs-arc42-brain", id_, status, section, related=[], terms=[], date=date)


def add_site_post(root: Path, posts_dir: str, name: str) -> None:
    """A site post with no brain page behind it (makes a section partial)."""
    _placeholder(root / "_posts" / posts_dir / name)


def build_repo(root: Path) -> Path:
    """Build the fixture repo (a whole site checkout) under `root` and return it."""
    vault = root / "docs-arc42-brain"

    _source(vault)

    _section(vault, 9, "Architecture Decisions", "decisions", "09-decisions", "/section-9/",
              13, "fundamental architecture and design decisions", "published", SECTION_BODY)
    _section(vault, 3, "Context and Scope", "context", "03-context", "/section-3/",
              7, "context and scope of the system", "draft", SECTION_3_BODY)

    _tip(vault, "9-1", "published", "[[section-9#Background (on ADRs)]]",
          related=["[[09-decision-example-x]]"], terms=["[[adr]]"], keywords=["[[lean]]"],
          body="See https://adr.github.io/ and [[tip-9-2]] for more.\n")
    _tip(vault, "9-2", "draft", "[[section-9]]", related=[], terms=["[[adr]]"],
          legacy_tags=["criteria"])
    _tip(vault, "9-3", "review", "[[section-9]]", related=[], terms=["[[adr]]", "[[stakeholder]]"],
          updated="2026-09-05")

    _example(vault, "09-decision-example-x", "published", "[[htmlsc]]", "decisions",
              related=["[[tip-9-1]]"])
    _example(vault, "09-decision-example-y", "draft", "", "orphans", related=[])

    _term(vault, "adr", "ADR", "review", legacy_tags=["adr", "ADRs"],
           home="[[section-9#Background (on ADRs)]]",
           body="**Definition.** An Architecture Decision Record.\n", updated="2026-09-01")
    _term(vault, "stakeholder", "Stakeholder", "draft", legacy_tags=[], home="",
           body="Someone with an interest in the system, without a formal definition here.\n")

    _keyword(vault, "lean")
    _system_page(vault, "htmlsc", "HTML Sanity Checker")

    _issue(vault, "ISS-001", "open", "minor", "gap", "2026-09-02", related=["[[tip-9-1]]"])
    _issue(vault, "ISS-002", "resolved", "major", "contradiction", "2026-09-01", related=["[[tip-9-2]]"])
    _issue(vault, "ISS-003", "open", "major", "risk", "2026-09-03", related=["[[section-3]]"])

    _log(vault)
    _ingest_workflow(vault)

    _placeholder(root / "_posts/09-decisions/2016-03-01-t-9-1.md")
    _placeholder(root / "_posts/09-decisions/2016-03-01-t-9-2.md")
    _placeholder(root / "_posts/09-decisions/2016-03-01-t-9-3.md")
    _placeholder(root / "_posts/03-context/2016-01-01-t-3-1.md")
    (root / "_pages").mkdir(parents=True, exist_ok=True)
    (root / "_examples").mkdir(parents=True, exist_ok=True)

    return root
