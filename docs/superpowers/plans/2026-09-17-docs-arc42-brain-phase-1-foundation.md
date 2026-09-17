# docs-arc42-brain Phase 1 (Foundation) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up the `docs-arc42-brain/` vault with its schema, workflows, a Python parser + lint, an importer that converts current site files into draft brain pages, all twelve section pages bootstrapped as drafts, and section 9 fully ingested so that `make brain-lint` passes.

**Architecture:** A Karpathy three-layer vault (`raw/` → `wiki/` → schema in `CLAUDE.md` + `_templates/`) inside this repo. A small Python package `braingen` under `_system/generate/` parses the vault into a model, lints it, and imports current site content into it. No generator yet (phase 2); nothing in the Jekyll site changes except the Makefile include and `.gitignore`.

**Tech Stack:** Python ≥ 3.12 managed by `uv`; `python-frontmatter`, `PyYAML`, `pytest`. GNU make. Obsidian for browsing.

**Spec:** `docs/superpowers/specs/2026-09-17-docs-arc42-brain-design.md` — the plan argues from it; read §3 (layout), §4 (metamodel), §5 (workflows), §8 (lint) before starting.

## Global Constraints

- Python `requires-python = ">=3.12"`; dependencies managed by `uv`; `uv.lock` is committed.
- **No Liquid in the brain.** `{{` or `{%` anywhere under `wiki/` is a lint error.
- Natural IDs: tip `9-1`, example `09-decision-example-adr`, section `section-9`, source `SRC-001`. `id` never changes. Filenames: tips `tip-N-M.md`, sections `section-N.md`, examples keep their stem.
- Wikilinks resolve by **filename stem** (Obsidian semantics); stems are unique across the whole vault. Wikilinks in YAML are quoted strings: `related: ["[[tip-9-2]]"]`.
- Statuses: `draft | review | published | retired`; issues `open | in-progress | resolved | wontfix`; sources `ingested`.
- Guidance blocks are Obsidian callouts `> [!arc42-help]`; directives are Obsidian comments `%% examples: <category> %%` and `%% examples-link %%`.
- Images in the brain are vault-relative markdown images (`../assets/sections/09/x.png`), never Liquid paths.
- English throughout. Dates absolute `YYYY-MM-DD`.
- Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Stage files explicitly (`git add <paths>`), never `git add -A`.
- All commands below run from the repo root `/Users/gernotstarke/projects/arc42/docs.arc42.org-site` on branch `docs-arc42-brain`.

## File structure

```
docs-arc42-brain/
  README.md                                  Task 7
  CLAUDE.md                                  Task 7  agent schema
  raw/.gitkeep  raw/ingested/.gitkeep  raw/sources/.gitkeep        Task 1
  wiki/{sections,tips,examples,faq,terms,keywords,systems,issues}/.gitkeep   Task 1
  wiki/assets/{sections,examples}/.gitkeep   Task 1
  _templates/{section,tip,example,faq,term,keyword,system,issue,source}.md   Task 7
  _system/index.md  _system/log.md           Task 7 (filled in Tasks 8, 9)
  _system/adr/0000-template.md, 0001…0005    Task 7
  _system/workflows/{bootstrap,ingest,audit,relations,cutover}.md            Task 7
  _system/brain.mk                           Task 1 (targets added in Tasks 4-6)
  _system/generate/
    pyproject.toml, uv.lock                  Task 1
    braingen/__init__.py                     Task 1
    braingen/wikilinks.py                    Task 2  [[target#heading|label]] parsing
    braingen/anchors.py                      Task 2  kramdown auto-ids
    braingen/parse.py                        Task 3  Page, Vault, load_vault
    braingen/lint.py                         Task 4  rules → Findings
    braingen/cli.py                          Task 4  `braingen lint|raw|import`
    braingen/raw.py                          Task 5  site → raw batch
    braingen/importer.py                     Task 6  raw batch → draft wiki pages
    tests/test_wikilinks.py, test_anchors.py, test_parse.py, test_lint.py, test_raw.py, test_importer.py
Makefile           (root, modify: add include)            Task 1
.gitignore         (root, modify)                          Task 1
```

---

### Task 1: Scaffold the vault, the Python package, and the Makefile wiring

**Files:**
- Create: `docs-arc42-brain/raw/.gitkeep`, `docs-arc42-brain/raw/ingested/.gitkeep`, `docs-arc42-brain/raw/sources/.gitkeep`
- Create: `docs-arc42-brain/wiki/<type>/.gitkeep` for `sections tips examples faq terms keywords systems issues`, plus `wiki/assets/sections/.gitkeep`, `wiki/assets/examples/.gitkeep`
- Create: `docs-arc42-brain/_system/generate/pyproject.toml`
- Create: `docs-arc42-brain/_system/generate/braingen/__init__.py`
- Create: `docs-arc42-brain/_system/generate/tests/test_smoke.py`
- Create: `docs-arc42-brain/_system/brain.mk`
- Modify: `Makefile` (append one `include` line)
- Modify: `.gitignore` (append)

**Interfaces:**
- Produces: `make brain-test` runs pytest via uv; `uv run --directory docs-arc42-brain/_system/generate braingen` is the CLI entry (added in Task 4).

- [x] **Step 1: Create the directory skeleton**

```bash
cd docs-arc42-brain
mkdir -p raw/ingested raw/sources wiki/sections wiki/tips wiki/examples wiki/faq wiki/terms wiki/keywords wiki/systems wiki/issues wiki/assets/sections wiki/assets/examples _templates _system/adr _system/workflows _system/generate/braingen _system/generate/tests
for d in raw raw/ingested raw/sources wiki/sections wiki/tips wiki/examples wiki/faq wiki/terms wiki/keywords wiki/systems wiki/issues wiki/assets/sections wiki/assets/examples; do touch "$d/.gitkeep"; done
cd ..
```

- [x] **Step 2: Write `pyproject.toml`**

Create `docs-arc42-brain/_system/generate/pyproject.toml`:

```toml
[project]
name = "braingen"
version = "0.1.0"
description = "Parser, lint, importer and (later) generator for docs-arc42-brain"
requires-python = ">=3.12"
dependencies = [
  "python-frontmatter>=1.1",
  "PyYAML>=6.0",
]

[project.scripts]
braingen = "braingen.cli:main"

[dependency-groups]
dev = ["pytest>=8.0"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["braingen"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Create `docs-arc42-brain/_system/generate/braingen/__init__.py`:

```python
"""braingen: tooling for the docs-arc42-brain vault."""

__version__ = "0.1.0"
```

- [x] **Step 3: Write the smoke test**

Create `docs-arc42-brain/_system/generate/tests/test_smoke.py`:

```python
import braingen


def test_package_imports():
    assert braingen.__version__ == "0.1.0"
```

- [x] **Step 4: Write `brain.mk` and include it from the root Makefile**

Create `docs-arc42-brain/_system/brain.mk`:

```make
# docs-arc42-brain targets. Included from the root Makefile, so every path
# here is relative to the repo root, which is where make runs.
BRAIN_DIR := $(CURDIR)/docs-arc42-brain
BRAIN_GEN := $(BRAIN_DIR)/_system/generate
# --directory makes uv (and pytest) run inside the package folder, so the
# pyproject there is the project and `tests/` is found; vault/site paths passed
# to braingen are absolute, so the cwd change does not matter to them.
BRAINGEN  := uv run --directory $(BRAIN_GEN) braingen

.PHONY: brain-test

brain-test: ## Run the braingen unit tests
	uv run --directory $(BRAIN_GEN) pytest -q
```

Append to the root `Makefile` (last line of the file):

```make

# docs-arc42-brain: parser, lint, importer, generator. See docs-arc42-brain/README.md
include docs-arc42-brain/_system/brain.mk
```

Append to root `.gitignore`:

```
# docs-arc42-brain
docs-arc42-brain/build/
docs-arc42-brain/.obsidian/
docs-arc42-brain/_system/generate/.venv/
__pycache__/
.pytest_cache/
```

- [x] **Step 5: Resolve dependencies and run the smoke test**

Run: `uv lock --project docs-arc42-brain/_system/generate && make brain-test`
Expected: `1 passed`, and a `uv.lock` file exists next to `pyproject.toml`. `make help` now lists `brain-test`.

- [x] **Step 6: Commit**

```bash
git add Makefile .gitignore docs-arc42-brain
git commit -m "brain: scaffold vault layout, braingen package, make wiring

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2: Wikilink parsing and kramdown anchors

**Files:**
- Create: `docs-arc42-brain/_system/generate/braingen/wikilinks.py`
- Create: `docs-arc42-brain/_system/generate/braingen/anchors.py`
- Test: `docs-arc42-brain/_system/generate/tests/test_wikilinks.py`, `tests/test_anchors.py`

**Interfaces:**
- Produces: `WikiLink(target: str, heading: str | None, label: str | None)` frozen dataclass; `parse_wikilinks(text: str) -> list[WikiLink]`; `kramdown_id(text: str) -> str`; `assign_anchors(texts: list[str]) -> list[str]` (duplicates get `-1`, `-2`, … like kramdown).

- [x] **Step 1: Write the failing wikilink tests**

Create `tests/test_wikilinks.py`:

```python
from braingen.wikilinks import WikiLink, parse_wikilinks


def test_plain_link():
    assert parse_wikilinks("see [[tip-9-2]]") == [WikiLink("tip-9-2", None, None)]


def test_link_with_heading():
    assert parse_wikilinks("[[section-5#5.1 Whitebox Overall System]]") == [
        WikiLink("section-5", "5.1 Whitebox Overall System", None)
    ]


def test_link_with_label():
    assert parse_wikilinks("[[tip-9-1|Document only relevant decisions]]") == [
        WikiLink("tip-9-1", None, "Document only relevant decisions")
    ]


def test_link_with_heading_and_label():
    assert parse_wikilinks("[[section-9#Background (on ADRs)|ADR background]]") == [
        WikiLink("section-9", "Background (on ADRs)", "ADR background")
    ]


def test_multiple_links_and_whitespace():
    links = parse_wikilinks("a [[ x ]] b [[y#h | l]] c")
    assert links == [WikiLink("x", None, None), WikiLink("y", "h", "l")]


def test_no_links():
    assert parse_wikilinks("nothing [here] or [[unclosed") == []
```

- [x] **Step 2: Run to verify failure**

Run: `uv run --directory docs-arc42-brain/_system/generate pytest tests/test_wikilinks.py -q`
Expected: FAIL, `ModuleNotFoundError: No module named 'braingen.wikilinks'`

- [x] **Step 3: Implement `wikilinks.py`**

```python
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
```

- [x] **Step 4: Run wikilink tests**

Run: `uv run --directory docs-arc42-brain/_system/generate pytest tests/test_wikilinks.py -q`
Expected: `6 passed`

- [x] **Step 5: Write the failing anchor tests**

Create `tests/test_anchors.py`:

```python
from braingen.anchors import assign_anchors, kramdown_id


def test_numbered_subsection_drops_leading_number():
    assert kramdown_id("5.1 Whitebox Overall System") == "whitebox-overall-system"


def test_parentheses_and_case():
    assert kramdown_id("Background (on ADRs)") == "background-on-adrs"


def test_placeholder_markup_is_stripped():
    assert kramdown_id("6.1 _<Runtime Scenario 1>_") == "runtime-scenario-1"


def test_trailing_space_is_ignored():
    assert kramdown_id("1.2 Quality Goals ") == "quality-goals"


def test_empty_falls_back_to_section():
    assert kramdown_id("###") == "section"


def test_duplicates_get_numeric_suffix():
    assert assign_anchors(["Content", "Motivation", "Content", "Content"]) == [
        "content",
        "motivation",
        "content-1",
        "content-2",
    ]
```

- [x] **Step 6: Run to verify failure**

Run: `uv run --directory docs-arc42-brain/_system/generate pytest tests/test_anchors.py -q`
Expected: FAIL, `ModuleNotFoundError: No module named 'braingen.anchors'`

- [x] **Step 7: Implement `anchors.py`**

```python
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
```

- [x] **Step 8: Run all tests**

