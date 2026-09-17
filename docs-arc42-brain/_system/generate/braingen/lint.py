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

    def __str__(self) -> str:
        return f"{self.level.upper():7} {self.page}: {self.message}"


def lint(vault: Vault) -> list[Finding]:
    out: list[Finding] = [Finding("error", "vault", e) for e in vault.errors]
    ids_by_type: dict[str, Counter] = defaultdict(Counter)
    for p in vault.pages.values():
        ids_by_type[p.type][p.id] += 1
    for p in vault.pages.values():
        out += _schema(vault, p)
        out += _links(vault, p)
        out += _body(vault, p)
        if ids_by_type[p.type][p.id] > 1:
            out.append(Finding("error", p.slug, f"duplicate id {p.id} within type {p.type}"))
    out += _example_directives(vault)
    return out


def _schema(vault: Vault, p: Page) -> list[Finding]:
    f: list[Finding] = []
    if p.type not in TYPE_FOLDERS:
        f.append(Finding("error", p.slug, f"unknown type '{p.type}'"))
        return f
    expected = vault.root / TYPE_FOLDERS[p.type]
    if p.path.parent != expected:
        f.append(Finding("error", p.slug, f"type {p.type} belongs in {TYPE_FOLDERS[p.type]}"))
    for field in COMMON_FIELDS + REQUIRED_FIELDS[p.type]:
        if field not in p.meta or p.meta[field] is None:
            f.append(Finding("error", p.slug, f"missing field '{field}'"))
    allowed = STATUS_BY_TYPE.get(p.type, DEFAULT_STATUS)
    if p.status is not None and p.status not in allowed:
        f.append(Finding("error", p.slug, f"invalid status '{p.status}' (allowed: {', '.join(sorted(allowed))})"))
    if p.status == "published" and not p.meta.get("sources"):
        f.append(Finding("error", p.slug, "published without sources"))
    if p.status in {"review", "published"} and p.meta.get("legacy-tags"):
        f.append(Finding("error", p.slug, f"legacy-tags still present: {p.meta['legacy-tags']}"))
    return f


def _check_link(vault: Vault, p: Page, link: WikiLink) -> Finding | None:
    target = vault.pages.get(link.target)
    if target is None:
        return Finding("error", p.slug, f"unresolved link {link}")
    if link.heading:
        matches = [h for h in target.headings if h.text == link.heading]
        if not matches:
            return Finding("error", p.slug, f"heading '{link.heading}' not found on {target.slug} ({link})")
        if len(matches) > 1:
            return Finding("error", p.slug, f"heading '{link.heading}' is not unique on {target.slug} ({link})")
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
            f.append(Finding("warning", p.slug, f"related {link} is not reciprocated"))
    return f


def _body(vault: Vault, p: Page) -> list[Finding]:
    f: list[Finding] = []
    if p.has_liquid:
        f.append(Finding("error", p.slug, "Liquid syntax in body ({{ or {%)"))
    for img in p.images:
        if img.startswith(("http://", "https://")):
            continue
        if not (p.path.parent / img).resolve().exists():
            f.append(Finding("error", p.slug, f"missing image {img}"))
    for d in p.directives:
        if d.name not in DIRECTIVES:
            f.append(Finding("error", p.slug, f"unknown directive '{d.name}' (line {d.line})"))
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
            f.append(Finding("error", e.slug, f"example-category '{cat}' is not referenced by any section directive"))
        elif n > 1:
            f.append(Finding("warning", e.slug, f"example-category '{cat}' is referenced by {n} directives"))
    return f
