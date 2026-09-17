"""Heading ids exactly as the site generates them: kramdown's **GFM** parser.

`_config.yml` sets `kramdown.input: GFM` and `Gemfile.lock` pins
`kramdown-parser-gfm`, so headings do not get kramdown's own auto-ids; they get
GitHub's rule, applied to the heading's *rendered* text:

1. inline emphasis / code markers are consumed by the renderer before the id
   is computed, and HTML entities are decoded (`&lt;` → `<`);
2. downcase;
3. delete every character that is not a word character, a hyphen, a space or a
   tab (kramdown uses `\\p{Word}`, Python's `\\w` is the unicode equivalent);
4. translate each space and each tab to one hyphen — no stripping, no
   collapsing, so a leading space yields a leading hyphen and two spaces yield
   two hyphens.

Repeated ids get "-1", "-2", … as before. There is **no** "section" fallback:
when nothing survives (`### ...`), kramdown's GFM parser emits the heading with
no `id` attribute at all, and `assign_anchors` returns "" for it and leaves it
out of the duplicate counter, because an id that is never emitted cannot
collide with anything.

Known, deliberate simplification: emphasis is stripped by paired delimiters, so
a heading like `a_b_c`, which GFM renders literally, would lose its middle
underscores here. No heading in the vault or in `_pages/` looks like that.
"""
from __future__ import annotations

import html
import re

# A run of *, _ or ` wrapping some text — what the inline renderer consumes.
EMPHASIS_RE = re.compile(r"(\*{1,3}|_{1,3}|`+)(.+?)\1")
DROP_RE = re.compile(r"[^\w\- \t]")


def _strip_emphasis(s: str) -> str:
    while True:
        out = EMPHASIS_RE.sub(r"\2", s)
        if out == s:
            return out
        s = out


def gfm_heading_id(text: str) -> str:
    s = _strip_emphasis(text.strip())
    s = html.unescape(s)
    s = s.lower()
    s = DROP_RE.sub("", s)
    return s.replace(" ", "-").replace("\t", "-")


def assign_anchors(texts: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out: list[str] = []
    for t in texts:
        base = gfm_heading_id(t)
        if not base:
            out.append("")
            continue
        if base in seen:
            seen[base] += 1
            out.append(f"{base}-{seen[base]}")
        else:
            seen[base] = 0
            out.append(base)
    return out
