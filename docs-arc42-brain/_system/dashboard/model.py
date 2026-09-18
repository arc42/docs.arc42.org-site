"""The dashboard's model: an mtime-cached `Brain` (a loaded, linted vault)
and the tile/list views built over it.

Reads the vault only through braingen (`load_vault`, `lint`, `section_of`,
`plan`, `not_ingested`) — no parser of its own (design D21).
"""
from __future__ import annotations

import re
import subprocess
import threading
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from braingen.emit import section_of
from braingen.generate import plan
from braingen.lint import LINK_FIELDS, Finding, lint
from braingen.parity import PARITY_STATUSES, not_ingested
from braingen.parse import Page, Vault, load_vault

STATUSES = ("draft", "review", "published", "retired")

FAQ_NOTE = "136 answers in faq.arc42.org, not yet ingested"

LOG_LINE_RE = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\] ([\w-]+) \| (.*)$")
CHECKLIST_ITEM_RE = re.compile(r"^\d+\.\s+\*\*(\w+)\.\*\*\s*(.*)$")
CHECKLIST_LABELS = {"Read", "Vocabulary", "Links", "Issues", "Status"}


@dataclass
class Brain:
    repo: Path            # repo root (the Jekyll site)
    vault: Vault           # braingen Vault of repo/"docs-arc42-brain"
    findings: list[Finding]


class Model:
    """mtime-cached loader: `get()` reloads the vault only when its files
    changed since the last load; `clear()` forgets the cache outright."""

    def __init__(self, repo: Path):
        self.repo = Path(repo)
        self.vault_root = self.repo / "docs-arc42-brain"
        self._brain: Brain | None = None
        self._stamp: float | None = None
        self._lock = threading.Lock()

    def stamp(self) -> float:
        """Newest mtime under wiki/, raw/sources/, and of _system/log.md."""
        newest = 0.0
        for base in (self.vault_root / "wiki", self.vault_root / "raw" / "sources"):
            if base.is_dir():
                for f in base.rglob("*"):
                    if f.is_file():
                        newest = max(newest, f.stat().st_mtime)
        log = self.vault_root / "_system" / "log.md"
        if log.is_file():
            newest = max(newest, log.stat().st_mtime)
        return newest

    def get(self) -> Brain:
        with self._lock:
            s = self.stamp()
            if self._brain is None or s != self._stamp:
                vault = load_vault(self.vault_root)
                findings = lint(vault)
                self._brain = Brain(self.repo, vault, findings)
                self._stamp = s
            return self._brain

    def clear(self) -> None:
        with self._lock:
            self._brain = None
            self._stamp = None


def status_counts(pages) -> dict[str, int]:
    """Only the statuses that occur, in STATUSES order."""
    counts = Counter(p.status for p in pages)
    return {s: counts[s] for s in STATUSES if counts.get(s)}


def section_number(b: Brain, page: Page | None) -> int | None:
    """Section of a page: itself for a section, `section_of` for a tip or
    example (catching a page not attached to one), the target of `home` for
    a term when it is a section page. None otherwise, or on any dead end."""
    if page is None:
        return None
    if page.type == "section":
        return int(page.meta["number"])
    if page.type in ("tip", "example"):
        try:
            sec = section_of(b.vault, page)
        except ValueError:
            return None
        return int(sec.meta["number"])
    if page.type == "term":
        links = page.links_in("home")
        if not links:
            return None
        target = b.vault.pages.get(links[0].target)
        if target is None or target.type != "section":
            return None
        return int(target.meta["number"])
    return None


def open_issues(b: Brain) -> list[Page]:
    """Open issues (status open|in-progress), oldest created first."""
    issues = [p for p in b.vault.by_type("issue") if p.status in ("open", "in-progress")]
    return sorted(issues, key=lambda p: p.meta.get("created") or "")


def issue_targets(b: Brain, issue: Page) -> set[str]:
    """Slugs named in `related` plus every wikilink in the body."""
    return {l.target for l in issue.links_in("related")} | {l.target for l in issue.body_links}


def _pages_in_section(b: Brain, ptype: str, number: int) -> list[Page]:
    return [p for p in b.vault.by_type(ptype) if section_number(b, p) == number]


def _issue_targets_section(b: Brain, issue: Page, slug: str, number: int) -> bool:
    for t in issue_targets(b, issue):
        if t == slug:
            return True
        target = b.vault.pages.get(t)
        if target is not None and section_number(b, target) == number:
            return True
    return False