Run: `make brain-test`
Expected: `13 passed`

- [x] **Step 9: Commit**

```bash
git add docs-arc42-brain/_system/generate
git commit -m "brain: wikilink parser and kramdown anchor ids

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 3: Page and vault parser

**Files:**
- Create: `docs-arc42-brain/_system/generate/braingen/parse.py`
- Test: `docs-arc42-brain/_system/generate/tests/test_parse.py`

**Interfaces:**
- Consumes: `parse_wikilinks`, `assign_anchors` from Task 2.
- Produces:
  - `TYPE_FOLDERS: dict[str, str]` mapping type → folder relative to the vault root.
  - `Heading(level: int, text: str, anchor: str, line: int)`, `Directive(name: str, arg: str | None, line: int)`.
  - `Page(slug, id, type, path, meta, body, headings, directives, images, body_links, has_liquid)` with `Page.links_in(key) -> list[WikiLink]` and `Page.status`.
  - `Vault(root, pages: dict[str, Page], errors: list[str])` with `Vault.by_type(t)`; `load_vault(root: Path) -> Vault`; `parse_page(path: Path) -> Page`.
  - Pages are keyed by **filename stem** (`slug`), not by `id`.

- [x] **Step 1: Write the failing parser tests**

Create `tests/test_parse.py`:

```python
from pathlib import Path

import pytest

from braingen.parse import TYPE_FOLDERS, load_vault, parse_page


def write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


TIP = """---
id: 9-1
type: tip
title: "Tip 9-1: Document only architecturally relevant decisions!"
status: draft
section: "[[section-9#Background (on ADRs)]]"
related: ["[[tip-9-2]]", "[[09-decision-example-adr|the ADR example]]"]
---

Some text linking [[section-9]].

![flow](../assets/sections/09/flow.png)

## Content

## Content
"""

SECTION = """---
id: section-9
type: section
title: 9 - Architecture decisions
status: draft
---

# 9. Architecture Decisions

> [!arc42-help]
> ## Content
> Important decisions.
> %% examples: decisions %%

%% examples-link %%

## Background (on ADRs)

~~~
# not a heading, inside a fence
{{ not liquid either, inside a fence }}
~~~
"""


def test_parse_page_extracts_meta_headings_links_images(tmp_path):
    p = write(tmp_path, "wiki/tips/tip-9-1.md", TIP)
    page = parse_page(p)
    assert page.slug == "tip-9-1"
    assert page.id == "9-1"
    assert page.type == "tip"
    assert page.status == "draft"
    assert [h.text for h in page.headings] == ["Content", "Content"]
    assert [h.anchor for h in page.headings] == ["content", "content-1"]
    assert [l.target for l in page.body_links] == ["section-9"]
    assert page.images == ["../assets/sections/09/flow.png"]
    assert page.has_liquid is False
    sec = page.links_in("section")
    assert sec[0].target == "section-9" and sec[0].heading == "Background (on ADRs)"
    assert [l.target for l in page.links_in("related")] == ["tip-9-2", "09-decision-example-adr"]
    assert page.links_in("missing") == []


def test_headings_and_directives_inside_callouts_and_not_inside_fences(tmp_path):
    p = write(tmp_path, "wiki/sections/section-9.md", SECTION)
    page = parse_page(p)
    assert [(h.level, h.text) for h in page.headings] == [
        (1, "9. Architecture Decisions"),
        (2, "Content"),
        (2, "Background (on ADRs)"),
    ]
    assert [(d.name, d.arg) for d in page.directives] == [
        ("examples", "decisions"),
        ("examples-link", None),
    ]
    assert page.has_liquid is False


def test_liquid_outside_fences_is_detected(tmp_path):
    p = write(tmp_path, "wiki/tips/tip-x.md", "---\nid: x\ntype: tip\n---\n{{ site.imageurl }}\n")
    assert parse_page(p).has_liquid is True


def test_load_vault_keys_by_stem_and_reports_duplicates(tmp_path):
    write(tmp_path, "wiki/tips/tip-9-1.md", TIP)
    write(tmp_path, "wiki/sections/section-9.md", SECTION)
    write(tmp_path, "wiki/terms/tip-9-1.md", "---\nid: dup\ntype: term\n---\n")
    write(tmp_path, "wiki/issues/broken.md", "---\nid: [unclosed\n---\n")
    write(tmp_path, "wiki/keywords/no-id.md", "---\ntype: keyword\n---\n")
    vault = load_vault(tmp_path)
    assert set(vault.pages) == {"tip-9-1", "section-9"}
    assert vault.by_type("tip")[0].id == "9-1"
    joined = "\n".join(vault.errors)
    assert "duplicate slug tip-9-1" in joined
    assert "wiki/issues/broken.md" in joined
    assert "wiki/keywords/no-id.md: missing id" in joined


def test_type_folders_cover_all_types():
    assert set(TYPE_FOLDERS) == {
        "section", "tip", "example", "faq", "term", "keyword", "system", "issue", "source",
    }
    assert TYPE_FOLDERS["source"] == "raw/sources"
```

- [x] **Step 2: Run to verify failure**

Run: `uv run --directory docs-arc42-brain/_system/generate pytest tests/test_parse.py -q`
Expected: FAIL, `ModuleNotFoundError: No module named 'braingen.parse'`

- [x] **Step 3: Implement `parse.py`**

```python
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


@dataclass
class Heading:
    level: int
    text: str
    anchor: str
    line: int


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
    anchors = assign_anchors([t for _, t, _ in heads])
    page = Page(
        slug=path.stem,
        id=str(post.get("id", "") or ""),
        type=str(post.get("type", "") or ""),
        path=path,
        meta=dict(post.metadata),
        body=body,
    )
    page.headings = [Heading(l, t, a, n) for (l, t, n), a in zip(heads, anchors)]
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
```

- [x] **Step 4: Run the parser tests**

Run: `uv run --directory docs-arc42-brain/_system/generate pytest tests/test_parse.py -q`
Expected: `5 passed`

- [x] **Step 5: Commit**

```bash
git add docs-arc42-brain/_system/generate
git commit -m "brain: vault parser (frontmatter, headings, directives, links)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 4: Lint rules and the `braingen lint` command

**Files:**
- Create: `docs-arc42-brain/_system/generate/braingen/lint.py`
- Create: `docs-arc42-brain/_system/generate/braingen/cli.py`
- Modify: `docs-arc42-brain/_system/brain.mk` (add `brain-lint`)
- Test: `docs-arc42-brain/_system/generate/tests/test_lint.py`

**Interfaces:**
- Consumes: `Vault`, `Page`, `TYPE_FOLDERS`, `load_vault` from Task 3.
- Produces: `Finding(level: "error"|"warning", page: str, message: str)`; `lint(vault: Vault) -> list[Finding]`; `REQUIRED_FIELDS`, `COMMON_FIELDS`; CLI `braingen lint <vault>` exiting 1 on any error.

Rules (spec §8, adapted to phase 1):

| # | Level | Rule |
|---|---|---|
| L1 | error | every `Vault.errors` entry (parse failure, missing id, duplicate slug) |
| L2 | error | unknown `type` |
| L3 | error | page not in the folder `TYPE_FOLDERS[type]` |
| L4 | error | missing required field (common + per type) |
| L5 | error | invalid `status` for the type |
| L6 | error | `id` duplicated within a type |
| L7 | error | unresolved wikilink (frontmatter link fields or body) |
| L8 | error | link with `#heading` whose heading is absent or not unique on the target page |
| L9 | warning | `related:` link not reciprocated by the target, unless the target is a section |
| L10 | error | `status: published` without `sources` |
| L11 | error | image path does not exist relative to the page |
| L12 | error | Liquid in the body |
| L13 | error | `legacy-tags` non-empty while `status` is `review` or `published` |
| L14 | error / warning | an example's `example-category` is referenced by zero (error) or more than one (warning) `%% examples: … %%` directive across section pages |
| L15 | error | unknown directive name (only `examples` and `examples-link` exist) |

- [x] **Step 1: Write the failing lint tests**

Create `tests/test_lint.py`:

```python
from pathlib import Path

import yaml

from braingen.lint import lint
from braingen.parse import load_vault


def page(root: Path, rel: str, meta: dict, body: str = "") -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    fm = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True)
    p.write_text(f"---\n{fm}---\n\n{body}\n", encoding="utf-8")


BASE = {"status": "draft", "created": "2026-09-17", "updated": "2026-09-17", "sources": [], "related": []}


def section(root, n=9, body="", **extra):
    meta = {
        "id": f"section-{n}", "type": "section", "title": f"{n} - X", **BASE,
        "number": n, "name": "X", "category": "decisions", "posts-dir": "09-decisions",
        "permalink": f"/section-{n}/", "order": 13, "faq-topic": "decisions", **extra,
    }
    page(root, f"wiki/sections/section-{n}.md", meta, body)


def tip(root, id="9-1", body="", **extra):
    meta = {"id": id, "type": "tip", "title": f"Tip {id}", **BASE, "section": "[[section-9]]",
            "keywords": [], "terms": [], "legacy-tags": [], "date": "2016-03-01",
            "permalink": f"/tips/{id}/", **extra}
    page(root, f"wiki/tips/tip-{id}.md", meta, body)


def errors(vault_root):
    return [str(f) for f in lint(load_vault(vault_root)) if f.level == "error"]


def warnings(vault_root):
    return [str(f) for f in lint(load_vault(vault_root)) if f.level == "warning"]


def test_clean_vault_has_no_findings(tmp_path):
    section(tmp_path, body="# 9\n\n> [!arc42-help]\n> %% examples: decisions %%\n")
    tip(tmp_path)
    assert lint(load_vault(tmp_path)) == []


def test_unknown_type_and_wrong_folder(tmp_path):
    page(tmp_path, "wiki/tips/x.md", {"id": "x", "type": "banana", **BASE, "title": "x"})
    page(tmp_path, "wiki/terms/section-1.md", {"id": "section-1", "type": "section", **BASE, "title": "x"})
    e = "\n".join(errors(tmp_path))
    assert "unknown type 'banana'" in e
    assert "section-1: type section belongs in wiki/sections" in e


def test_missing_required_fields_and_bad_status(tmp_path):
    page(tmp_path, "wiki/tips/tip-9-1.md", {"id": "9-1", "type": "tip", "title": "t", "status": "bogus"})
    e = "\n".join(errors(tmp_path))
    for f in ("created", "updated", "section", "date", "permalink"):
        assert f"missing field '{f}'" in e
    assert "invalid status 'bogus'" in e


def test_issue_and_source_have_their_own_status_sets(tmp_path):
    page(tmp_path, "wiki/issues/ISS-001-q.md", {"id": "ISS-001", "type": "issue", "title": "q", **BASE,
         "status": "open", "severity": "minor", "kind": "question", "raised-by": "agent"})
    page(tmp_path, "raw/sources/SRC-001-x.md", {"id": "SRC-001", "type": "source", "title": "x", **BASE,
         "status": "ingested", "origin": "raw/x/", "files": []})
    assert errors(tmp_path) == []


def test_duplicate_id_within_type(tmp_path):
    tip(tmp_path, id="9-1")
    page(tmp_path, "wiki/tips/tip-9-1-copy.md", {"id": "9-1", "type": "tip", "title": "t", **BASE,
         "section": "[[section-9]]", "date": "2016-03-01", "permalink": "/tips/9-1/"})
    section(tmp_path, body="> %% examples: decisions %%")
    assert any("duplicate id 9-1" in e for e in errors(tmp_path))


def test_unresolved_and_ambiguous_heading_links(tmp_path):
    section(tmp_path, body="# 9\n\n## Content\n\n## Content\n\n## Form\n\n> %% examples: decisions %%")
    tip(tmp_path, body="[[nowhere]] [[section-9#Form]] [[section-9#Content]] [[section-9#Nope]]")
    e = "\n".join(errors(tmp_path))
    assert "unresolved link [[nowhere]]" in e
    assert "heading 'Content' is not unique on section-9" in e
    assert "heading 'Nope' not found on section-9" in e
    assert "[[section-9#Form]]" not in e


def test_related_reciprocity_is_a_warning_except_for_sections(tmp_path):
    section(tmp_path, body="> %% examples: decisions %%")
    tip(tmp_path, id="9-1", related=["[[tip-9-2]]", "[[section-9]]"])
    tip(tmp_path, id="9-2")
    assert errors(tmp_path) == []
    w = "\n".join(warnings(tmp_path))
    assert "tip-9-1: related [[tip-9-2]] is not reciprocated" in w
    assert "section-9" not in w


def test_published_requires_sources_and_no_legacy_tags(tmp_path):
    section(tmp_path, body="> %% examples: decisions %%")
    tip(tmp_path, status="published", sources=[], **{"legacy-tags": ["decision"]})
    e = "\n".join(errors(tmp_path))
    assert "published without sources" in e
    assert "legacy-tags still present" in e


def test_images_must_exist_and_liquid_is_forbidden(tmp_path):
    section(tmp_path, body="> %% examples: decisions %%")
    (tmp_path / "wiki/assets/sections/09").mkdir(parents=True)
    (tmp_path / "wiki/assets/sections/09/ok.png").write_bytes(b"x")
    tip(tmp_path, body="![a](../assets/sections/09/ok.png) ![b](../assets/sections/09/missing.png) {{ site.imageurl }}")
    e = "\n".join(errors(tmp_path))
    assert "missing image ../assets/sections/09/missing.png" in e
    assert "ok.png" not in e
    assert "Liquid syntax in body" in e


def test_example_category_must_be_referenced_exactly_once(tmp_path):
    section(tmp_path, n=9, body="> %% examples: decisions %%\n> %% bogus %%")
    section(tmp_path, n=8, body="> %% examples: decisions %%", category="concepts", **{"posts-dir": "08-concepts"})
    page(tmp_path, "wiki/examples/ex-a.md", {"id": "ex-a", "type": "example", "title": "a", **BASE,
         "section": "[[section-9]]", "example-category": "decisions", "permalink": "/examples/a/"})
    page(tmp_path, "wiki/examples/ex-b.md", {"id": "ex-b", "type": "example", "title": "b", **BASE,
         "section": "[[section-9]]", "example-category": "orphaned", "permalink": "/examples/b/"})
    e = "\n".join(errors(tmp_path))
    w = "\n".join(warnings(tmp_path))
    assert "example-category 'orphaned' is not referenced by any section directive" in e
    assert "unknown directive 'bogus'" in e
    assert "example-category 'decisions' is referenced by 2 directives" in w
```

