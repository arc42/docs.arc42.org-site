"""Heading ids exactly as kramdown (Jekyll's default markdown engine) generates them.

kramdown's auto_ids: drop everything before the first ASCII letter, drop every
character that is not [a-zA-Z0-9 -], turn spaces into hyphens, downcase, and
fall back to "section" when nothing is left. Repeated ids get "-1", "-2", ….
"""
from __future__ import annotations

import re


def kramdown_id(text: str) -> str:
    s = text.strip()
    s = re.sub(r"^[^a-zA-Z]+", "", s)
    s = re.sub(r"[^a-zA-Z0-9 -]", "", s)
    s = s.replace(" ", "-").lower()
    return s or "section"


def assign_anchors(texts: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out: list[str] = []
    for t in texts:
        base = kramdown_id(t)
        if base in seen:
            seen[base] += 1
            out.append(f"{base}-{seen[base]}")
        else:
            seen[base] = 0
            out.append(base)
    return out