def sections_view(b: Brain, parity: dict[str, str]) -> dict:
    sections = sorted(b.vault.by_type("section"), key=lambda p: int(p.meta["number"]))
    open_iss = open_issues(b)
    rows = []
    for s in sections:
        n = int(s.meta["number"])
        rows.append({
            "number": n,
            "slug": s.slug,
            "title": s.meta.get("title"),
            "status": s.status,
            "tips": len(_pages_in_section(b, "tip", n)),
            "examples": len(_pages_in_section(b, "example", n)),
            "terms": len(_pages_in_section(b, "term", n)),
            "open_issues": sum(1 for i in open_iss if _issue_targets_section(b, i, s.slug, n)),
            "parity": parity.get(str(n)),
        })
    return {"counts": status_counts(sections), "rows": rows}


def tips_view(b: Brain) -> dict:
    tips = b.vault.by_type("tip")
    without_related = sorted(p.slug for p in tips if not p.links_in("related"))
    legacy = sorted(p.slug for p in tips if p.meta.get("legacy-tags"))
    return {"counts": status_counts(tips), "without_related": without_related, "legacy": legacy}


def _referenced_categories(b: Brain) -> set[str]:
    cats: set[str] = set()
    for s in b.vault.by_type("section"):
        for d in s.directives:
            if d.name == "examples" and d.arg:
                cats.add(d.arg)
    return cats


def examples_view(b: Brain) -> dict:
    examples = b.vault.by_type("example")
    by_system: Counter = Counter()
    for e in examples:
        links = e.links_in("system")
        if not links:
            by_system["(none)"] += 1
            continue
        target = b.vault.pages.get(links[0].target)
        name = str(target.meta.get("name")) if target is not None else links[0].target
        by_system[name] += 1
    categories = {e.meta.get("example-category") for e in examples if e.meta.get("example-category")}
    orphan_categories = sorted(categories - _referenced_categories(b))
    return {"counts": status_counts(examples), "by_system": dict(by_system), "orphan_categories": orphan_categories}


def faq_view(b: Brain) -> dict:
    faqs = b.vault.by_type("faq")
    note = None if faqs else FAQ_NOTE
    return {"count": len(faqs), "note": note}


def _tag_usage(b: Brain, key: str, slug: str) -> int:
    count = 0
    for p in b.vault.pages.values():
        if p.type == "issue":
            continue
        if any(l.target == slug for l in p.links_in(key)):
            count += 1
    return count


def tags_view(b: Brain) -> dict:
    terms = sorted(b.vault.by_type("term"), key=lambda p: p.slug)
    keywords = sorted(b.vault.by_type("keyword"), key=lambda p: p.slug)
    terms_usage = [(t.slug, _tag_usage(b, "terms", t.slug)) for t in terms]
    keywords_usage = [(k.slug, _tag_usage(b, "keywords", k.slug)) for k in keywords]
    incomplete = sorted(
        t.slug for t in terms
        if "**Definition.**" not in t.body or not t.links_in("home")
    )
    legacy = sorted(
        (str(tag), t.slug)
        for t in terms
        for tag in (t.meta.get("legacy-tags") or [])
        if str(tag) != t.slug
    )
    return {"terms": terms_usage, "keywords": keywords_usage, "incomplete_terms": incomplete, "legacy": legacy}


def issues_view(b: Brain) -> dict:
    open_iss = open_issues(b)
    by_severity = Counter(i.meta.get("severity") for i in open_iss)
    by_kind = Counter(i.meta.get("kind") for i in open_iss)
    return {"open": open_iss, "by_severity": dict(by_severity), "by_kind": dict(by_kind)}


def lint_view(b: Brain) -> dict:
    errors: dict[str, list[Finding]] = defaultdict(list)
    warnings: dict[str, list[Finding]] = defaultdict(list)
    for f in b.findings:
        (errors if f.level == "error" else warnings)[f.rule].append(f)
    return {"errors": dict(errors), "warnings": dict(warnings)}


def log_entries(b: Brain, n: int = 5) -> list[dict]:
    """Newest first: {date, kind, subject}, parsed from `_system/log.md`."""
    path = b.vault.root / "_system" / "log.md"
    if not path.is_file():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = LOG_LINE_RE.match(line)
        if m:
            entries.append({"date": m.group(1), "kind": m.group(2), "subject": m.group(3)})
    entries.reverse()
    return entries[:n]