- [x] **Step 2: Run to verify failure**

Run: `uv run --directory docs-arc42-brain/_system/generate pytest tests/test_lint.py -q`
Expected: FAIL, `ModuleNotFoundError: No module named 'braingen.lint'`

- [x] **Step 3: Implement `lint.py`**

```python
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
```

- [x] **Step 4: Implement `cli.py` with the `lint` command**

```python
"""braingen command line: lint | raw | import."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .lint import lint
from .parse import load_vault


def cmd_lint(args: argparse.Namespace) -> int:
    findings = lint(load_vault(args.vault))
    for x in findings:
        print(x)
    errors = sum(1 for x in findings if x.level == "error")
    print(f"{len(findings)} findings, {errors} errors, {len(findings) - errors} warnings")
    return 1 if errors else 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="braingen", description="docs-arc42-brain tooling")
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("lint", help="validate the vault")
    l.add_argument("vault", type=Path)
    l.set_defaults(func=cmd_lint)
    return ap


def main(argv: list[str] | None = None) -> int:
    ap = build_parser()
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
```

- [x] **Step 5: Run the lint tests**

Run: `uv run --directory docs-arc42-brain/_system/generate pytest tests/test_lint.py -q`
Expected: `10 passed`

- [x] **Step 6: Add the `brain-lint` target**

Append to `docs-arc42-brain/_system/brain.mk` (and add `brain-lint` to the `.PHONY` line):

```make
brain-lint: ## Validate the brain: schema, links, anchors, images, no Liquid
	$(BRAINGEN) lint $(BRAIN_DIR)
```

Run: `make brain-lint`
Expected: `0 findings, 0 errors, 0 warnings` and exit code 0 (the vault is still empty).

- [x] **Step 7: Commit**

