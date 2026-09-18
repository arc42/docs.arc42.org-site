"""Page emitters: one wiki page → one Jekyll file (front matter ending in the marker, body).

The front matter follows the key order and quoting of the hand-written files
so a cut-over diff stays small; the parity check compares values, not bytes.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

import yaml

from .emit_body import content_body, marker, section_document_body
from .parse import Page, Vault
from .wikilinks import WikiLink

KIND_BY_TYPE = {"section": "section", "tip": "tip", "example": "example", "faq": "faq",
                "term": "term", "keyword": "keyword", "system": "system"}
# Types whose pages exist on the site only once generated; a related link to an
# unpublished one would be dead, so it is left out.
PUBLISHED_ONLY = {"tip", "example", "faq"}


@dataclass(frozen=True)
class Output:
    rel: str      # path relative to the site root, e.g. "_posts/09-decisions/2016-03-01-t-9-1.md"
    text: str     # the complete file content
    source: str   # vault-relative brain page, e.g. "wiki/tips/tip-9-1.md"


def yaml_scalar(value, quote: bool = False) -> str:
    """One YAML scalar: plain when that reads back identically, else double-quoted."""
    if isinstance(value, bool) or value is None:
        raise TypeError(f"unsupported front-matter value {value!r}")
    if isinstance(value, int):
        return str(value)
    s = str(value)
    if not quote and s == s.strip() and s:
        try:
            if yaml.safe_load(f"k: {s}") == {"k": s}:
                return s
        except yaml.YAMLError:
            pass
    return json.dumps(s, ensure_ascii=False)


def render_frontmatter(items: list[tuple[str, object]], quoted: frozenset[str] = frozenset()) -> str:
    lines = ["---"]
    for key, value in items:
        if key == "related":
            if not value:
                continue
            lines.append("related:")
            for entry in value:
                lines.append(f"- kind: {entry['kind']}")
                lines.append(f"  title: {yaml_scalar(entry['title'], quote=True)}")
                if entry.get("url"):
                    lines.append(f"  url: {yaml_scalar(entry['url'])}")
            continue
        lines.append(f"{key}: {yaml_scalar(value, quote=key in quoted)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def document(front: str, source: str, body: str) -> str:
    """Front matter with the marker as its last line, one blank line, the body."""
    head = front.removesuffix("---\n")
    return f"{head}{marker(source)}\n---\n\n{body}"


def emit_section(vault: Vault, page: Page) -> Output:
    m = page.meta
    front = render_frontmatter([
        ("layout", "arc42-doc-section"),
        ("title", m["title"]),
        ("permalink", m["permalink"]),
        ("number", int(m["number"])),
        ("order", int(m["order"])),
    ])
    body = section_document_body(page.body, int(m["number"]), str(m["category"]), str(m["faq-topic"]))
    return Output(f"_pages/section-{int(m['number'])}.md", document(front, vault.rel(page.path), body), vault.rel(page.path))


def _target(vault: Vault, link: WikiLink) -> Page | None:
    return vault.pages.get(link.target)


def section_of(vault: Vault, page: Page) -> Page:
    links = page.links_in("section")
    target = _target(vault, links[0]) if links else None
    if target is None or target.type != "section":
        raise ValueError(f"{page.slug}: 'section' does not resolve to a section page")
    return target


def tags_for(vault: Vault, page: Page) -> list[str]:
    """Keywords, then terms, in declared order: the slug of each non-retired target."""
    out: list[str] = []
    for key in ("keywords", "terms"):
        for link in page.links_in(key):
            t = _target(vault, link)
            if t is None or t.status == "retired" or t.slug in out:
                continue
            out.append(t.slug)
    return out


def _entry(vault: Vault, link: WikiLink, emitted: set[str], site_tags: set[str]) -> dict | None:
    t = _target(vault, link)
    if t is None or t.status == "retired" or t.type not in KIND_BY_TYPE:
        return None
    if t.type in PUBLISHED_ONLY and t.slug not in emitted:
        return None
    if t.type == "section":
        url = str(t.meta["permalink"])
        if link.heading:
            head = next(h for h in t.headings if h.text == link.heading)
            return {"kind": "subsection", "title": link.label or link.heading, "url": f"{url}#{head.anchor}"}
        return {"kind": "section", "title": link.label or str(t.meta["title"]), "url": url}
    if t.type in ("term", "keyword"):
        title = str(t.meta.get("term") or t.meta.get("title"))
        url = f"/keywords/#{t.slug}" if t.slug in site_tags else ""
        return {"kind": t.type, "title": link.label or title, "url": url}
    if t.type == "system":
        return {"kind": "system", "title": link.label or str(t.meta.get("name")), "url": str(t.meta.get("url") or "")}
    return {"kind": t.type, "title": link.label or str(t.meta["title"]), "url": str(t.meta["permalink"])}


def related_for(vault: Vault, page: Page, emitted: set[str], site_tags: set[str]) -> list[dict]:
    """The page's section link first, then `related:` in declared order.

    `emitted` holds the slugs of the tips/examples/faq written in this run;
    `site_tags` the tags those tips carry, i.e. the /keywords/ anchors that exist.
    """
    out: list[dict] = []
    for link in page.links_in("section")[:1] + page.links_in("related"):
        e = _entry(vault, link, emitted, site_tags)
        if e is not None and e not in out:
            out.append(e)
    return out


def emit_tip(vault: Vault, page: Page, emitted: set[str], site_tags: set[str]) -> Output:
    m = page.meta
    sec = section_of(vault, page)
    front = render_frontmatter([
        ("layout", "post"),
        ("title", m["title"]),
        ("tags", " ".join(tags_for(vault, page))),
        ("category", sec.meta["category"]),
        ("permalink", m["permalink"]),
        ("related", related_for(vault, page, emitted, site_tags)),
    ], quoted=frozenset({"title"}))
    rel = f"_posts/{sec.meta['posts-dir']}/{m['date']}-t-{page.id}.md"
    return Output(rel, document(front, vault.rel(page.path), content_body(page.body)), vault.rel(page.path))


def emit_example(vault: Vault, page: Page, emitted: set[str], site_tags: set[str]) -> Output:
    m = page.meta
    front = render_frontmatter([
        ("layout", "post"),
        ("title", m["title"]),
        ("tags", " ".join(tags_for(vault, page))),
        ("category", m["example-category"]),
        ("permalink", m["permalink"]),
        ("related", related_for(vault, page, emitted, site_tags)),
    ], quoted=frozenset({"title"}))
    return Output(f"_examples/{page.id}.md", document(front, vault.rel(page.path), content_body(page.body)), vault.rel(page.path))
