"""Page emitters: one wiki page → one Jekyll file (front matter, marker, body).

The front matter follows the key order and quoting of the hand-written files
so a cut-over diff stays small; the parity check compares values, not bytes.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

import yaml

from .emit_body import marker, section_document_body
from .parse import Page, Vault


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
    return f"{front}{marker(source)}\n\n{body}"


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
