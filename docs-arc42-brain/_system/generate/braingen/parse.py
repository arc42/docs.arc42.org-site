"""Parse the vault: markdown + YAML frontmatter + wikilinks into Page and Vault."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import frontmatter

from .anchors import assign_anchors
from .wikilinks import WikiLink, parse_wikilinks

TYPE_FOLDERS: dict[str, str] = {
    "section": "wiki/sections",
    "tip": "wiki/tips",
    "example": "wiki/examples",
    "faq": "wiki/faq",
    "term": "wiki/terms",
    "keyword": "wiki/keywords",
    "system": "wiki/systems",
    "issue": "wiki/issues",
    "source": "raw/sources",
}

HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$")
DIRECTIVE_RE = re.compile(r"^%%\s*([a-z-]+)(?::\s*(.*?))?\s*%%\s*$")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
LIQUID_RE = re.compile(r"\{\{|\{%")
CALLOUT_PREFIX_RE = re.compile(r"^(?:>[ \t]?)+")


# Headings the generated page gains from the Jekyll includes, which the brain
# never writes but which take part in the page's anchor numbering all the same:
# `_includes/example.md` emits "### Examples" at every `%% examples: … %%`
# position, and `_includes/further-info.md` emits the fixed foot (its own
# "## Practical Tips" and "### Related Questions", then "### Complete Examples"
# from `_includes/examples-link.html variant="block"`).
INCLUDE_EXAMPLES_HEADING = (3, "Examples")
INCLUDE_FOOT_HEADINGS = [(2, "Practical Tips"), (3, "Related Questions"), (3, "Complete Examples")]


@dataclass
class Heading:
    level: int
    text: str
    anchor: str
    line: int
    # True for a heading that no line of the brain contains: the generator
    # injects it via a Jekyll include (see INCLUDE_* above). It is a real
    # heading on the rendered page, so it consumes an anchor and satisfies a
    # `[[section-N#Practical Tips]]` link, but the emitter must never write it
    # into the page body. `line` is then the body line the include sits on, or
    # one past the body for the foot.
    synthetic: bool = False


@dataclass
class Directive:
    name: str
    arg: str | None
    line: int


@dataclass
class Page:
    slug: str
    id: str
    type: str
    path: Path
    meta: dict
    body: str
    headings: list[Heading] = field(default_factory=list)
    directives: list[Directive] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    body_links: list[WikiLink] = field(default_factory=list)
    has_liquid: bool = False

    @property
    def status(self) -> str | None:
        v = self.meta.get("status")
        return str(v) if v is not None else None

    def links_in(self, key: str) -> list[WikiLink]:
        """Wikilinks found in the frontmatter field `key` (string or list of strings)."""
        v = self.meta.get(key)
        if v is None:
            return []
        values = [v] if isinstance(v, str) else list(v)
        out: list[WikiLink] = []
        for s in values:
            if isinstance(s, str):
                out.extend(parse_wikilinks(s))
        return out


def _scan_body(body: str) -> tuple[list[tuple[int, str, int]], list[Directive], bool]:
    heads: list[tuple[int, str, int]] = []
    dirs: list[Directive] = []
    liquid = False
    in_fence = False
    for n, raw in enumerate(body.splitlines(), 1):
        line = CALLOUT_PREFIX_RE.sub("", raw)
        if line.startswith("```") or line.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if LIQUID_RE.search(line):
            liquid = True
        m = HEADING_RE.match(line)
        if m:
            heads.append((len(m.group(1)), m.group(2).strip(), n))
            continue
        d = DIRECTIVE_RE.match(line.strip())
        if d:
            arg = (d.group(2) or "").strip() or None
            dirs.append(Directive(d.group(1), arg, n))
    return heads, dirs, liquid


def parse_page(path: Path) -> Page:
    post = frontmatter.load(path)
    body = post.content
    heads, dirs, liquid = _scan_body(body)
    ptype = str(post.get("type", "") or "")
    items: list[tuple[int, str, int, bool]] = [(l, t, n, False) for l, t, n in heads]
    if ptype == "section":
        lvl, txt = INCLUDE_EXAMPLES_HEADING
        items += [(lvl, txt, d.line, True) for d in dirs if d.name == "examples"]
        items.sort(key=lambda it: it[2])
        foot = len(body.splitlines()) + 1
        items += [(l, t, foot + i, True) for i, (l, t) in enumerate(INCLUDE_FOOT_HEADINGS)]
    anchors = assign_anchors([t for _, t, _, _ in items])
    page = Page(
        slug=path.stem,
        id=str(post.get("id", "") or ""),
        type=ptype,
        path=path,
        meta=dict(post.metadata),
        body=body,
    )
    page.headings = [Heading(l, t, a, n, s) for (l, t, n, s), a in zip(items, anchors)]
    page.directives = dirs
    page.images = IMAGE_RE.findall(body)
    page.body_links = parse_wikilinks(body)
    page.has_liquid = liquid
    return page


@dataclass
class Vault:
    root: Path
    pages: dict[str, Page]
    errors: list[str]

    def by_type(self, t: str) -> list[Page]:
        return [p for p in self.pages.values() if p.type == t]

    def rel(self, path: Path) -> str:
        return str(path.relative_to(self.root))


def load_vault(root: Path) -> Vault:
    root = Path(root)
    pages: dict[str, Page] = {}
    errors: list[str] = []
    for folder in TYPE_FOLDERS.values():
        d = root / folder
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.md")):
            rel = str(path.relative_to(root))
            try:
                page = parse_page(path)
            except Exception as e:  # noqa: BLE001 - report, don't crash the lint
                errors.append(f"{rel}: cannot parse ({e.__class__.__name__}: {e})")
                continue
            if not page.id:
                errors.append(f"{rel}: missing id")
                continue
            if page.slug in pages:
                other = str(pages[page.slug].path.relative_to(root))
                errors.append(f"{rel}: duplicate slug {page.slug} (also {other})")
                continue
            pages[page.slug] = page
    return Vault(root, pages, errors)
