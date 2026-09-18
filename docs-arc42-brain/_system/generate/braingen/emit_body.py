"""Body transforms brain → Jekyll: the importer's conversions, inverted.

Pure text in, text out. Everything here introduces Liquid; nothing in the
brain contains any (brain spec §4.4).
"""
from __future__ import annotations

import re

MARKER_PREFIX = "<!-- generated from docs-arc42-brain/"
HELP_CALLOUT = "> [!arc42-help]"
HELP_OPEN = '<div class="arc42-help" markdown="1">'
HELP_CLOSE = "</div>"
DIRECTIVE_LINE_RE = re.compile(r"^%%\s*([a-z-]+)(?::\s*(.*?))?\s*%%\s*$")
FAQ_URL = "https://faq.arc42.org/category_c/#c-sec-{n}"

IMAGE_REWRITES = [
    ("../assets/sections/", "{{ site.imageurl }}/"),
    ("../assets/examples/", "{{ site.exampleimages }}/"),
]


def marker(source: str) -> str:
    """The line placed right after the front matter of every generated file."""
    return f"{MARKER_PREFIX}{source} — do not edit -->"


def is_generated(text: str) -> bool:
    """True when the first line after the front matter is a braingen marker."""
    if not text.startswith("---\n"):
        return False
    end = text.find("\n---\n", 3)
    if end < 0:
        return False
    return text[end + 5:].startswith(MARKER_PREFIX)


def rewrite_images(text: str) -> str:
    """Vault-relative image paths back to the site's Liquid variables."""
    for old, new in IMAGE_REWRITES:
        text = text.replace(old, new)
    return text


def _directive(line: str) -> str:
    m = DIRECTIVE_LINE_RE.match(line.strip())
    if not m:
        return line
    name, arg = m.group(1), (m.group(2) or "").strip()
    if name == "examples":
        return f'{{% include example.md category="{arg}" %}}'
    if name == "examples-link":
        return '{% include examples-link.html variant="inline" %}'
    raise ValueError(f"unknown directive {name!r}")


def _uncallout(line: str) -> str:
    if line == ">":
        return ""
    if line.startswith("> "):
        return line[2:]
    return line[1:]


def section_body(body: str) -> str:
    """Callouts → help divs, directives → includes, images → Liquid."""
    out: list[str] = []
    in_help = False
    for line in body.splitlines():
        if line.rstrip() == HELP_CALLOUT:
            if in_help:
                out.append(HELP_CLOSE)
            out.append(HELP_OPEN)
            in_help = True
            continue
        if in_help and not line.startswith(">"):
            out.append(HELP_CLOSE)
            in_help = False
        if in_help:
            line = _uncallout(line)
        out.append(rewrite_images(_directive(line)))
    if in_help:
        out.append(HELP_CLOSE)
    return "\n".join(out).rstrip("\n") + "\n"


def further_info(number: int, category: str, topic: str) -> str:
    return (
        "{% include further-info.md\n"
        f'   category="{category}"\n'
        f'   topic="{topic}"\n'
        f'   faqlink="{FAQ_URL.format(n=number)}" %}}\n'
    )


def section_document_body(body: str, number: int, category: str, topic: str) -> str:
    """The complete section body: converted brain content, two blank lines, the foot."""
    return section_body(body) + "\n\n" + further_info(number, category, topic)


def content_body(body: str) -> str:
    """Tip and example bodies: pass-through apart from image paths."""
    return rewrite_images(body).rstrip("\n") + "\n"
