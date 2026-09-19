"""Lint rules for the vault. Each rule appends Findings; the CLI decides the exit code."""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from .parse import TYPE_FOLDERS, Page, Vault
from .wikilinks import WikiLink

COMMON_FIELDS = ["id", "type", "title", "status", "created", "updated"]
REQUIRED_FIELDS: dict[str, list[str]] = {
    "section": ["number", "name", "category", "posts-dir", "permalink", "order", "faq-topic"],
    "tip": ["section", "date", "permalink"],
    "example": ["section", "example-category", "permalink"],
    "faq": ["question", "legacy-permalink", "legacy-category"],
    "term": ["term", "home"],
    "keyword": ["description", "featured"],
    "system": ["name"],
    "issue": ["severity", "kind", "raised-by"],
    "source": ["origin", "files"],
}
STATUS_BY_TYPE: dict[str, set[str]] = {
    "issue": {"open", "in-progress", "resolved", "wontfix"},
    "source": {"ingested"},
}
DEFAULT_STATUS = {"draft", "review", "published", "retired"}
LINK_FIELDS = ["related", "section", "sources", "home", "system", "ingested-pages"]
DIRECTIVES = {"examples", "examples-link"}


@dataclass
class Finding:
    level: str  # "error" | "warning"
    page: str
    message: str
    rule: str = "other"

    def __str__(self) -> str:
        return f"{self.level.upper():7} {self.page}: {self.message}"


def lint(vault: Vault) -> list[Finding]:
    out: list[Finding] = [Finding("error", "vault", e, "parse") for e in vault.errors]
    ids_by_type: dict[str, Counter] = defaultdict(Counter)
    for p in vault.pages.values():
        ids_by_type[p.type][p.id] += 1
    for p in vault.pages.values():
        out += _schema(vault, p)
        out += _links(vault, p)
        out += _body(vault, p)
        if ids_by_type[p.type][p.id] > 1:
            out.append(Finding("error", p.slug, f"duplicate id {p.id} within type {p.type}", "duplicate-id"))
    out += _example_directives(vault)
    out += _permalinks(vault)
    return out


def _schema(vault: Vault, p: Page) -> list[Finding]:
    f: list[Finding] = []
    if p.type not in TYPE_FOLDERS:
        f.append(Finding("error", p.slug, f"unknown type '{p.type}'", "type"))
        return f
    expected = vault.root / TYPE_FOLDERS[p.type]
    if p.path.parent != expected:
        f.append(Finding("error", p.slug, f"type {p.type} belongs in {TYPE_FOLDERS[p.type]}", "folder"))
    for field in COMMON_FIELDS + REQUIRED_FIELDS[p.type]:
        if field not in p.meta or p.meta[field] is None:
            f.append(Finding("error", p.slug, f"missing field '{field}'", "required-field"))
    allowed = STATUS_BY_TYPE.get(p.type, DEFAULT_STATUS)
    if p.status is not None and p.status not in allowed:
        f.append(Finding("error", p.slug, f"invalid status '{p.status}' (allowed: {', '.join(sorted(allowed))})", "status"))
    if p.status == "published" and not p.meta.get("sources"):
        f.append(Finding("error", p.slug, "published without sources", "sources"))
    # L13: legacy-tags are transient work items on imported pages and must be mapped away
    # before the page leaves draft. On a term page the same field is the permanent mapping of
    # old tag spellings to this term, so type `term` is exempt (see ISS-010).
    if p.status in {"review", "published"} and p.type != "term" and p.meta.get("legacy-tags"):
        f.append(Finding("error", p.slug, f"legacy-tags still present: {p.meta['legacy-tags']}", "legacy-tags"))
    return f


def _check_link(vault: Vault, p: Page, link: WikiLink) -> Finding | None:
    target = vault.pages.get(link.target)
    if target is None:
        return Finding("error", p.slug, f"unresolved link {link}", "link")
    if link.heading:
        matches = [h for h in target.headings if h.text == link.heading]
        if not matches:
            return Finding("error", p.slug, f"heading '{link.heading}' not found on {target.slug} ({link})", "heading")
        if len(matches) > 1:
            return Finding("error", p.slug, f"heading '{link.heading}' is not unique on {target.slug} ({link})", "heading")
    return None


def _links(vault: Vault, p: Page) -> list[Finding]:
    f: list[Finding] = []
    for key in LINK_FIELDS:
        for link in p.links_in(key):
            if (x := _check_link(vault, p, link)) is not None:
                f.append(x)
    for link in p.body_links:
        if (x := _check_link(vault, p, link)) is not None:
            f.append(x)
    for link in p.links_in("related"):
        target = vault.pages.get(link.target)
        if target is None or target.type == "section":
            continue
        if not any(back.target == p.slug for back in target.links_in("related")):
            f.append(Finding("warning", p.slug, f"related {link} is not reciprocated", "reciprocity"))
    return f


def _body(vault: Vault, p: Page) -> list[Finding]:
    f: list[Finding] = []
    if p.has_liquid:
        f.append(Finding("error", p.slug, "Liquid syntax in body ({{ or {%)", "liquid"))
    for img in p.images:
        if img.startswith(("http://", "https://")):
            continue
        if not (p.path.parent / img).resolve().exists():
            f.append(Finding("error", p.slug, f"missing image {img}", "image"))
    for d in p.directives:
        if d.name not in DIRECTIVES:
            f.append(Finding("error", p.slug, f"unknown directive '{d.name}' (line {d.line})", "directive"))
    return f


def _example_directives(vault: Vault) -> list[Finding]:
    f: list[Finding] = []
    refs: Counter = Counter()
    for s in vault.by_type("section"):
        for d in s.directives:
            if d.name == "examples" and d.arg:
                refs[d.arg] += 1
    seen: set[str] = set()
    for e in vault.by_type("example"):
        cat = e.meta.get("example-category")
        if not cat or cat in seen:
            continue
        seen.add(cat)
        n = refs.get(cat, 0)
        if n == 0:
            f.append(Finding("error", e.slug, f"example-category '{cat}' is not referenced by any section directive", "example-category"))
        elif n > 1:
            f.append(Finding("warning", e.slug, f"example-category '{cat}' is referenced by {n} directives", "example-category"))
    return f


PERMALINK_TYPES = {"section", "tip", "example"}


def _permalinks(vault: Vault) -> list[Finding]:
    """Two pages generating the same URL would overwrite each other on the site."""
    f: list[Finding] = []
    by_url: dict[str, list[str]] = defaultdict(list)
    for p in vault.pages.values():
        if p.type in PERMALINK_TYPES and p.status != "retired" and p.meta.get("permalink"):
            by_url[str(p.meta["permalink"])].append(p.slug)
    for url, slugs in sorted(by_url.items()):
        if len(slugs) > 1:
            for slug in sorted(slugs):
                others = ", ".join(s for s in sorted(slugs) if s != slug)
                f.append(Finding("error", slug, f"permalink {url} is also used by {others}", "permalink"))
    return f
