"""Render a page body (markdown + callouts + directives + wikilinks) to HTML.

Reuses braingen's `DIRECTIVE_RE` and `WIKILINK_RE` rather than re-deriving
them (D21).
"""
from __future__ import annotations

import re
from html import escape
from urllib.parse import quote

import markdown as _markdown

from braingen.parse import DIRECTIVE_RE
from braingen.wikilinks import WIKILINK_RE

CALLOUT_MARKER_RE = re.compile(r"^>\s*\[!([\w-]+)\]")
CALLOUT_LINE_RE = re.compile(r"^>[ \t]?(.*)$")

EXTENSIONS = ["tables", "fenced_code", "sane_lists", "md_in_html"]


def _process_callouts(lines: list[str]) -> list[str]:
    """A block starting with `> [!type]` runs until the first line that does
    not start with `>`. The marker line is dropped; the rest become a
    `<div class="callout {type}" markdown="1">` with one `>`/`> ` prefix
    stripped per line, surrounded by blank lines."""
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        m = CALLOUT_MARKER_RE.match(line)
        if not m:
            out.append(line)
            i += 1
            continue
        ctype = m.group(1)
        i += 1
        inner: list[str] = []
        while i < n and lines[i].startswith(">"):
            cm = CALLOUT_LINE_RE.match(lines[i])
            inner.append(cm.group(1) if cm else "")
            i += 1
        out.append("")
        out.append(f'<div class="callout {ctype}" markdown="1">')
        out.extend(inner)
        out.append("</div>")
        out.append("")
    return out


def _process_directives(lines: list[str]) -> list[str]:
    """`%% name: arg %%` / `%% name %%` become `<p class="directive">...</p>`."""
    out = []
    for line in lines:
        m = DIRECTIVE_RE.match(line.strip())
        if m:
            name, arg = m.group(1), (m.group(2) or "").strip()
            text = f"{name}: {arg}" if arg else name
            out.append(f'<p class="directive">{escape(text)}</p>')
        else:
            out.append(line)
    return out


def _wikilink_html(target: str, heading: str | None, label: str | None, known: set[str]) -> str:
    display = escape(label or (f"{target}#{heading}" if heading else target))
    if target in known:
        return f'<a class="wikilink" href="/page/{quote(target)}">{display}</a>'
    return f'<span class="wikilink broken">{display}</span>'


def _replace_wikilinks(text: str, known: set[str]) -> str:
    def repl(m: re.Match) -> str:
        target = m.group(1).strip()
        heading = (m.group(2) or "").strip() or None
        label = (m.group(3) or "").strip() or None
        return _wikilink_html(target, heading, label, known)

    return WIKILINK_RE.sub(repl, text)


def render_inline(text: str, known: set[str]) -> str:
    """A single string (e.g. a front-matter value) as safe inline HTML:
    `[[wikilinks]]` become links/broken-spans (as in `render`), everything
    else is HTML-escaped. Unlike `render`, this never runs markdown."""
    out: list[str] = []
    pos = 0
    for m in WIKILINK_RE.finditer(text):
        out.append(escape(text[pos:m.start()]))
        target = m.group(1).strip()
        heading = (m.group(2) or "").strip() or None
        label = (m.group(3) or "").strip() or None
        out.append(_wikilink_html(target, heading, label, known))
        pos = m.end()
    out.append(escape(text[pos:]))
    return "".join(out)


def render_meta(value, known: set[str]) -> str:
    """A front-matter value as safe HTML: strings and list items get their
    wikilinks resolved via `render_inline`; lists render comma-separated,
    dicts as "key: value" pairs. Mirrors the plain-text shape the old
    `fmt_meta` filter used, but with real links instead of raw `[[...]]`."""
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (list, tuple)):
        return ", ".join(render_meta(v, known) for v in value) if value else "—"
    if isinstance(value, dict):
        return ", ".join(f"{escape(str(k))}: {render_meta(v, known)}" for k, v in value.items()) if value else "—"
    if isinstance(value, str):
        return render_inline(value, known)
    return escape(str(value))


def render(body: str, known: set[str]) -> str:
    """Markdown -> HTML: callouts, then directives, then wikilinks, then
    `markdown.markdown` with tables/fenced_code/sane_lists/md_in_html."""
    lines = _process_callouts(body.splitlines())
    lines = _process_directives(lines)
    text = _replace_wikilinks("\n".join(lines), known)
    return _markdown.markdown(text, extensions=EXTENSIONS)