def git_log(repo: Path, n: int = 10) -> list[dict]:
    """{hash, date, subject} for the last `n` commits touching docs-arc42-brain/; [] on any failure."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "log", f"-{n}", "--date=short",
             "--format=%h%x1f%ad%x1f%s", "--", "docs-arc42-brain/"],
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if result.returncode != 0:
        return []
    out = []
    for line in result.stdout.splitlines():
        parts = line.split("\x1f")
        if len(parts) != 3:
            continue
        out.append({"hash": parts[0], "date": parts[1], "subject": parts[2]})
    return out


def _ingest_checklist(b: Brain) -> list[tuple[str, str]]:
    """The numbered items of ingest.md whose bold label is one of
    CHECKLIST_LABELS; `label` without its dot, `text` with continuation
    lines joined by single spaces."""
    path = b.vault.root / "_system" / "workflows" / "ingest.md"
    if not path.is_file():
        return []
    items: list[tuple[str, list[str]]] = []
    label: str | None = None
    text: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = CHECKLIST_ITEM_RE.match(line)
        if m:
            if label is not None:
                items.append((label, text))
            label, first = m.group(1), m.group(2).strip()
            text = [first] if first else []
        elif line.strip() == "":
            if label is not None:
                items.append((label, text))
            label, text = None, []
        elif label is not None:
            text.append(line.strip())
    if label is not None:
        items.append((label, text))
    return [(l, " ".join(t).strip()) for l, t in items if l in CHECKLIST_LABELS]


def review_queue(b: Brain) -> dict:
    pages = sorted(
        (p for p in b.vault.pages.values() if p.status == "review"),
        key=lambda p: p.meta.get("updated") or "",
    )
    return {"pages": pages, "checklist": _ingest_checklist(b)}


def _lint_clean(b: Brain, slug: str, number: int) -> bool:
    for f in b.findings:
        if f.level != "error":
            continue
        if f.page == slug:
            return False
        target = b.vault.pages.get(f.page)
        if target is not None and section_number(b, target) == number:
            return False
    return True


def _ingested(b: Brain, number: int) -> bool:
    try:
        p = plan(b.vault, PARITY_STATUSES, section=number)
    except Exception:  # noqa: BLE001 - any planning failure means "not ready"
        return False
    generated = {o.rel for o in p.outputs}
    return not not_ingested(b.vault, b.repo, number, generated)


def _related_ok(b: Brain, number: int) -> bool:
    pages = [
        p for p in b.vault.by_type("tip") + b.vault.by_type("example")
        if p.status != "retired" and section_number(b, p) == number
    ]
    return all(p.links_in("related") for p in pages)


def readiness(b: Brain, parity: dict[str, str]) -> dict:
    sections = sorted(b.vault.by_type("section"), key=lambda p: int(p.meta["number"]))
    rows = []
    for s in sections:
        n = int(s.meta["number"])
        cut_over = s.status == "published"
        ingested = _ingested(b, n)
        lint_clean = _lint_clean(b, s.slug, n)
        par = parity.get(str(n))
        related = _related_ok(b, n)
        ready = (not cut_over) and ingested and lint_clean and par == "PASS" and related
        rows.append({
            "number": n, "slug": s.slug, "cut_over": cut_over, "ingested": ingested,
            "lint_clean": lint_clean, "parity": par, "related": related, "ready": ready,
        })
    nxt = next((r["number"] for r in rows if r["ready"]), None)
    return {"rows": rows, "next": nxt}


def _all_links(p: Page):
    links = list(p.body_links)
    for key in LINK_FIELDS:
        links += p.links_in(key)
    return links


def _names_type(b: Brain, p: Page, ptype: str) -> bool:
    for l in p.links_in("related"):
        target = b.vault.pages.get(l.target)
        if target is not None and target.type == ptype:
            return True
    return False


def _unlinked_subsections(b: Brain) -> list[tuple[str, str]]:
    linked: set[tuple[str, str]] = set()
    for p in b.vault.pages.values():
        for l in _all_links(p):
            if l.heading:
                linked.add((l.target, l.heading))
    result = []
    for s in sorted(b.vault.by_type("section"), key=lambda p: int(p.meta["number"])):
        for h in s.headings:
            if h.synthetic or h.level < 2:
                continue
            if (s.slug, h.text) not in linked:
                result.append((s.slug, h.text))
    return result


def _sections_without_related(b: Brain) -> list[str]:
    referenced: set[str] = set()
    for p in b.vault.pages.values():
        if p.type == "issue":
            continue
        for l in p.links_in("related"):
            referenced.add(l.target)
    return sorted(
        s.slug for s in b.vault.by_type("section")
        if not s.links_in("related") and s.slug not in referenced
    )


def gaps(b: Brain) -> dict:
    return {
        "tips_without_example": sorted(
            p.slug for p in b.vault.by_type("tip") if not _names_type(b, p, "example")
        ),
        "examples_without_tip": sorted(
            p.slug for p in b.vault.by_type("example") if not _names_type(b, p, "tip")
        ),
        "unlinked_subsections": _unlinked_subsections(b),
        "sections_without_related": _sections_without_related(b),
    }