```bash
git add docs-arc42-brain/_system
git commit -m "brain: lint rules and braingen lint command

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 5: `braingen raw` — copy one section's site files into a raw batch

**Files:**
- Create: `docs-arc42-brain/_system/generate/braingen/raw.py`
- Modify: `docs-arc42-brain/_system/generate/braingen/cli.py` (add `raw` subcommand)
- Modify: `docs-arc42-brain/_system/brain.mk` (add `brain-raw`)
- Test: `docs-arc42-brain/_system/generate/tests/test_raw.py`

**Interfaces:**
- Produces: `make_raw(site: Path, vault: Path, section: int, what: str) -> Path` where `what ∈ {"all", "page", "content"}`. Creates `raw/section-<N>-<what>/` containing `manifest.yaml`, `pages/section-N.md` (page, all), `posts/*.md` and `examples/*.md` (content, all), and `assets/sections/<NN>/…`, `assets/examples/…` for every image the copied files reference. Refuses to overwrite an existing batch.
- `manifest.yaml` keys: `section` (int), `what`, `name`, `category`, `permalink`, `posts_dir`, `order`, `title`, `example_categories` (list, from the page's `example.md` includes), `files` (list of copied relative paths).

The batch layout is the contract the importer (Task 6) reads. Section metadata comes from `_data/sections.yml` (number, name, category, permalink), the `_posts/NN-*` directory name, and the page's own frontmatter (`title`, `order`).

- [x] **Step 1: Write the failing test with a miniature site fixture**

Create `tests/test_raw.py`:

```python
from pathlib import Path

import pytest
import yaml

from braingen.raw import make_raw

SECTIONS_YML = """
- number: 9
  name: Architecture Decisions
  category: decisions
  permalink: /section-9/
  examples_slug: 09-architecture-decisions
"""

PAGE = """---
layout: arc42-doc-section
title: 9 - Architecture decisions
permalink: /section-9/
number: 9
order: 13
---

# 9. Architecture Decisions

<div class="arc42-help" markdown="1">

## Content
Important decisions.

![flow]({{ site.imageurl }}/09/flow.png)

{% include example.md category="decisions" %}

</div>

{% include examples-link.html variant="inline" %}

{% include further-info.md
   category="decisions"
   topic="fundamental architecture and design decisions"
   faqlink="https://faq.arc42.org/category_c/#c-sec-9" %}
"""

TIP = """---
layout: post
title: "Tip 9-1: Document only architecturally relevant decisions!"
tags: decision quality stakeholder lean
category: decisions
permalink: /tips/9-1/
---

Body of the tip.
"""

EXAMPLE = """---
layout: post
title: "Example Decision: Use ADRs in Nygard format"
tags: decision example
category: decisions
permalink: /examples/decision-use-adrs/
---

![table]({{ site.exampleimages }}/adr-table.png)
"""

OTHER_EXAMPLE = EXAMPLE.replace("category: decisions", "category: concepts")


def build_site(root: Path) -> Path:
    site = root / "site"
    (site / "_data").mkdir(parents=True)
    (site / "_data/sections.yml").write_text(SECTIONS_YML)
    (site / "_pages").mkdir()
    (site / "_pages/section-9.md").write_text(PAGE)
    (site / "_posts/09-decisions").mkdir(parents=True)
    (site / "_posts/09-decisions/2016-03-01-t-9-1.md").write_text(TIP)
    (site / "_examples").mkdir()
    (site / "_examples/09-decision-example-adr.md").write_text(EXAMPLE)
    (site / "_examples/08-concept-example-x.md").write_text(OTHER_EXAMPLE)
    (site / "assets/images/sections/09").mkdir(parents=True)
    (site / "assets/images/sections/09/flow.png").write_bytes(b"png")
    (site / "assets/images/examples").mkdir(parents=True)
    (site / "assets/images/examples/adr-table.png").write_bytes(b"png")
    return site


def test_raw_all_copies_page_posts_matching_examples_and_images(tmp_path):
    site = build_site(tmp_path)
    vault = tmp_path / "vault"
    batch = make_raw(site, vault, 9, "all")
    assert batch == vault / "raw/section-9-all"
    assert (batch / "pages/section-9.md").read_text() == PAGE
    assert (batch / "posts/2016-03-01-t-9-1.md").read_text() == TIP
    assert (batch / "examples/09-decision-example-adr.md").exists()
    assert not (batch / "examples/08-concept-example-x.md").exists()
    assert (batch / "assets/sections/09/flow.png").read_bytes() == b"png"
    assert (batch / "assets/examples/adr-table.png").read_bytes() == b"png"
    m = yaml.safe_load((batch / "manifest.yaml").read_text())
    assert m["section"] == 9 and m["what"] == "all"
    assert m["name"] == "Architecture Decisions"
    assert m["category"] == "decisions"
    assert m["posts_dir"] == "09-decisions"
    assert m["permalink"] == "/section-9/"
    assert m["order"] == 13
    assert m["title"] == "9 - Architecture decisions"
    assert m["example_categories"] == ["decisions"]
    assert "pages/section-9.md" in m["files"] and "posts/2016-03-01-t-9-1.md" in m["files"]


def test_raw_page_only_and_content_only(tmp_path):
    site = build_site(tmp_path)
    vault = tmp_path / "vault"
    page_batch = make_raw(site, vault, 9, "page")
    assert (page_batch / "pages/section-9.md").exists()
    assert not (page_batch / "posts").exists()
    content_batch = make_raw(site, vault, 9, "content")
    assert not (content_batch / "pages").exists()
    assert (content_batch / "posts/2016-03-01-t-9-1.md").exists()
    assert (content_batch / "examples/09-decision-example-adr.md").exists()


def test_raw_refuses_to_overwrite(tmp_path):
    site = build_site(tmp_path)
    vault = tmp_path / "vault"
    make_raw(site, vault, 9, "page")
    with pytest.raises(FileExistsError):
        make_raw(site, vault, 9, "page")


def test_raw_unknown_section(tmp_path):
    site = build_site(tmp_path)
    with pytest.raises(ValueError, match="section 13"):
        make_raw(site, tmp_path / "vault", 13, "page")
```

- [x] **Step 2: Run to verify failure**

Run: `uv run --directory docs-arc42-brain/_system/generate pytest tests/test_raw.py -q`
Expected: FAIL, `ModuleNotFoundError: No module named 'braingen.raw'`

- [x] **Step 3: Implement `raw.py`**

```python
"""Copy one arc42 section's current site files into a raw/ batch for ingest.

A batch is a folder raw/section-<N>-<what>/ with a manifest.yaml. Nothing in
the site is modified; the batch is the immutable provenance the importer
reads. `what` is "page" (the section page only), "content" (its tips and
examples) or "all".
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

import frontmatter
import yaml

WHAT = ("all", "page", "content")
EXAMPLE_INCLUDE_RE = re.compile(r'{%\s*include example\.md\s+category="([^"]+)"\s*%}')
SECTION_IMAGE_RE = re.compile(r"(?:\{\{\s*site\.imageurl\s*\}\}|/assets/images/sections)/([^)\s\"']+)")
EXAMPLE_IMAGE_RE = re.compile(r"(?:\{\{\s*site\.exampleimages\s*\}\}|/assets/images/examples)/([^)\s\"']+)")


def _section_meta(site: Path, section: int) -> dict:
    entries = yaml.safe_load((site / "_data" / "sections.yml").read_text(encoding="utf-8"))
    for e in entries:
        if int(e["number"]) == section:
            return e
    raise ValueError(f"section {section} not in _data/sections.yml")


def _posts_dir(site: Path, section: int) -> str:
    prefix = f"{section:02d}-"
    for d in sorted((site / "_posts").iterdir()):
        if d.is_dir() and d.name.startswith(prefix):
            return d.name
    raise ValueError(f"no _posts/{prefix}* directory for section {section}")


def _copy(src: Path, dst: Path, files: list[str], batch: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    files.append(str(dst.relative_to(batch)))


def make_raw(site: Path, vault: Path, section: int, what: str = "all") -> Path:
    if what not in WHAT:
        raise ValueError(f"what must be one of {WHAT}, got {what!r}")
    site, vault = Path(site), Path(vault)
    meta = _section_meta(site, section)
    batch = vault / "raw" / f"section-{section}-{what}"
    if batch.exists():
        raise FileExistsError(f"{batch} exists; archive it under raw/ingested/ or remove it first")

    page_path = site / "_pages" / f"section-{section}.md"
    page = frontmatter.load(page_path)
    example_categories = EXAMPLE_INCLUDE_RE.findall(page.content)
    files: list[str] = []
    texts: list[str] = []

    if what in ("all", "page"):
        _copy(page_path, batch / "pages" / page_path.name, files, batch)
        texts.append(page_path.read_text(encoding="utf-8"))

    posts_dir = _posts_dir(site, section)
    if what in ("all", "content"):
        for p in sorted((site / "_posts" / posts_dir).glob("*.md")):
            _copy(p, batch / "posts" / p.name, files, batch)
            texts.append(p.read_text(encoding="utf-8"))
        for e in sorted((site / "_examples").glob("*.md")):
            cat = frontmatter.load(e).get("category")
            if cat in example_categories:
                _copy(e, batch / "examples" / e.name, files, batch)
                texts.append(e.read_text(encoding="utf-8"))

    joined = "\n".join(texts)
    for rel in sorted(set(SECTION_IMAGE_RE.findall(joined))):
        _copy(site / "assets/images/sections" / rel, batch / "assets/sections" / rel, files, batch)
    for rel in sorted(set(EXAMPLE_IMAGE_RE.findall(joined))):
        _copy(site / "assets/images/examples" / rel, batch / "assets/examples" / rel, files, batch)

    manifest = {
        "section": section,
        "what": what,
        "name": meta["name"],
        "category": meta["category"],
        "permalink": meta["permalink"],
        "posts_dir": posts_dir,
        "order": page.get("order"),
        "title": page.get("title"),
        "example_categories": example_categories,
        "files": files,
    }
    batch.mkdir(parents=True, exist_ok=True)
    (batch / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return batch
```

- [x] **Step 4: Add the `raw` subcommand to `cli.py`**

Add to `cli.py` after `cmd_lint`:

```python
def cmd_raw(args: argparse.Namespace) -> int:
    from .raw import make_raw

    batch = make_raw(args.site, args.vault, args.section, args.what)
    print(f"raw batch written: {batch}")
    return 0
```

And inside `build_parser()` before `return ap`:

```python
    r = sub.add_parser("raw", help="copy a section's site files into a raw/ batch")
    r.add_argument("--site", type=Path, required=True)
    r.add_argument("--vault", type=Path, required=True)
    r.add_argument("--section", type=int, required=True)
    r.add_argument("--what", choices=["all", "page", "content"], default="all")
    r.set_defaults(func=cmd_raw)
```

- [x] **Step 5: Run the tests**

Run: `uv run --directory docs-arc42-brain/_system/generate pytest tests/test_raw.py -q`
Expected: `4 passed`

- [x] **Step 6: Add the `brain-raw` target**

Append to `brain.mk` (add `brain-raw` to `.PHONY`):

```make
SECTION ?=
WHAT ?= all

brain-raw: ## Copy one section's site files into raw/ (SECTION=9 WHAT=all|page|content)
	@test -n "$(SECTION)" || { echo "usage: make brain-raw SECTION=9 [WHAT=all|page|content]"; exit 2; }
	$(BRAINGEN) raw --site $(CURDIR) --vault $(BRAIN_DIR) --section $(SECTION) --what $(WHAT)
```

Run: `make brain-raw SECTION=9 WHAT=page && ls docs-arc42-brain/raw/section-9-page && rm -r docs-arc42-brain/raw/section-9-page`
Expected: `manifest.yaml pages` listed; the batch is removed again (Task 8 does the real run).

- [x] **Step 7: Commit**

```bash
git add docs-arc42-brain/_system
git commit -m "brain: braingen raw copies a section's site files into a raw batch

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 6: `braingen import` — convert a raw batch into draft wiki pages

**Files:**
- Create: `docs-arc42-brain/_system/generate/braingen/importer.py`
- Modify: `docs-arc42-brain/_system/generate/braingen/cli.py` (add `import` subcommand)
- Modify: `docs-arc42-brain/_system/brain.mk` (add `brain-import`)
- Test: `docs-arc42-brain/_system/generate/tests/test_importer.py`

**Interfaces:**
- Consumes: batch layout and `manifest.yaml` from Task 5; `load_vault`/`lint` for the end-to-end test.
- Produces: `import_batch(vault: Path, batch_name: str, today: str) -> ImportReport` with `ImportReport(source_slug: str, written: list[Path])`. Writes draft pages into `wiki/`, copies `assets/**` to `wiki/assets/**`, and writes `raw/sources/SRC-NNN-<batch>.md`. Pure conversion functions are exposed for tests: `convert_section(text, manifest, today, source_slug) -> (meta, body)`, `convert_tip(filename, text, manifest, today, source_slug)`, `convert_example(filename, text, manifest, today, source_slug)`, `write_page(path, meta, body)`, `next_source_id(vault) -> int`.

Conversion rules (spec §4.3, §4.4):

| Site | Brain |
|---|---|
| `<div class="arc42-help" markdown="1">` … `</div>` | `> [!arc42-help]` callout; every inner line prefixed `> ` (empty lines become `>`) |
| `{% include example.md category="X" %}` | `%% examples: X %%` |
| `{% include examples-link.html variant="inline" %}` | `%% examples-link %%` |
| `{% include further-info.md … topic="T" … %}` (multi-line) | removed; `T` → frontmatter `faq-topic` |
| `{{ site.imageurl }}/P` and `/assets/images/sections/P` | `../assets/sections/P` |
| `{{ site.exampleimages }}/P` and `/assets/images/examples/P` | `../assets/examples/P` |
| tip `tags: a b c` (string or list) | `legacy-tags: [a, b, c]`, `keywords: []`, `terms: []` |
| tip filename `YYYY-MM-DD-t-N-M.md` | `id: N-M`, `date: YYYY-MM-DD`, file `wiki/tips/tip-N-M.md` |
| tip/example `category` | `section: "[[section-N]]"` |
| example `category` | `example-category` |
| example filename token `htmlsc`, `hsc`, `tpu`, `mama`, `status` | `system: "[[htmlsc]]"` (hsc maps to htmlsc), `[[tpu]]`, `[[mama]]`, `[[status]]`; else `""` |

Frontmatter key order matters for humans reading the vault; the emitter writes keys in the order given below and never sorts.

- [x] **Step 1: Write the failing importer tests**

Create `tests/test_importer.py`:

```python
from pathlib import Path

import frontmatter
import pytest

from braingen.importer import (
    convert_example,
    convert_section,
    convert_tip,
    import_batch,
    next_source_id,
    write_page,
)
from braingen.lint import lint
from braingen.parse import load_vault
from braingen.raw import make_raw
from tests.test_raw import EXAMPLE, PAGE, TIP, build_site

TODAY = "2026-09-17"
MANIFEST = {
    "section": 9, "what": "all", "name": "Architecture Decisions", "category": "decisions",
    "permalink": "/section-9/", "posts_dir": "09-decisions", "order": 13,
    "title": "9 - Architecture decisions", "example_categories": ["decisions"], "files": [],
}


def test_convert_section_callouts_directives_images_and_foot():
    meta, body = convert_section(PAGE, MANIFEST, TODAY, "SRC-001-section-9-all")
    assert list(meta) == ["id", "type", "title", "status", "created", "updated", "sources", "related",
                          "number", "name", "category", "posts-dir", "permalink", "order", "faq-topic"]
    assert meta["id"] == "section-9" and meta["type"] == "section" and meta["status"] == "draft"
    assert meta["sources"] == ["[[SRC-001-section-9-all]]"]
    assert meta["faq-topic"] == "fundamental architecture and design decisions"
    assert meta["posts-dir"] == "09-decisions" and meta["order"] == 13
    assert "> [!arc42-help]\n>\n> ## Content\n> Important decisions.\n" in body
    assert "> ![flow](../assets/sections/09/flow.png)" in body
    assert "> %% examples: decisions %%" in body
    assert "\n%% examples-link %%\n" in body
    assert "further-info" not in body and "{%" not in body and "{{" not in body
    assert "<div" not in body and "</div>" not in body


def test_convert_tip_maps_frontmatter_and_legacy_tags():
    meta, body = convert_tip("2016-03-01-t-9-1.md", TIP, MANIFEST, TODAY, "SRC-001-x")
    assert list(meta) == ["id", "type", "title", "status", "created", "updated", "sources", "related",
                          "section", "keywords", "terms", "legacy-tags", "date", "permalink"]
    assert meta["id"] == "9-1" and meta["date"] == "2016-03-01"
    assert meta["section"] == "[[section-9]]"
    assert meta["legacy-tags"] == ["decision", "quality", "stakeholder", "lean"]
    assert meta["keywords"] == [] and meta["terms"] == []
    assert meta["permalink"] == "/tips/9-1/"
    assert body.strip() == "Body of the tip."


def test_convert_tip_accepts_list_tags():
    text = TIP.replace("tags: decision quality stakeholder lean", "tags: [decision, lean]")
    meta, _ = convert_tip("2016-03-01-t-9-1.md", text, MANIFEST, TODAY, "SRC-001-x")
    assert meta["legacy-tags"] == ["decision", "lean"]


def test_convert_example_maps_category_system_and_images():
    meta, body = convert_example("09-decision-example-adr.md", EXAMPLE, MANIFEST, TODAY, "SRC-001-x")
    assert meta["id"] == "09-decision-example-adr" and meta["type"] == "example"
    assert meta["example-category"] == "decisions" and meta["system"] == ""
    assert meta["legacy-tags"] == ["decision", "example"]
    assert "![table](../assets/examples/adr-table.png)" in body
    meta2, _ = convert_example("05-buildingblock-example-hsc.md", EXAMPLE, MANIFEST, TODAY, "SRC-001-x")
    assert meta2["system"] == "[[htmlsc]]"
    meta3, _ = convert_example("07-deployment-example-tpu-1.md", EXAMPLE, MANIFEST, TODAY, "SRC-001-x")
    assert meta3["system"] == "[[tpu]]"


def test_write_page_quotes_wikilinks_and_keeps_order(tmp_path):
    p = tmp_path / "x.md"
    write_page(p, {"id": "a", "related": ["[[b]]"], "z": 1, "a": 2}, "body\n")
    text = p.read_text()
    assert text.startswith("---\nid: a\nrelated:\n- '[[b]]'\nz: 1\na: 2\n---\n\nbody\n")
    assert frontmatter.loads(text)["related"] == ["[[b]]"]


def test_next_source_id(tmp_path):
    (tmp_path / "raw/sources").mkdir(parents=True)
    assert next_source_id(tmp_path) == 1
    (tmp_path / "raw/sources/SRC-007-foo.md").write_text("---\nid: SRC-007\n---\n")
    assert next_source_id(tmp_path) == 8


def test_import_batch_end_to_end_lints_clean(tmp_path):
    site = build_site(tmp_path)
    vault = tmp_path / "vault"
    make_raw(site, vault, 9, "all")
    report = import_batch(vault, "section-9-all", TODAY)
    assert report.source_slug == "SRC-001-section-9-all"
    assert (vault / "wiki/sections/section-9.md").exists()
    assert (vault / "wiki/tips/tip-9-1.md").exists()
    assert (vault / "wiki/examples/09-decision-example-adr.md").exists()
    assert (vault / "wiki/assets/sections/09/flow.png").read_bytes() == b"png"
    assert (vault / "wiki/assets/examples/adr-table.png").read_bytes() == b"png"
    src = frontmatter.load(vault / "raw/sources/SRC-001-section-9-all.md")
    assert src["origin"] == "raw/section-9-all/"
    paths = [f["path"] for f in src["files"]]
    assert "pages/section-9.md" in paths and all(len(f["sha256"]) == 64 for f in src["files"])
    assert set(src["ingested-pages"]) == {"[[section-9]]", "[[tip-9-1]]", "[[09-decision-example-adr]]"}
    findings = lint(load_vault(vault))
    assert [str(f) for f in findings if f.level == "error"] == []


def test_import_batch_refuses_to_overwrite_existing_page(tmp_path):
    site = build_site(tmp_path)
    vault = tmp_path / "vault"
    make_raw(site, vault, 9, "page")
    import_batch(vault, "section-9-page", TODAY)
    make_raw(site, vault, 9, "all")
    with pytest.raises(FileExistsError, match="section-9.md"):
        import_batch(vault, "section-9-all", TODAY)
```

Add an empty `tests/__init__.py` so `from tests.test_raw import …` works:

```bash
touch docs-arc42-brain/_system/generate/tests/__init__.py
```

- [x] **Step 2: Run to verify failure**

Run: `uv run --directory docs-arc42-brain/_system/generate pytest tests/test_importer.py -q`
Expected: FAIL, `ModuleNotFoundError: No module named 'braingen.importer'`

- [x] **Step 3: Implement `importer.py`**

```python
"""Convert a raw/ batch (see raw.py) into draft wiki pages plus a source record.

Mechanical only: frontmatter mapping, callouts, directives, image paths. The
judgement work (mapping legacy tags to keywords/terms, related links, issues)
is the ingest session's, see _system/workflows/ingest.md.
"""
from __future__ import annotations

import hashlib
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import frontmatter
import yaml

HELP_OPEN = '<div class="arc42-help"'
HELP_CLOSE = "</div>"
EXAMPLE_INCLUDE_RE = re.compile(r'^\s*{%\s*include example\.md\s+category="([^"]+)"\s*%}\s*$')
EXAMPLES_LINK_RE = re.compile(r'^\s*{%\s*include examples-link\.html\s+variant="inline"\s*%}\s*$')
FURTHER_INFO_START = "{% include further-info.md"
TOPIC_RE = re.compile(r'topic="([^"]*)"')
TIP_FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-t-(\d+)-(\d+)\.md$")
SYSTEM_TOKENS = {"htmlsc": "htmlsc", "hsc": "htmlsc", "tpu": "tpu", "mama": "mama", "status": "status"}

IMAGE_REWRITES = [
    (re.compile(r"\{\{\s*site\.imageurl\s*\}\}/"), "../assets/sections/"),
    (re.compile(r"/assets/images/sections/"), "../assets/sections/"),
    (re.compile(r"\{\{\s*site\.exampleimages\s*\}\}/"), "../assets/examples/"),
    (re.compile(r"/assets/images/examples/"), "../assets/examples/"),
]


def rewrite_images(text: str) -> str:
    for rx, repl in IMAGE_REWRITES:
        text = rx.sub(repl, text)
    return text


def _common(id_: str, type_: str, title: str, today: str, source_slug: str) -> dict:
    return {
        "id": id_,
        "type": type_,
        "title": title,
        "status": "draft",
        "created": today,
        "updated": today,
        "sources": [f"[[{source_slug}]]"],
        "related": [],
    }


def _split_tags(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [t for t in value.replace(",", " ").split() if t]
    return [str(t).strip() for t in value if str(t).strip()]


def convert_section(text: str, manifest: dict, today: str, source_slug: str) -> tuple[dict, str]:
    post = frontmatter.loads(text)
    out: list[str] = []
    in_help = False
    faq_topic = ""
    lines = post.content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith(HELP_OPEN):
            in_help = True
            out.append("> [!arc42-help]")
            i += 1
            continue
        if in_help and stripped == HELP_CLOSE:
            in_help = False
            i += 1
            continue
        if stripped.startswith(FURTHER_INFO_START):
            block = line
            while "%}" not in block and i + 1 < len(lines):
                i += 1
                block += "\n" + lines[i]
            m = TOPIC_RE.search(block)
            faq_topic = m.group(1) if m else ""
            i += 1
            continue
        m = EXAMPLE_INCLUDE_RE.match(line)
        if m:
            line = f"%% examples: {m.group(1)} %%"
        elif EXAMPLES_LINK_RE.match(line):
            line = "%% examples-link %%"
        line = rewrite_images(line)
        if in_help:
            line = f"> {line}" if line.strip() else ">"
        out.append(line)
        i += 1
    body = "\n".join(out).rstrip("\n") + "\n"
    n = int(manifest["section"])
    meta = _common(f"section-{n}", "section", str(post.get("title", manifest.get("title"))), today, source_slug)
    meta.update({
        "number": n,
        "name": manifest["name"],
        "category": manifest["category"],
        "posts-dir": manifest["posts_dir"],
        "permalink": manifest["permalink"],
        "order": manifest.get("order"),
        "faq-topic": faq_topic,
    })
    return meta, body


def convert_tip(filename: str, text: str, manifest: dict, today: str, source_slug: str) -> tuple[dict, str]:
    m = TIP_FILENAME_RE.match(filename)
    if not m:
        raise ValueError(f"tip filename {filename!r} does not match YYYY-MM-DD-t-N-M.md")
    date, n, k = m.group(1), m.group(2), m.group(3)
    post = frontmatter.loads(text)
    meta = _common(f"{n}-{k}", "tip", str(post.get("title", "")), today, source_slug)
    meta.update({
        "section": f"[[section-{int(manifest['section'])}]]",
        "keywords": [],
        "terms": [],
        "legacy-tags": _split_tags(post.get("tags")),
        "date": date,
        "permalink": str(post.get("permalink", f"/tips/{n}-{k}/")),
    })
    return meta, rewrite_images(post.content).rstrip("\n") + "\n"


def _system_for(stem: str) -> str:
    for token in stem.split("-"):
        if token in SYSTEM_TOKENS:
            return f"[[{SYSTEM_TOKENS[token]}]]"
    return ""


def convert_example(filename: str, text: str, manifest: dict, today: str, source_slug: str) -> tuple[dict, str]:
    stem = filename[:-3] if filename.endswith(".md") else filename
    post = frontmatter.loads(text)
    meta = _common(stem, "example", str(post.get("title", "")), today, source_slug)
    meta.update({
        "section": f"[[section-{int(manifest['section'])}]]",
        "system": _system_for(stem),
        "example-category": str(post.get("category", "")),
        "keywords": [],
        "terms": [],
        "legacy-tags": _split_tags(post.get("tags")),
        "permalink": str(post.get("permalink", "")),
    })
    return meta, rewrite_images(post.content).rstrip("\n") + "\n"


def write_page(path: Path, meta: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fm = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, default_flow_style=False)
    path.write_text(f"---\n{fm}---\n\n{body}", encoding="utf-8")


def next_source_id(vault: Path) -> int:
    best = 0
    for p in (Path(vault) / "raw" / "sources").glob("SRC-*.md"):
        m = re.match(r"SRC-(\d+)", p.name)
        if m:
            best = max(best, int(m.group(1)))
    return best + 1


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class ImportReport:
    source_slug: str
    written: list[Path] = field(default_factory=list)


def import_batch(vault: Path, batch_name: str, today: str) -> ImportReport:
    vault = Path(vault)
    batch = vault / "raw" / batch_name
    manifest = yaml.safe_load((batch / "manifest.yaml").read_text(encoding="utf-8"))
    source_slug = f"SRC-{next_source_id(vault):03d}-{batch_name}"
    report = ImportReport(source_slug)

    planned: list[tuple[Path, dict, str]] = []
    page_file = batch / "pages" / f"section-{manifest['section']}.md"
    if page_file.exists():
        meta, body = convert_section(page_file.read_text(encoding="utf-8"), manifest, today, source_slug)
        planned.append((vault / "wiki/sections" / f"{meta['id']}.md", meta, body))
    for p in sorted((batch / "posts").glob("*.md")) if (batch / "posts").is_dir() else []:
        meta, body = convert_tip(p.name, p.read_text(encoding="utf-8"), manifest, today, source_slug)
        planned.append((vault / "wiki/tips" / f"tip-{meta['id']}.md", meta, body))
    for p in sorted((batch / "examples").glob("*.md")) if (batch / "examples").is_dir() else []:
        meta, body = convert_example(p.name, p.read_text(encoding="utf-8"), manifest, today, source_slug)
        planned.append((vault / "wiki/examples" / f"{meta['id']}.md", meta, body))

    for path, _, _ in planned:
        if path.exists():
            raise FileExistsError(f"{path.relative_to(vault)} already exists; the vault owns it now")

    for path, meta, body in planned:
        write_page(path, meta, body)
        report.written.append(path)

    assets = batch / "assets"
    if assets.is_dir():
        for src in sorted(assets.rglob("*")):
            if src.is_file():
                dst = vault / "wiki/assets" / src.relative_to(assets)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

    files = [
        {"path": rel, "sha256": _sha256(batch / rel)}
        for rel in manifest.get("files", [])
        if (batch / rel).is_file()
    ]
    src_meta = {
        "id": source_slug.split("-section-")[0] if "-section-" in source_slug else source_slug[:7],
        "type": "source",
        "title": f"Site files of section {manifest['section']} ({manifest['what']})",
        "status": "ingested",
        "created": today,
        "updated": today,
        "source-type": "repository",
        "origin": f"raw/{batch_name}/",
        "captured": today,
        "files": files,
        "ingested-pages": [f"[[{p.stem}]]" for p in report.written],
    }
    src_path = vault / "raw/sources" / f"{source_slug}.md"
    write_page(src_path, src_meta, f"Copied from docs.arc42.org-site on {today} by `braingen raw`; converted by `braingen import`.\n")
    report.written.append(src_path)
    return report
```

The `id` of the source record must be `SRC-NNN`; with `source_slug = "SRC-001-section-9-all"` the expression `source_slug.split("-section-")[0]` gives `SRC-001`. Keep the batch naming `section-N-<what>` so this holds.

- [x] **Step 4: Add the `import` subcommand to `cli.py`**

```python
def cmd_import(args: argparse.Namespace) -> int:
    from datetime import date

    from .importer import import_batch

    report = import_batch(args.vault, args.batch, args.today or date.today().isoformat())
    for p in report.written:
        print(f"wrote {p.relative_to(args.vault)}")
    print(f"source record: {report.source_slug}")
    return 0
```

In `build_parser()`:

```python
    i = sub.add_parser("import", help="convert a raw batch into draft wiki pages")
    i.add_argument("--vault", type=Path, required=True)
    i.add_argument("--batch", required=True, help="batch folder name under raw/, e.g. section-9-all")
    i.add_argument("--today", default=None, help="override the date written into created/updated")
    i.set_defaults(func=cmd_import)
```

- [x] **Step 5: Run all tests**

Run: `make brain-test`
Expected: `40 passed` (1 smoke + 6 wikilinks + 6 anchors + 5 parse + 10 lint + 4 raw + 8 importer). If the count differs, every file must still report 0 failures.

- [x] **Step 6: Add the `brain-import` target**

Append to `brain.mk` (add `brain-import` to `.PHONY`):

```make
BATCH ?=

brain-import: ## Convert a raw batch into draft wiki pages (BATCH=section-9-all)
	@test -n "$(BATCH)" || { echo "usage: make brain-import BATCH=section-9-all"; exit 2; }
	$(BRAINGEN) import --vault $(BRAIN_DIR) --batch $(BATCH)
```

- [x] **Step 7: Commit**

```bash
git add docs-arc42-brain/_system
git commit -m "brain: braingen import converts a raw batch into draft wiki pages

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 7: Schema documents: CLAUDE.md, README, templates, ADRs, workflows, index, log

**Files:**
- Create: `docs-arc42-brain/CLAUDE.md`, `docs-arc42-brain/README.md`
- Create: `docs-arc42-brain/_templates/{section,tip,example,faq,term,keyword,system,issue,source}.md`
- Create: `docs-arc42-brain/_system/adr/0000-template.md`, `0001-record-architecture-decisions.md`, `0002-content-types-and-natural-ids.md`, `0003-two-vocabularies.md`, `0004-explicit-related-links.md`, `0005-no-liquid-callouts-and-directives.md`
- Create: `docs-arc42-brain/_system/workflows/{bootstrap,ingest,audit,relations,cutover}.md`
- Create: `docs-arc42-brain/_system/index.md`, `docs-arc42-brain/_system/log.md`

No code in this task; the deliverable is reviewed for consistency with the lint (Task 4) and the spec. Templates live outside `wiki/`, so the lint never reads them.

- [x] **Step 1: Write `CLAUDE.md`**

```markdown
# docs-arc42-brain — agent schema

You maintain the **second brain of docs.arc42.org**: every content page of the
site (sections with their guidance, tips, examples, later FAQ answers) lives
here as a typed, interlinked wiki page. A generator (`_system/generate/`,
phase 2) turns `wiki/` into the Jekyll input of the site one directory up.
Layouts, includes, styling and navigation stay in Jekyll; the brain owns
content only.

Design spec: `../docs/superpowers/specs/2026-09-17-docs-arc42-brain-design.md`.

## Three layers (Karpathy LLM-wiki pattern)

1. **`raw/`** — human-owned, immutable. Top level is the inbox of not-yet-ingested
   batches (`raw/section-9-all/`, written by `make brain-raw`). After ingest a
   batch moves to `raw/ingested/`. `raw/sources/` holds the `SRC-NNN` provenance
   records you write. Never edit a raw file.
2. **`wiki/`** — agent-owned content, one typed page per file, Obsidian wikilinks.
3. **Schema** — this file, `_templates/`, `_system/adr/`. Changing the schema
   needs an ADR.

## Content types

| Type | Folder | Slug (= filename stem) | Notes |
|---|---|---|---|
| section | `wiki/sections/` | `section-N` | one page per arc42 section, guidance as `> [!arc42-help]` callouts |
| tip | `wiki/tips/` | `tip-N-M` | `id: N-M`; `permalink` is a public URL and never changes |
| example | `wiki/examples/` | legacy filename stem | `example-category` is the legacy Jekyll category |
| faq | `wiki/faq/` | `faq-a-13` | phase 4 |
| term | `wiki/terms/` | kebab slug | arc42 vocabulary: definition, `aliases`, `legacy-tags`, `home` section |
| keyword | `wiki/keywords/` | kebab slug | small controlled navigation facets (`lean`, `essential`, `thorough`, …) |
| system | `wiki/systems/` | `htmlsc`, `tpu`, `mama`, `status` | the example systems |
| issue | `wiki/issues/` | `ISS-NNN-kebab` | open question, contradiction, gap, ambiguity, risk |
| source | `raw/sources/` | `SRC-NNN-<batch>` | provenance record |

Required fields per type are enforced by `make brain-lint`; the templates in
`_templates/` are the contract. Do not invent fields.

## Conventions

- **Language**: English.
- **Wikilinks**: `[[slug]]`, `[[slug#Heading text]]`, `[[slug|label]]`. In YAML
  always quoted: `related: ["[[tip-9-2]]"]`. Every cross-reference is a link;
  no bare prose references.
- **Links to subsections** use the heading text exactly as written on the
  target page: `[[section-5#5.1 Whitebox Overall System]]`. Only headings that
  are unique on their page are valid targets; `Content`, `Motivation`, `Form`
  are not.
- **Vocabulary**: a tip references `keywords:` (facets) and `terms:` (arc42
  concepts). Legacy site tags arrive in `legacy-tags:` from the importer and
  must be emptied by mapping each one to a keyword or a term before the page
  leaves `draft`. Create the term or keyword page if it does not exist; when a
  tag is ambiguous, raise an issue instead of guessing.
- **`related:`** is the only source of "see also" links on the site. Add links
  deliberately, at both ends where it makes sense. Links to sections need no
  backlink.
- **No Liquid** anywhere in `wiki/`. Images are vault-relative
  (`../assets/sections/09/x.png`). Directives are Obsidian comments:
  `%% examples: <category> %%`, `%% examples-link %%`.
- **Status**: `draft → review → published → retired`. Only `published` pages
  reach the site. Issues: `open → in-progress → resolved | wontfix`.
- **Provenance**: every page derived from a source links it in `sources:`.
- **Contradictions and doubts become issues**, never silent edits.
- **Dates** absolute, `YYYY-MM-DD`.

## Workflows (`_system/workflows/`)

| When | Read |
|---|---|
| empty vault | `bootstrap.md` |
| a batch appears in `raw/` | `ingest.md` |
| a section is fully ingested | `cutover.md` (phase 2) |
| on request | `audit.md`, `relations.md` |

Every run appends one entry to `_system/log.md` and updates `_system/index.md`.

## Commands

```
make brain-lint                      validate the vault (must pass before every commit)
make brain-raw SECTION=9 WHAT=all    copy site files into raw/section-9-all/
make brain-import BATCH=section-9-all  convert the batch into draft pages
make brain-test                      unit tests of the tooling
```
```

- [x] **Step 2: Write `README.md`**

```markdown
# docs-arc42-brain

The content of docs.arc42.org as a Karpathy-style LLM wiki: `raw/` holds
immutable sources, `wiki/` holds typed, interlinked pages, and the schema
(`CLAUDE.md`, `_templates/`, `_system/adr/`) evolves with the content.

Open this folder in Obsidian as a vault to browse and graph it. Point Claude
Code at it and it reads `CLAUDE.md`. All make targets run from the repo root:
`make help` lists the `brain-*` ones.

Design: `../docs/superpowers/specs/2026-09-17-docs-arc42-brain-design.md`.
```

- [x] **Step 3: Write the nine templates**

`_templates/section.md`:

```markdown
---
id: section-N
type: section
title: N - <Section title as on the site>
status: draft
created: {{date}}
updated: {{date}}
sources: []
related: []
number: N
name: <Short nav name from _data/sections.yml>
category: <legacy tip category, e.g. decisions>
posts-dir: <legacy _posts folder, e.g. 09-decisions>
permalink: /section-N/
order: <nav order from the page front matter>
faq-topic: <phrase used in "questions related to …">
---

# N. <Title>

> [!arc42-help]
> ## Content
> …
> ## Motivation
> …
> ## Form
> …
> %% examples: <example-category> %%

%% examples-link %%

## N.1 <Subsection>
```

`_templates/tip.md`:

```markdown
---
id: N-M
type: tip
title: "Tip N-M: <Imperative sentence!>"
status: draft
created: {{date}}
updated: {{date}}
sources: []
related: []
section: "[[section-N]]"          # may carry a heading: "[[section-5#5.1 Whitebox Overall System]]"
keywords: []                      # ["[[lean]]"] …
terms: []                         # ["[[decision]]"] …
legacy-tags: []                   # filled by the importer; must be empty before status leaves draft
date: YYYY-MM-DD                  # legacy post date; keeps the site's list order
permalink: /tips/N-M/
---

<Body. Markdown only. Images: ../assets/sections/NN/name.png>
```

`_templates/example.md`:

```markdown
---
id: <legacy filename stem, e.g. 09-decision-example-adr>
type: example
title: "Example <Section>: <Name>"
status: draft
created: {{date}}
updated: {{date}}
sources: []
related: []
section: "[[section-N]]"
system: "[[htmlsc]]"              # or "" when the example is not from one of the sample systems
example-category: <legacy category, e.g. decisions>
keywords: []
terms: []
legacy-tags: []
permalink: /examples/<slug>/
---

<Body. Images: ../assets/examples/name.png>
```

`_templates/faq.md`:

```markdown
---
id: A-13
type: faq
title: "Question A-13: <question>"
status: draft
created: {{date}}
updated: {{date}}
sources: []
related: []
question: <the question in one line>
section: ""                       # "[[section-N]]" when the answer belongs to a section
keywords: []
terms: []
legacy-tags: []
legacy-permalink: /questions/A-13/
legacy-category: general
---

<Answer.>
```

`_templates/term.md`:

```markdown
---
id: <kebab-slug>
type: term
title: <Term>
status: draft
created: {{date}}
updated: {{date}}
sources: []
related: []
term: <Display form, e.g. Building block>
aliases: []                       # synonyms; Obsidian resolves links through them
legacy-tags: []                   # old site tags that mean this term, e.g. [scenario, quality-scenario]
home: "[[section-N]]"             # where arc42 introduces the concept
---

**Definition.** <One sentence.>

**In arc42.** <Where it appears, how it is used.>

**Distinguish from.** <[[other-term]] and how it differs.>
```

`_templates/keyword.md`:

```markdown
---
id: <kebab-slug>
type: keyword
title: <keyword>
status: draft
created: {{date}}
updated: {{date}}
sources: []
related: []
description: <One line: what this facet means for the reader>
featured: false                   # true for lean / essential / thorough
---

<Optional longer explanation.>
```

`_templates/system.md`:

```markdown
---
id: <slug>
type: system
title: <System name>
status: draft
created: {{date}}
updated: {{date}}
sources: []
related: []
name: <Full name, e.g. HTML Sanity Checker>
url: ""                           # its page on examples.arc42.org, if any
aliases: []
---

<One paragraph: what the system is and why it serves as an example.>
```

`_templates/issue.md`:

```markdown
---
id: ISS-NNN
type: issue
title: <The open point, in one line>
status: open                      # open | in-progress | resolved | wontfix
created: {{date}}
updated: {{date}}
sources: []
related: []                       # every page this issue affects
severity: minor                   # blocker | major | minor
kind: question                    # question | contradiction | gap | ambiguity | risk
raised-by: agent
resolved: null
---

**What's unresolved.** <Precise statement.>

**Affects.** <[[…]] pages.>

**Evidence.** <Quotes or links, both sides if a contradiction.>

**Options.**
1. <option> — <implication>
2. <option> — <implication>

**Resolution.** <Filled in when closed.>
```

`_templates/source.md`:

```markdown
---
id: SRC-NNN
type: source
title: <What was ingested>
status: ingested
created: {{date}}
updated: {{date}}
source-type: repository           # repository | document | url | maintainer
origin: raw/<batch>/              # updated to raw/ingested/<batch>/ after archiving
captured: {{date}}
files: []                         # [{path: …, sha256: …}]
ingested-pages: []                # ["[[section-9]]", …]
---

<One line. Narrative belongs in _system/log.md.>
```

- [x] **Step 4: Write the ADRs**

`_system/adr/0000-template.md`:

```markdown
# ADR-NNNN: <Title>

- **Status:** proposed | accepted | superseded by ADR-XXXX
- **Date:** YYYY-MM-DD

## Context
## Decision
## Consequences
```

`_system/adr/0001-record-architecture-decisions.md`:

```markdown
# ADR-0001: Record decisions about the brain as ADRs

- **Status:** accepted
- **Date:** 2026-09-17

## Context
The brain's structure (types, fields, conventions, tooling) will change as content is ingested. Decisions about arc42 content itself belong on the site; decisions about the brain need a home too.

## Decision
We record every decision about the brain's own structure as an ADR in `_system/adr/`, numbered, one line each in `_system/index.md`. ADRs are English, terse, and never rewritten; a change is a new ADR that supersedes.

## Consequences
Schema changes are traceable. Agents must read the ADRs before proposing a new field or folder.
```

`_system/adr/0002-content-types-and-natural-ids.md`:

```markdown
# ADR-0002: Nine content types with natural IDs

- **Status:** accepted
- **Date:** 2026-09-17

## Context
docs.arc42.org URLs are cited externally and must not change. The site already has natural identifiers: tip `9-1`, example filename stems, section numbers, FAQ `A-13`.

## Decision
Types: section, tip, example, faq, term, keyword, system, issue, source. IDs are the natural ones; filenames derive from them (`tip-9-1.md`, `section-9.md`, `<example-stem>.md`, `faq-a-13.md`). Wikilinks resolve by filename stem, which is unique across the vault. `permalink` is stored on every page that has a public URL and is never derived.

## Consequences
No ID registry is needed. Renaming a page is forbidden; retiring it is `status: retired`.
```

`_system/adr/0003-two-vocabularies.md`:

```markdown
# ADR-0003: Terms and keywords are separate vocabularies

- **Status:** accepted
- **Date:** 2026-09-17

## Context
The site's flat tag list mixes reading facets (`lean`, `essential`, `thorough`) with arc42 concepts (`building-block`, `quality-scenario`) and contains near-duplicates.

## Decision
`wiki/terms/` holds arc42 concepts with a definition, aliases, `legacy-tags` and a home section. `wiki/keywords/` holds a small controlled list of navigation facets. Tips, examples and FAQ answers reference both. The importer parks old tags in `legacy-tags`; a page may not leave `draft` until that list is empty. Consolidating tags may change tag names on the site's keyword page; page URLs never change.

## Consequences
The keyword page is generated from the union. Tag cleanup is an explicit, reviewable act per page.
```

`_system/adr/0004-explicit-related-links.md`:

```markdown
# ADR-0004: The site renders only explicit related links

- **Status:** accepted
- **Date:** 2026-09-17

## Context
Links between tips, examples, sections and terms are the main value of the brain. Computed similarity is cheap but noisy and makes the site change when a tag changes.

## Decision
`related:` on a page is the only source of "see also" links on the generated site. Link targets may be any page, and sections may be addressed by heading (`[[section-5#5.1 Whitebox Overall System]]`); only headings unique on their page are valid targets. The generator computes candidate links from shared terms and keywords and shows them in the dashboard only; a human or an ingest session promotes them. Links to sections need no backlink; other unreciprocated links are lint warnings.

## Consequences
The site is deterministic and reviewable in git. Discovery is a dashboard job.
```

`_system/adr/0005-no-liquid-callouts-and-directives.md`:

```markdown
# ADR-0005: No Liquid in the brain; callouts and directives instead

- **Status:** accepted
- **Date:** 2026-09-17

## Context
Section pages today mix markdown with Jekyll includes and `<div class="arc42-help">` blocks. Obsidian renders neither.

## Decision
`wiki/` contains no Liquid. Guidance is an Obsidian callout `> [!arc42-help]`. The example list is the directive `%% examples: <category> %%`; the pointer to examples.arc42.org is `%% examples-link %%`; both are Obsidian comments. The page foot (`further-info.md`) is generated from the section's `category` and `faq-topic`. Images use vault-relative paths; the generator rewrites them. A case that truly needs Liquid gets an issue and, if it recurs, a new directive by ADR.

## Consequences
Pages render in Obsidian. The importer and the generator are inverses of each other, which is what the parity check relies on.
```

- [x] **Step 5: Write the workflows**

`_system/workflows/bootstrap.md`:

```markdown
# Workflow: Bootstrap

Run once on an empty vault. Not grill-gated: the content is already published.

1. For every section N in 1..12: `make brain-raw SECTION=N WHAT=page` then
   `make brain-import BATCH=section-N-page`. This creates the twelve section
   pages as drafts, with callouts and directives, and copies their images.
2. Create the featured keyword pages from `_templates/keyword.md`: `lean`,
   `essential`, `thorough` (`featured: true`), plus `example` and `tooling`
   (`featured: false`). Definitions come from how the site uses them today.
3. Create the system pages from `_templates/system.md`: `htmlsc` (HTML Sanity
   Checker, alias `hsc`), `tpu` (TrafficPursuitUnit), `mama`, `status`. Where
   the meaning of a slug is unclear, raise an issue rather than invent.
4. Move the twelve batches to `raw/ingested/` and set each `SRC` record's
   `origin:` to `raw/ingested/section-N-page/`.
5. Fill `_system/index.md` with one line per page and append a
   `## [YYYY-MM-DD] bootstrap | twelve section pages` entry to `_system/log.md`.
6. `make brain-lint` must pass with zero errors.
```

`_system/workflows/ingest.md`:

```markdown
# Workflow: Ingest

Turn one raw batch into typed, linked wiki pages. For the bootstrap of
existing site content this is audit-style: type, link, flag. Grilling is
reserved for new content and for the FAQ merge.

1. **Batch.** `make brain-raw SECTION=N WHAT=content` (the section page already
   exists from bootstrap; use `WHAT=all` only when it does not). Confirm the
   batch under `raw/section-N-content/`.
2. **Import.** `make brain-import BATCH=section-N-content`. Every tip and
   example now exists as a draft with `legacy-tags` filled and a `SRC` record.
3. **Read.** Read every imported page. Note near-duplicates, outdated
   statements, dead external links, statements that contradict a section page.
4. **Vocabulary.** For every entry in `legacy-tags` on every page: decide
   keyword or term. Existing page: reference it (`keywords: ["[[lean]]"]`,
   `terms: ["[[decision]]"]`). Missing: create it from the template with a
   real definition and `home`. Ambiguous or near-duplicate of an existing
   term: add it to that term's `legacy-tags`/`aliases` and reference the term;
   when unsure raise an issue. Empty `legacy-tags` when done.
5. **Links.** Fill `related:` on every page. Look for: tips of the same
   section that build on each other, the example that shows what the tip
   says, the subsection the tip elaborates (link by heading), the term the
   tip is about. Add the reverse link on tips, examples and terms; not on
   sections.
6. **Issues.** One `ISS-NNN` page per finding from step 3, `related:` to every
   affected page.
7. **Status.** Set `status: review` on every page whose `legacy-tags` is
   empty and whose `related` is filled.
8. **Bookkeeping.** Update `_system/index.md`; append to `_system/log.md`:
   `## [YYYY-MM-DD] ingest | section N content`, listing pages created,
   terms/keywords created, issues raised. Move the batch to `raw/ingested/`
   and update the `SRC` record's `origin:`.
9. **Gate.** `make brain-lint` must report zero errors. Warnings about
   reciprocity are allowed but should be deliberate.

Quality bar: a section's ingest that creates no term page and raises no
issue has almost certainly under-read the content.
```

`_system/workflows/audit.md`:

```markdown
# Workflow: Audit

On request or after a batch of ingests. Read-only except for issues and the log.

Check and raise an issue for each finding:
- pages in `review` for longer than 30 days;
- terms without a definition sentence, or without `home`;
- keywords referenced by fewer than 2 pages;
- tips with an empty `related`;
- `legacy-tags` still present anywhere;
- headings inside guidance that differ from the house pattern
  (`Content` / `Motivation` / `Form`) — record, do not fix, until the section is
  cut over and parity no longer applies;
- external links that no longer resolve (check with `curl -sI`).

Append `## [YYYY-MM-DD] audit | <scope>` to `_system/log.md`.
```

`_system/workflows/relations.md`:

```markdown
# Workflow: Relations

How links are proposed and promoted (ADR-0004).

- The site renders `related:` only.
- Candidates are computed (dashboard, phase 3) from: shared terms (weight 3),
  same subsection (weight 2), shared keywords (weight 1), same system for
  examples (weight 2). Until the dashboard exists, find them by reading.
- Promote a candidate by adding it to `related:` on the page, and on the
  target when the target is a tip, example, term or FAQ answer.
- Never link a page to itself, to its own section (the section link is
  `section:`), or to more than 8 targets; more than 8 means the page or the
  vocabulary is too coarse.
```

`_system/workflows/cutover.md`:

```markdown
# Workflow: Cut-over (phase 2)

Placeholder until the generator exists. The steps will be: set the section's
pages to `published`, `make generate`, delete the hand-written originals in
`_pages/`, `_posts/`, `_examples/`, run `make check` and `make check-links`,
open one PR per section. See the spec §5 and §6.
```

- [x] **Step 6: Write `index.md` and `log.md`**

`_system/index.md`:

```markdown
# Index

One line per page, grouped by type. Updated on every ingest.

## Sections

## Tips

## Examples

## Terms

## Keywords

## Systems

## Issues

## Sources

## Architecture Decisions (ADR)
- [ADR-0001](adr/0001-record-architecture-decisions.md) — Record decisions about the brain as ADRs
- [ADR-0002](adr/0002-content-types-and-natural-ids.md) — Nine content types with natural IDs
- [ADR-0003](adr/0003-two-vocabularies.md) — Terms and keywords are separate vocabularies
- [ADR-0004](adr/0004-explicit-related-links.md) — The site renders only explicit related links
- [ADR-0005](adr/0005-no-liquid-callouts-and-directives.md) — No Liquid in the brain; callouts and directives instead
```

`_system/log.md`:

```markdown
# Log

Append-only. One entry per operation, prefix exact so it stays greppable:
`grep '^## \[' _system/log.md | tail -5`.

<!-- Format:
## [YYYY-MM-DD] <bootstrap|ingest|audit|report> | <subject>
- created: …
- updated: …
- issues: …
-->
```

- [x] **Step 7: Verify and commit**

Run: `make brain-lint && make brain-test`
Expected: lint `0 errors` (templates are outside `wiki/`), tests pass.

```bash
git add docs-arc42-brain
git commit -m "brain: agent schema, templates, ADRs 0001-0005, workflows, index and log

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 8: Bootstrap the vault: twelve section pages, keywords, systems

**Files:**
- Create (by tooling): `docs-arc42-brain/wiki/sections/section-1.md` … `section-12.md`, `wiki/assets/sections/{01,05,08,10}/…`, `raw/sources/SRC-001-section-1-page.md` … `SRC-012-section-12-page.md`, `raw/ingested/section-N-page/` (12 batches)
- Create (by hand from templates): `wiki/keywords/{lean,essential,thorough,example,tooling}.md`, `wiki/systems/{htmlsc,tpu,mama,status}.md`
- Modify: `_system/index.md`, `_system/log.md`

Follow `_system/workflows/bootstrap.md`. This task is the first real run of the tooling; anything it chokes on is a bug to fix in Tasks 5-6 (with a test) before continuing.

- [x] **Step 1: Raw and import all twelve section pages**

```bash
for n in 1 2 3 4 5 6 7 8 9 10 11 12; do
  make brain-raw SECTION=$n WHAT=page || exit 1
  make brain-import BATCH=section-$n-page || exit 1
done
ls docs-arc42-brain/wiki/sections
```

Expected: twelve files `section-1.md` … `section-12.md`; `wiki/assets/sections/` contains `01/iso-25010-2023-topics-en.svg`, `05/building-block-hierarchy.png`, `08/concepts-EN.drawio.png`, `10/arc42-system-qualities-overview.svg`.

- [x] **Step 2: Inspect the conversion of two irregular pages**

Run: `sed -n 1,60p docs-arc42-brain/wiki/sections/section-5.md` and `grep -n '%%\|\[!arc42-help\]\|{%\|{{' docs-arc42-brain/wiki/sections/section-10.md docs-arc42-brain/wiki/sections/section-3.md`

Expected: callouts open with `> [!arc42-help]` at every former div, including the two under 5.1; exactly one `%% examples: … %%` per former include (section 3: `business-context` and `technical-context`; section 1: `overview`, `qualitygoals`); one `%% examples-link %%` per page; no `{%` or `{{` anywhere; section 10's image reads `../assets/sections/10/arc42-system-qualities-overview.svg`. If anything differs, fix the importer with a failing test first, delete `wiki/sections/`, `wiki/assets/sections/`, `raw/sources/`, `raw/section-*`, and rerun Step 1.

- [x] **Step 3: Lint**

Run: `make brain-lint`
Expected: zero errors. Warnings are acceptable only if they are reciprocity warnings (there should be none yet).

- [x] **Step 4: Create keyword pages**

From `_templates/keyword.md`, with `status: draft`, `created`/`updated` = today, `sources: []` (keywords have no batch source; their meaning comes from how the site uses them), `related: []`. Files and content:

`wiki/keywords/lean.md`: `id: lean`, `title: lean`, `description: The minimal version of a practice: what to do when time is short`, `featured: true`.
`wiki/keywords/essential.md`: `id: essential`, `title: essential`, `description: The practice arc42 considers indispensable for a usable documentation`, `featured: true`.
`wiki/keywords/thorough.md`: `id: thorough`, `title: thorough`, `description: The extended version of a practice for teams that can afford rigour`, `featured: true`.
`wiki/keywords/example.md`: `id: example`, `title: example`, `description: The page shows a worked example rather than guidance`, `featured: false`.
`wiki/keywords/tooling.md`: `id: tooling`, `title: tooling`, `description: The page is about tools that support the practice`, `featured: false`.

- [x] **Step 5: Create system pages**

From `_templates/system.md`, `status: draft`, `sources: []`:

`wiki/systems/htmlsc.md`: `id: htmlsc`, `title: HTML Sanity Checker`, `name: HTML Sanity Checker`, `aliases: [hsc, HtmlSC]`, `url: ""`, body: one paragraph that it is the small open-source tool whose arc42 documentation serves as the running example on examples.arc42.org (check `_examples/*htmlsc*` for wording).
`wiki/systems/tpu.md`: `id: tpu`, `title: TrafficPursuitUnit`, `name: TrafficPursuitUnit`, body from `_examples/*tpu*`.
`wiki/systems/mama.md`: `id: mama`, `title: MaMa`, `name: <full name from _examples/*mama*>`, body from those files.
`wiki/systems/status.md`: read `_examples/05-buildingblock-example-status.md` first. If it documents a real system, create the page. If `status` is not a system, do not create the page; raise `wiki/issues/ISS-001-status-example-system.md` instead (kind `question`, `related: []` because the example is not a wiki page yet, name the file in the body) and remove `"status"` from `SYSTEM_TOKENS` in `importer.py`, updating `test_convert_example_maps_category_system_and_images` accordingly.

- [x] **Step 6: Archive the batches and fix `origin`**

```bash
cd docs-arc42-brain
for n in 1 2 3 4 5 6 7 8 9 10 11 12; do
  mv "raw/section-$n-page" "raw/ingested/section-$n-page"
  f=$(ls raw/sources/SRC-*-section-$n-page.md)
  sed -i '' "s#^origin: raw/section-$n-page/#origin: raw/ingested/section-$n-page/#" "$f"
done
cd ..
grep -h '^origin:' docs-arc42-brain/raw/sources/*.md
```

Expected: twelve `origin: raw/ingested/section-N-page/` lines; `docs-arc42-brain/raw/` top level holds only `ingested/`, `sources/`, `.gitkeep`.

- [x] **Step 7: Fill the index and log**

In `_system/index.md` add under `## Sections` one line per page in the form
`- [section-9](../wiki/sections/section-9.md) — 9 - Architecture decisions`, under `## Keywords` and `## Systems` the same pattern, and under `## Sources` one line per `SRC`. Append to `_system/log.md`:

```markdown
## [2026-09-17] bootstrap | twelve section pages, keywords, systems
- created: section-1 … section-12 (draft, from raw/ingested/section-N-page), SRC-001 … SRC-012
- created: keywords lean, essential, thorough, example, tooling; systems htmlsc, tpu, mama (+ status or ISS-001)
- notes: section 10 image path normalised from a hard-coded /assets/images path; all other bodies verbatim
```

Use the actual date of the run.

- [x] **Step 8: Lint and commit**

Run: `make brain-lint && make brain-test`
Expected: zero errors.

```bash
git add docs-arc42-brain
git commit -m "brain: bootstrap twelve section pages, keywords, systems

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 9: Pilot ingest of section 9 (content work)

**Files:**
- Create (by tooling): `wiki/tips/tip-9-1.md` … `tip-9-10.md`, `wiki/examples/09-decision-example-adr.md`, `09-decision-example-htmlsc-1.md`, `09-decision-example-tpu-2.md`, `raw/sources/SRC-013-section-9-content.md`
- Create (by hand): term pages under `wiki/terms/`, issue pages under `wiki/issues/`
- Modify: the imported pages (`keywords`, `terms`, `legacy-tags`, `related`, `status`), `wiki/sections/section-9.md` (`related`), `_system/index.md`, `_system/log.md`

Follow `_system/workflows/ingest.md` exactly. The legacy tags in this section are: `decision` (all ten tips), `adr` (9-8, 9-9, 9-10), `criteria` (9-2), `stakeholder` (9-1, 9-2, 9-4), `quality` (9-1, 9-4), `tooling` (9-10), `lean` (9-1, 9-7), `essential` (9-2, 9-3), `thorough` (9-6), and `example` on all three examples.

- [x] **Step 1: Batch and import**

```bash
make brain-raw SECTION=9 WHAT=content
make brain-import BATCH=section-9-content
make brain-lint
```

Expected: ten tips and three examples written; lint zero errors (drafts may carry `legacy-tags`).

- [x] **Step 2: Read every imported page** (`wiki/tips/tip-9-*.md`, the three examples, `wiki/sections/section-9.md`) and write down, for the log, near-duplicates, outdated statements, and external links to check with `curl -sI <url> | head -1`.

- [x] **Step 3: Vocabulary — proposed mapping, adjust with reasons if the text says otherwise**

Keywords (exist): `lean`, `essential`, `thorough`, `tooling`, `example`.

Terms to create from `_templates/term.md`, `status: draft`, `sources: ["[[SRC-013-section-9-content]]"]`:
- `wiki/terms/architecture-decision.md`: `id: architecture-decision`, `term: Architecture decision`, `legacy-tags: [decision]`, `home: "[[section-9]]"`, definition from the section's Content block ("selecting one alternative based on given criteria").
- `wiki/terms/adr.md`: `id: adr`, `term: Architecture Decision Record (ADR)`, `aliases: [ADR, Architecture Decision Record]`, `legacy-tags: [adr]`, `home: "[[section-9#Background (on ADRs)]]"` (a heading link is fine here: `home` is a link field and that heading is unique on the page), definition from the Nygard table.
- `wiki/terms/decision-criteria.md`: `id: decision-criteria`, `term: Decision criteria`, `legacy-tags: [criteria]`, `home: "[[section-9]]"`.
- `wiki/terms/stakeholder.md`: `id: stakeholder`, `term: Stakeholder`, `legacy-tags: [stakeholder]`, `home: "[[section-1#1.3 Stakeholder]]"`, definition from section 1.3's guidance.
- `wiki/terms/quality-requirement.md`: `id: quality-requirement`, `term: Quality requirement`, `legacy-tags: [quality]`, `home: "[[section-10]]"`, definition from section 10's Content block. Raise an issue that `quality` on tips 9-1 and 9-4 may mean "quality of the decision" rather than the arc42 concept; keep the mapping but record the doubt.

Then on every tip: `keywords: ["[[lean]]"]` etc., `terms: ["[[architecture-decision]]", …]`, and `legacy-tags: []`. On the examples: `keywords: ["[[example]]"]`, `terms: ["[[architecture-decision]]"]` (plus `[[adr]]` on the ADR example), `legacy-tags: []`.

- [x] **Step 4: Links — starting proposal**

- `tip-9-5` (document as ADR) ↔ `tip-9-8`, `tip-9-9`, `tip-9-10`, `09-decision-example-adr`, `[[section-9#Background (on ADRs)]]`, term `adr`.
- `tip-9-1` (only relevant decisions) → `[[section-9#Our proposal concerning decisions]]`, ↔ `tip-9-2`, `tip-9-3`.
- `tip-9-2` (criteria) ↔ `tip-9-3` (reasons), `tip-9-6` (rejected alternatives), term `decision-criteria`.
- `tip-9-4` (mind-map or table) ↔ `tip-9-7` (blog), the `htmlsc` and `tpu` examples.
- Each example → its system page (`system:` already) and `related: ["[[section-9]]"]`.
- Terms get `related` back-links to the tips that reference them (terms are reciprocated; sections are not).

Check `[[section-9#Our proposal concerning decisions]]` is unique on the page (it is an H3 inside the callout; the parser strips the callout prefix). If the lint reports it as not found, the heading text differs; copy it exactly from `wiki/sections/section-9.md`.

- [x] **Step 5: Issues** — one page per finding from Step 2, plus the `quality` doubt from Step 3, named `wiki/issues/ISS-NNN-<kebab>.md` from `_templates/issue.md`, `related:` listing every affected page.

- [x] **Step 6: Status, bookkeeping, archive**

Set `status: review` on all thirteen pages and the new terms. Update `_system/index.md` (Tips, Examples, Terms, Issues, Sources). Append to `_system/log.md`:

```markdown
## [YYYY-MM-DD] ingest | section 9 content
- created: tip-9-1 … tip-9-10, 3 examples (review), terms architecture-decision, adr, decision-criteria, stakeholder, quality-requirement, SRC-013
- links: N related links, M subsection links   (real numbers from the pages you wrote)
- issues: ISS-013 …, one line each
- notes: whatever the next section's ingest should know, or "none"
```

```bash
mv docs-arc42-brain/raw/section-9-content docs-arc42-brain/raw/ingested/section-9-content
sed -i '' 's#^origin: raw/section-9-content/#origin: raw/ingested/section-9-content/#' docs-arc42-brain/raw/sources/SRC-013-section-9-content.md
```

- [x] **Step 7: Gate and commit**

Run: `make brain-lint`
Expected: zero errors; any warnings are listed and each is deliberate (write why in the log entry).

```bash
git add docs-arc42-brain
git commit -m "brain: ingest section 9 tips and examples (pilot)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 10: Phase exit verification

**Files:**
- Modify: `docs/superpowers/specs/2026-09-17-docs-arc42-brain-design.md` (status line only)

- [x] **Step 1: Run every check**

```bash
make brain-test
make brain-lint
make check
```

Expected: tests pass; lint zero errors; `make check` builds the Jekyll site in Docker and passes its sanity checks, proving the `docs`/`docs-arc42-brain` excludes keep the vault out of `_site/`. Confirm with `ls _site | grep -c brain` → `0`.

- [x] **Step 2: Open the vault in Obsidian** (`open -a Obsidian docs-arc42-brain` or File → Open folder as vault) and check: `section-9` renders its callouts, `tip-9-5` shows its related links, the graph view connects tips, terms, examples and section 9. Record any rendering problem as an issue page; do not fix the schema ad hoc.

  Adjusted: driven non-interactively, so the GUI check was replaced with a read-only structural stand-in (confirmed `section-9.md` has `> [!arc42-help]`, `tip-9-5.md` has a non-empty `related:` list, and cited the lint's `0 errors` as proof every wikilink resolves). The Obsidian rendering/graph-view check itself is left to the human.

- [x] **Step 3: Mark the spec**

Change the spec's first status line to `Status: phase 1 implemented · 2026-09-17 · branch docs-arc42-brain` and commit:

```bash
git add docs/superpowers/specs/2026-09-17-docs-arc42-brain-design.md
git commit -m "docs: mark brain spec phase 1 as implemented

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [x] **Step 4: Report** the phase exit to the user: number of pages by type, open issues, lint warnings, and what phase 2 (generator + parity check on section 9) needs first.

---

## Self-review against the spec

- §3 layout: Task 1 (folders), Task 7 (docs), `build/` gitignored, `.obsidian/` gitignored. ✔
- §4.1 common frontmatter and statuses: Task 4 `COMMON_FIELDS`, `DEFAULT_STATUS`, `STATUS_BY_TYPE`. ✔
- §4.2 types and fields: Task 4 `REQUIRED_FIELDS`, Task 7 templates. Deviations from the spec table, deliberate: `subsection` is folded into the `section` link's `#heading` (D6 link format); `source` carries `files: [{path, sha256}]` instead of a single `sha256` because a batch has many files; `system` pages gain `aliases`. ✔
- §4.3 callouts, directives, anchors, foot: Task 3 parser, Task 4 L8/L14/L15, Task 6 importer. ✔
- §4.4 no Liquid, image rewriting: Task 4 L12, Task 6. ✔
- §4.5 site-side rendering: phase 2, out of scope. —
- §5 workflows: Task 7; bootstrap executed in Task 8; ingest executed in Task 9; cut-over is a placeholder until phase 2. ✔
- §8 lint: all rules except "tip section vs legacy category" (tips no longer carry `category`; the importer derives `section` from the batch) and "hand-edited generated file" (phase 2). ✔
- §9 make targets: `brain-test`, `brain-lint`, `brain-raw`, `brain-import` in phase 1; `generate`, `generate-check`, `dashboard`, `brain-suggest` in later phases. ✔
- §10 testing: unit tests per module; end-to-end import → lint test. ✔
- §11 phase 1 exit criterion: Task 10. ✔
