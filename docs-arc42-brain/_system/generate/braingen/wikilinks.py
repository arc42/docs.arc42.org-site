"""Obsidian wikilink parsing: [[target]], [[target#heading]], [[target|label]]."""
from __future__ import annotations

import re
from dataclasses import dataclass

WIKILINK_RE = re.compile(r"\[\[([^\[\]|#]+?)(?:#([^\[\]|]+?))?(?:\|([^\[\]]+?))?\]\]")


@dataclass(frozen=True)
class WikiLink:
    target: str
    heading: str | None = None
    label: str | None = None

    def __str__(self) -> str:
        s = self.target
        if self.heading:
            s += f"#{self.heading}"
        if self.label:
            s += f"|{self.label}"
        return f"[[{s}]]"


def _clean(s: str | None) -> str | None:
    if s is None:
        return None
    s = s.strip()
    return s or None


def parse_wikilinks(text: str) -> list[WikiLink]:
    """Return every wikilink in `text`, in order. Embeds (![[...]]) are included."""
    return [
        WikiLink(m.group(1).strip(), _clean(m.group(2)), _clean(m.group(3)))
        for m in WIKILINK_RE.finditer(text)
    ]
