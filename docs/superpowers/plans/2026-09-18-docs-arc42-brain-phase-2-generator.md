# docs-arc42-brain Phase 2 (Generator and Section-9 Cut-over) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A deterministic generator turns published brain pages into the Jekyll files of docs.arc42.org, a parity check proves it reproduces the hand-written section-9 files, and section 9 is cut over.

**Architecture:** Five new modules in the existing `braingen` package: `emit_body` (text transforms that invert the importer), `compare` (per-file parity rule), `emit` (page → file with front matter, tags, `related:`), `generate` (plan / apply / check, owning only files that carry the marker line), `parity` (per-section check with notes). Three CLI commands and three make targets drive them; `make check` gains the lint and the generated-files check. One hand-made include renders `related:` on tips and examples.

**Tech Stack:** Python ≥3.12 managed by uv (`python-frontmatter`, `PyYAML`, `pytest` — no new dependencies), GNU make, Jekyll 3.10 / Liquid in Docker.

**Spec:** `docs/superpowers/specs/2026-09-17-docs-arc42-brain-design.md` §4.3–§4.5, §6, §9, §10, §11 phase 2. Dashboard contract: `docs/superpowers/specs/2026-09-18-docs-arc42-brain-dashboard-design.md` D19 and §4 (the dashboard will call `make brain-lint && make generate`, and the parity generator into `build/parity/` for its preview). Phase-2 must-knows: `docs/superpowers/plans/2026-09-18-docs-arc42-brain-next-session-handover.md`.

## Global Constraints

- Repo `/Users/gernotstarke/projects/arc42/docs.arc42.org-site`, branch `docs-arc42-brain`. Stay on it. Never push, never switch branches.
- Nothing outside `docs-arc42-brain/` and `docs/` changes, except: `_includes/related.html` (new, Task 8), one include line in `_layouts/post.html` (Task 8), the `check` target in the root `Makefile` (Task 7), and in Task 9 the section-9 files under `_pages/`, `_posts/09-decisions/`, `_examples/`. Nothing else in `_layouts/`, `_includes/`, `_sass/`, `_data/`, `scripts/`.
- No Liquid (`{{` or `{%`) anywhere under `docs-arc42-brain/wiki/`. The generator introduces every `{% %}` and `{{ }}`.
- Every generated file carries the marker line `<!-- generated from docs-arc42-brain/<vault-relative path> — do not edit -->` as the first line after its front matter. `make generate` never writes over or deletes a file without it.
- Permalinks are emitted byte-identical (D3). Tags are compared as sets after alias normalisation; differences are printed, never failed.
- Every commit message ends with exactly this line, whatever model you are: `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. After committing, verify with `git log -1 --format=%B | tail -1`; amend if it differs.
- Stage with explicit paths: `git add <path> …`. Never `git add -A`, `git add .` or `git commit -a`.
- One commit per task. The commit includes this plan file with the task's own checkboxes ticked — tick boxes only between your task's heading and the next task's heading.
- Tooling: `uv` is `~/.local/bin/uv` (on PATH). System `python3` is 3.14; the package needs ≥3.12 and uv provides it. Run tests with `make brain-test` from the repo root. Docker runs `make check`, `make site`, `make check-links`.
- `pyproject.toml` and `uv.lock` do not change: no new dependencies. (The spec names Jinja2 and markdown-it-py; see Deviations.)
- Match the existing `braingen` style: module docstring, `from __future__ import annotations`, dataclasses, plain functions, no classes with behaviour beyond dataclasses, comments only where the why is not obvious.
- Do not modify phase-1 modules (`parse.py`, `lint.py`, `importer.py`, `raw.py`, `anchors.py`, `wikilinks.py`) or their tests. `cli.py` is extended in Task 7 only.
- Code blocks in this plan were run against the real vault and site before the plan was written (113 tests green, all twelve sections parity-green, a simulated section-9 cut-over idempotent). Transcribe them exactly; if something fails, report it instead of improvising.

## Deviations from the spec (decided in this plan, for review)

1. **No Jinja2, no markdown-it-py.** Each emitter is a short string builder; the one non-trivial transform (callout → help div) is line-based and its contract is the round-trip test on real pages. A template engine adds a dependency and hides byte layout, which parity depends on.
2. **External links are not rewritten** (spec §4.4 says every absolute markdown link becomes `<a target="_blank" …>`). Section 9's page body has plain markdown links today, so the rewrite would break parity on the very section that gates phase 2. Raised as ISS-011 in Task 2.
3. **"Tags that disappear from the site" are reported by `make generate-check`**, not by `make brain-lint` (spec §4.5): only the parity check reads the site. It prints `keyword page loses tags: …` / `gains tags: …`, computed like `site.tags` (posts only).
4. **Parity normalises more than trailing whitespace:** leading and trailing blank lines of the body (posts have 0, 1 or 2 blank lines after the front matter, and `frontmatter` strips them on import), and the `further-info.md` foot, which is compared by its three arguments because its line layout differs between sections 1, 5 and the rest. Each normalisation is printed as a note. Section 11's missing blank line is therefore a note, not a failure.
5. **Anchors are checked against the built page** (`_site/section-N/index.html`) when it exists: every heading anchor the brain computes must exist on the site. Section 7's `motivation-1` (brain) vs `motivation` (site) is the one documented exception. Without a build, the check prints a note and skips.
6. **Cut-over order is: flip status, delete originals, generate** (the handover says generate, then delete). `make generate` refuses to overwrite a file without the marker, so the originals go first. The generated files return at the same paths; git shows 14 modified files, not deletions plus additions.
7. **The `related:` block** lists the page's own section link first (a `subsection` entry when `section:` carries a heading, else a `section` entry), then `related:` in declared order. A term or keyword links to `/keywords/#<slug>` only when a generated tip carries that tag (otherwise that anchor does not exist and html-proofer would fail); without a URL it renders as text. Links to unpublished tips/examples are left out.
8. **Assets are owned through a manifest**, `docs-arc42-brain/_system/generated-assets.txt`, because a binary file cannot carry the marker. Only images referenced by emitted pages are copied. An existing identical file is adopted; an existing different one blocks the run. Section 9 references no images, so the manifest is not created in this phase.
9. **`braingen generate` runs the lint first** and stops on errors. The dashboard's `make brain-lint && make generate` works unchanged.

## File structure

```
docs-arc42-brain/_system/generate/
  braingen/
    emit_body.py      NEW  T2  marker, callout→div, directives→includes, images→Liquid, further-info foot
    compare.py        NEW  T2  one generated file vs. its original: normalisation, notes, problems
    emit.py           NEW  T3/T4  Output; YAML scalars and front matter; emit_section; tags, related, emit_tip, emit_example
    generate.py       NEW  T5  plan / conflicts / apply / check, asset manifest
    parity.py         NEW  T6  check_section: files + anchors + not-ingested + keyword-page tags; format_report
    cli.py            MOD  T7  generate, generate-check, check-generated
  tests/
    fixtures/roundtrip/    NEW  T1  sections 5, 10, 11 (+ manifests), tip 9-2, example adr — verbatim site copies
    test_roundtrip.py      NEW  T1  importer → emitter → original (strict xfail until T3/T4)
    test_emit_body.py      NEW  T2
    test_compare.py        NEW  T2
    vaultkit.py            NEW  T3  builders for small test vaults
    test_emit_section.py   NEW  T3
    test_emit_content.py   NEW  T4
    test_generate.py       NEW  T5
    test_parity.py         NEW  T6  includes the section-9 integration test against raw/ingested/
    test_cli_generate.py   NEW  T7
docs-arc42-brain/_system/brain.mk          MOD  T7  generate, generate-check, brain-check-generated
docs-arc42-brain/CLAUDE.md                  MOD  T7  command list
docs-arc42-brain/_system/workflows/cutover.md  MOD  T7  the real procedure
docs-arc42-brain/_system/log.md             MOD  T7 (format line), T9 (cutover entry)
docs-arc42-brain/wiki/issues/ISS-011-…md    NEW  T2
docs-arc42-brain/_system/index.md           MOD  T2  ISS-011 line
Makefile                                    MOD  T7  check: brain-lint brain-check-generated
_includes/related.html                      NEW  T8
_layouts/post.html                          MOD  T8  one include line
_pages/section-9.md, _posts/09-decisions/*.md, _examples/09-decision-*.md   T9  generated
docs-arc42-brain/wiki/{sections/section-9,tips/tip-9-*,examples/09-*}.md    T9  status: published
```

Test counts after each task (`make brain-test`): T1 53 passed + 5 xfailed · T2 79 + 5 xfailed · T3 85 + 2 xfailed · T4 94 · T5 103 · T6 110 · T7 113 · T8 113 · T9 113.

---

### Task 1: Real-page fixtures and the round-trip test

Model: Haiku. The round-trip test is written before any emitter exists. It is marked `xfail(strict=True, raises=ImportError)`: it is expected to fail only because the emitter modules do not exist yet; the moment Tasks 3 and 4 make it pass, strict xfail turns the XPASS into a failure and forces the marker's removal.

**Files:**
- Create: `docs-arc42-brain/_system/generate/tests/fixtures/roundtrip/` (8 files copied from the site)
- Create: `docs-arc42-brain/_system/generate/tests/test_roundtrip.py`

**Interfaces:**
- Consumes: `braingen.importer.convert_section(text, manifest, today, source_slug) -> (meta, body)`, `convert_tip(filename, text, manifest, today, source_slug)`, `convert_example(...)`, `write_page(path, meta, body)`; `braingen.parse.load_vault(root) -> Vault`.
- Produces (for Tasks 3 and 4 to satisfy): `braingen.compare.compare_file(rel, original, generated, section, aliases) -> FileReport` with `.problems: list[str]`, `.notes: list[str]`; `braingen.emit.emit_section(vault, page) -> Output`; `emit_tip(vault, page, emitted: set[str], site_tags: set[str]) -> Output`; `emit_example(vault, page, emitted, site_tags) -> Output`; `Output.rel`, `Output.text`.

- [x] **Step 1: Copy the fixtures verbatim (from the repo root)**

```bash
F=docs-arc42-brain/_system/generate/tests/fixtures/roundtrip
mkdir -p $F
for n in 5 10 11; do
  cp _pages/section-$n.md $F/section-$n.md
  cp docs-arc42-brain/raw/ingested/section-$n-page/manifest.yaml $F/section-$n.manifest.yaml
done
cp _posts/09-decisions/2016-03-01-t-9-2.md _examples/09-decision-example-adr.md $F/
for n in 5 10 11; do cmp _pages/section-$n.md $F/section-$n.md; done
cmp _posts/09-decisions/2016-03-01-t-9-2.md $F/2016-03-01-t-9-2.md
cmp _examples/09-decision-example-adr.md $F/09-decision-example-adr.md
ls $F
```

Expected: no `cmp` output; `ls` lists 8 files: `09-decision-example-adr.md 2016-03-01-t-9-2.md section-10.manifest.yaml section-10.md section-11.manifest.yaml section-11.md section-5.manifest.yaml section-5.md`.

- [x] **Step 2: Write the round-trip test**

Create `docs-arc42-brain/_system/generate/tests/test_roundtrip.py`:

```python
"""Round trip on real pages: original -> importer -> wiki page -> emitter -> original.

The fixtures under fixtures/roundtrip/ are verbatim copies of site files:
sections 5, 10 and 11 were picked for their irregularities (5: two callouts
under one heading and callouts under H3 headings; 10: the hard-coded image
path and H2 guidance headings inside a subsection; 11: no blank line after the
front matter and a raw <a> inside a blockquote), plus one tip and one example
of section 9. The emitters are the importer inverted; this test is their
contract, and compare_file is the parity check's per-file rule.
"""
from pathlib import Path

import pytest
import yaml

from braingen.importer import convert_example, convert_section, convert_tip, write_page
from braingen.parse import load_vault

FIX = Path(__file__).parent / "fixtures" / "roundtrip"
TODAY = "2026-09-18"
SRC = "SRC-999-roundtrip"
SECTION_9_MANIFEST = {"section": 9, "posts_dir": "09-decisions"}
SECTION_9_META = {
    "id": "section-9", "type": "section", "title": "9 - Architecture decisions", "status": "draft",
    "created": TODAY, "updated": TODAY, "sources": [], "related": [], "number": 9,
    "name": "Architecture Decisions", "category": "decisions", "posts-dir": "09-decisions",
    "permalink": "/section-9/", "order": 13, "faq-topic": "fundamental architecture and design decisions",
}
EXPECTED_NOTES = {
    5: [],
    10: ["expected difference: hard-coded image path normalised to {{ site.imageurl }} at ingest (spec Appendix A)"],
    11: ["normalised: 0 blank lines after the front matter in the original, 1 generated"],
}

SECTIONS_PENDING = pytest.mark.xfail(strict=True, raises=ImportError, reason="section emitter arrives in Task 3")
CONTENT_PENDING = pytest.mark.xfail(strict=True, raises=ImportError, reason="tip/example emitters arrive in Task 4")


@SECTIONS_PENDING
@pytest.mark.parametrize("n", [5, 10, 11])
def test_section_round_trip(tmp_path, n):
    from braingen.compare import compare_file
    from braingen.emit import emit_section

    original = (FIX / f"section-{n}.md").read_text(encoding="utf-8")
    manifest = yaml.safe_load((FIX / f"section-{n}.manifest.yaml").read_text(encoding="utf-8"))
    meta, body = convert_section(original, manifest, TODAY, SRC)
    write_page(tmp_path / "wiki/sections" / f"section-{n}.md", meta, body)
    vault = load_vault(tmp_path)

    out = emit_section(vault, vault.pages[f"section-{n}"])

    assert out.rel == f"_pages/section-{n}.md"
    rep = compare_file(out.rel, original, out.text, n, {})
    assert rep.problems == []
    assert rep.notes == EXPECTED_NOTES[n]


def _section_9(root: Path) -> None:
    write_page(root / "wiki/sections/section-9.md", SECTION_9_META, "# 9. Architecture Decisions\n")


@CONTENT_PENDING
def test_tip_round_trip(tmp_path):
    from braingen.compare import compare_file
    from braingen.emit import emit_tip

    name = "2016-03-01-t-9-2.md"
    original = (FIX / name).read_text(encoding="utf-8")
    _section_9(tmp_path)
    meta, body = convert_tip(name, original, SECTION_9_MANIFEST, TODAY, SRC)
    write_page(tmp_path / "wiki/tips/tip-9-2.md", meta, body)
    vault = load_vault(tmp_path)

    out = emit_tip(vault, vault.pages["tip-9-2"], set(), set())

    assert out.rel == "_posts/09-decisions/" + name
    rep = compare_file(out.rel, original, out.text, 9, {})
    assert rep.problems == []   # tags differ (legacy tags are not mapped here): notes only


@CONTENT_PENDING
def test_example_round_trip(tmp_path):
    from braingen.compare import compare_file
    from braingen.emit import emit_example

    name = "09-decision-example-adr.md"
    original = (FIX / name).read_text(encoding="utf-8")
    _section_9(tmp_path)
    meta, body = convert_example(name, original, SECTION_9_MANIFEST, TODAY, SRC)
    write_page(tmp_path / "wiki/examples" / name, meta, body)
    vault = load_vault(tmp_path)

    out = emit_example(vault, vault.pages["09-decision-example-adr"], set(), set())

    assert out.rel == "_examples/" + name
    rep = compare_file(out.rel, original, out.text, 9, {})
    assert rep.problems == []
```

- [x] **Step 3: Run the suite**

Run: `make brain-test`
Expected: `53 passed, 5 xfailed`.

- [x] **Step 4: Commit**

```bash
git add docs-arc42-brain/_system/generate/tests/fixtures/roundtrip docs-arc42-brain/_system/generate/tests/test_roundtrip.py docs/superpowers/plans/2026-09-18-docs-arc42-brain-phase-2-generator.md
git commit -m "brain: round-trip fixtures (sections 5, 10, 11, tip 9-2, adr example) and test, before any emitter

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
git log -1 --format=%B | tail -1
```

---

### Task 2: Body transforms and the per-file comparison

Model: Haiku.

**Files:**
- Create: `docs-arc42-brain/_system/generate/braingen/emit_body.py`
- Create: `docs-arc42-brain/_system/generate/braingen/compare.py`
- Create: `docs-arc42-brain/_system/generate/tests/test_emit_body.py`
- Create: `docs-arc42-brain/_system/generate/tests/test_compare.py`
- Create: `docs-arc42-brain/wiki/issues/ISS-011-external-link-rewrite-deferred.md`
- Modify: `docs-arc42-brain/_system/index.md` (one line under `## Issues`)

**Interfaces:**
- Produces: `emit_body.MARKER_PREFIX: str`; `marker(source: str) -> str`; `is_generated(text: str) -> bool`; `rewrite_images(text) -> str`; `section_body(body) -> str`; `further_info(number: int, category: str, topic: str) -> str`; `section_document_body(body, number, category, topic) -> str`; `content_body(body) -> str`.
- Produces: `compare.FileReport(rel, ok=True, problems=[], notes=[])`; `normalise_lines(text) -> list[str]`; `strip_marker(body) -> str`; `split_foot(body) -> (body, dict | None)`; `split_tags(value) -> list[str]`; `leading_blank_lines(text) -> int`; `compare_file(rel, original, generated, section: int, aliases: dict[str, str]) -> FileReport`; `EXPECTED_BODY`.

- [x] **Step 1: Write the failing tests**

Create `docs-arc42-brain/_system/generate/tests/test_emit_body.py`:

```python
import pytest

from braingen.emit_body import (
    content_body,
    further_info,
    is_generated,
    marker,
    rewrite_images,
    section_body,
    section_document_body,
)

HELP_OPEN = '<div class="arc42-help" markdown="1">'


def test_marker_line():
    assert marker("wiki/tips/tip-9-1.md") == "<!-- generated from docs-arc42-brain/wiki/tips/tip-9-1.md — do not edit -->"


def test_is_generated_only_when_marker_is_first_line_after_front_matter():
    m = marker("wiki/tips/tip-9-1.md")
    assert is_generated(f"---\na: 1\n---\n{m}\n\nbody\n")
    assert not is_generated("---\na: 1\n---\n\nbody\n")
    assert not is_generated(f"---\na: 1\n---\n\n{m}\n")
    assert not is_generated(f"{m}\n")
    assert not is_generated("---\na: 1\n")


def test_rewrite_images_back_to_liquid():
    text = "![a](../assets/sections/10/q.svg) and ![b](../assets/examples/x.png)"
    assert rewrite_images(text) == "![a]({{ site.imageurl }}/10/q.svg) and ![b]({{ site.exampleimages }}/x.png)"


def test_callout_becomes_help_div_closed_before_next_plain_line():
    body = "# 9. X\n\n> [!arc42-help]\n>\n> ## Content\n> text\n>  indented\n>\n\nafter\n"
    assert section_body(body) == (
        f"# 9. X\n\n{HELP_OPEN}\n\n## Content\ntext\n indented\n\n</div>\n\nafter\n"
    )


def test_callout_at_end_of_body_is_closed():
    assert section_body("> [!arc42-help]\n> x\n") == f"{HELP_OPEN}\nx\n</div>\n"


def test_adjacent_callouts_become_adjacent_divs():
    assert section_body("> [!arc42-help]\n> a\n> [!arc42-help]\n> b\n") == (
        f"{HELP_OPEN}\na\n</div>\n{HELP_OPEN}\nb\n</div>\n"
    )


def test_blockquote_inside_callout_keeps_one_level():
    assert section_body("> [!arc42-help]\n> > quoted\n") == f"{HELP_OPEN}\n> quoted\n</div>\n"


def test_directives_become_includes():
    body = "> [!arc42-help]\n> %% examples: decisions %%\n\n%% examples-link %%\n"
    assert section_body(body) == (
        f'{HELP_OPEN}\n{{% include example.md category="decisions" %}}\n</div>\n\n'
        '{% include examples-link.html variant="inline" %}\n'
    )


def test_unknown_directive_is_an_error():
    with pytest.raises(ValueError, match="bogus"):
        section_body("%% bogus %%\n")


def test_images_in_section_body():
    assert section_body("![q](../assets/sections/10/q.svg)\n") == "![q]({{ site.imageurl }}/10/q.svg)\n"


def test_further_info_foot():
    assert further_info(9, "decisions", "fundamental architecture and design decisions") == (
        "{% include further-info.md\n"
        '   category="decisions"\n'
        '   topic="fundamental architecture and design decisions"\n'
        '   faqlink="https://faq.arc42.org/category_c/#c-sec-9" %}\n'
    )


def test_section_document_body_appends_foot_after_two_blank_lines():
    assert section_document_body("# 9\n", 9, "decisions", "t") == (
        "# 9\n\n\n" + further_info(9, "decisions", "t")
    )


def test_content_body_rewrites_images_and_ends_with_one_newline():
    assert content_body("![x](../assets/examples/a.png)\n\n\n") == "![x]({{ site.exampleimages }}/a.png)\n"
```

Create `docs-arc42-brain/_system/generate/tests/test_compare.py`:

```python
from braingen.compare import (
    compare_file,
    leading_blank_lines,
    normalise_lines,
    split_foot,
    split_tags,
    strip_marker,
)
from braingen.emit_body import marker

MARK = marker("wiki/tips/tip-9-1.md")
ORIG = (
    '---\nlayout: post\ntitle: "Tip 9-1: X"\ntags: decision lean\ncategory: decisions\n'
    "permalink: /tips/9-1/\n---\nBody line  \n\nsecond\n"
)
GEN = (
    '---\nlayout: post\ntitle: "Tip 9-1: X"\ntags: lean architecture-decision\ncategory: decisions\n'
    'permalink: /tips/9-1/\nrelated:\n- kind: tip\n  title: "Tip 9-2"\n  url: /tips/9-2/\n---\n'
    f"{MARK}\n\nBody line\n\nsecond\n"
)


def test_normalise_lines():
    assert normalise_lines("\n\na  \n\nb\t\n\n") == ["a", "", "b"]


def test_strip_marker():
    assert strip_marker(f"\n{MARK}\n\nbody") == "\nbody"
    assert strip_marker("body") == "body"


def test_split_foot_compares_arguments_not_layout():
    a = '{% include further-info.md category="x"\n  topic="t" faqlink="u" %}'
    b = '{% include further-info.md\n   category="x"\n   topic="t"\n   faqlink="u" %}\n'
    args = {"category": "x", "topic": "t", "faqlink": "u"}
    assert split_foot("body\n" + a)[1] == args
    assert split_foot("body\n" + b)[1] == args
    assert split_foot("no foot") == ("no foot", None)


def test_split_tags():
    assert split_tags("a b") == ["a", "b"]
    assert split_tags(["a"]) == ["a"]
    assert split_tags(None) == []


def test_leading_blank_lines():
    assert leading_blank_lines("---\na: 1\n---\nx") == 0
    assert leading_blank_lines("---\na: 1\n---\n\n\nx") == 2


def test_identical_apart_from_marker_related_and_tags_passes_with_notes():
    rep = compare_file("_posts/09-decisions/2016-03-01-t-9-1.md", ORIG, GEN, 9, {"decision": "architecture-decision"})
    assert rep.ok
    assert rep.problems == []
    assert rep.notes == [
        "tags on the site: -['decision'] +['architecture-decision']",
        "normalised: 0 blank lines after the front matter in the original, 1 generated",
    ]


def test_tag_residue_after_alias_normalisation_is_a_note():
    rep = compare_file("x.md", ORIG, GEN, 9, {})
    assert rep.ok
    assert "tags after alias normalisation: -['decision'] +['architecture-decision']" in rep.notes


def test_changed_front_matter_value_fails():
    rep = compare_file("x.md", ORIG, GEN.replace("/tips/9-1/", "/tips/9-99/"), 9, {})
    assert not rep.ok
    assert rep.problems == ["front matter: permalink: '/tips/9-1/' -> '/tips/9-99/'"]


def test_missing_front_matter_key_fails():
    rep = compare_file("x.md", ORIG, GEN.replace("category: decisions\n", ""), 9, {})
    assert rep.problems == ["front matter: key 'category' missing"]


def test_body_difference_fails_with_a_diff():
    rep = compare_file("x.md", ORIG, GEN.replace("second", "2nd"), 9, {})
    assert not rep.ok
    assert rep.problems[0].startswith("body differs:")
    assert "-second" in rep.problems[0] and "+2nd" in rep.problems[0]


def test_expected_difference_applies_to_its_section_only():
    orig = "---\ntitle: t\n---\n\n![q](/assets/images/sections/10/q.svg)\n"
    gen = f"---\ntitle: t\n---\n{marker('wiki/sections/section-10.md')}\n\n![q]({{{{ site.imageurl }}}}/10/q.svg)\n"
    ten = compare_file("_pages/section-10.md", orig, gen, 10, {})
    assert ten.ok
    assert ten.notes == ["expected difference: hard-coded image path normalised to {{ site.imageurl }} at ingest (spec Appendix A)"]
    assert not compare_file("_pages/section-9.md", orig, gen, 9, {}).ok


def test_foot_layout_is_ignored_but_its_arguments_are_compared():
    orig = '---\ntitle: t\n---\n\nx\n\n{% include further-info.md category="a"\n  topic="t"\n  faqlink="u" %}\n'
    gen = (
        f"---\ntitle: t\n---\n{marker('wiki/sections/section-1.md')}\n\nx\n\n\n"
        '{% include further-info.md\n   category="a"\n   topic="t"\n   faqlink="u" %}\n'
    )
    assert compare_file("s.md", orig, gen, 1, {}).ok
    rep = compare_file("s.md", orig, gen.replace('topic="t"', 'topic="other"'), 1, {})
    assert rep.problems == [
        "further-info foot: {'category': 'a', 'topic': 't', 'faqlink': 'u'} -> "
        "{'category': 'a', 'topic': 'other', 'faqlink': 'u'}"
    ]


def test_a_generated_original_compares_equal_to_itself():
    rep = compare_file("x.md", GEN, GEN, 9, {})
    assert rep.ok
    assert rep.notes == []
```

- [x] **Step 2: Run them to see them fail**

Run: `make brain-test`
Expected: collection errors for `test_emit_body.py` and `test_compare.py` (`ModuleNotFoundError: No module named 'braingen.emit_body'` / `'braingen.compare'`).

- [x] **Step 3: Write `emit_body.py`**

Create `docs-arc42-brain/_system/generate/braingen/emit_body.py`:

```python
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
```

- [x] **Step 4: Write `compare.py`**

Create `docs-arc42-brain/_system/generate/braingen/compare.py`:

```python
"""Compare one generated file with its hand-written original (brain spec §6).

Pass condition:
- body identical after normalisation: trailing whitespace per line, leading and
  trailing blank lines, the marker line, and the further-info foot, which is
  compared by its arguments because its line layout varies between the
  hand-written pages;
- every front-matter key of the original has an identical value in the
  generated file, except `tags`; new keys (`related`) are allowed;
- `tags` differences are reported as notes, raw and after alias
  normalisation, and never fail.

EXPECTED_BODY lists the documented differences; each is applied to the
original before comparing and reported as a note.
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field

import frontmatter

from .emit_body import MARKER_PREFIX, is_generated

FOOT_RE = re.compile(r"\{%\s*include further-info\.md(.*?)%\}", re.S)
ARG_RE = re.compile(r'([a-z]+)="([^"]*)"')

# (section number, text in the original, replacement, why)
EXPECTED_BODY: list[tuple[int, str, str, str]] = [
    (10, "](/assets/images/sections/", "]({{ site.imageurl }}/",
     "hard-coded image path normalised to {{ site.imageurl }} at ingest (spec Appendix A)"),
]


@dataclass
class FileReport:
    rel: str
    ok: bool = True
    problems: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def normalise_lines(text: str) -> list[str]:
    lines = [l.rstrip() for l in text.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return lines


def strip_marker(body: str) -> str:
    lines = body.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].startswith(MARKER_PREFIX):
        lines.pop(0)
    return "\n".join(lines)


def split_foot(body: str) -> tuple[str, dict[str, str] | None]:
    m = FOOT_RE.search(body)
    if not m:
        return body, None
    return body[: m.start()] + body[m.end():], dict(ARG_RE.findall(m.group(1)))


def split_tags(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return value.split()
    return [str(t) for t in value]


def leading_blank_lines(text: str) -> int:
    end = text.find("\n---\n", 3)
    rest = text[end + 5:] if text.startswith("---\n") and end >= 0 else text
    return len(rest) - len(rest.lstrip("\n"))


def compare_file(rel: str, original: str, generated: str, section: int, aliases: dict[str, str]) -> FileReport:
    rep = FileReport(rel)
    o, g = frontmatter.loads(original), frontmatter.loads(generated)
    for key, value in o.metadata.items():
        if key == "tags":
            continue
        if key not in g.metadata:
            rep.problems.append(f"front matter: key '{key}' missing")
        elif g.metadata[key] != value:
            rep.problems.append(f"front matter: {key}: {value!r} -> {g.metadata[key]!r}")
    old, new = split_tags(o.metadata.get("tags")), split_tags(g.metadata.get("tags"))
    if set(old) != set(new):
        rep.notes.append(f"tags on the site: -{sorted(set(old) - set(new))} +{sorted(set(new) - set(old))}")
        norm = {aliases.get(t, t) for t in old}
        if norm != set(new):
            rep.notes.append(f"tags after alias normalisation: -{sorted(norm - set(new))} +{sorted(set(new) - norm)}")
    lead = leading_blank_lines(original)
    if lead != 1 and not is_generated(original):
        rep.notes.append(f"normalised: {lead} blank lines after the front matter in the original, 1 generated")
    obody = strip_marker(o.content)   # after cut-over the "original" is a generated file
    for n, old_text, new_text, why in EXPECTED_BODY:
        if n == section and old_text in obody:
            obody = obody.replace(old_text, new_text)
            rep.notes.append(f"expected difference: {why}")
    obody, ofoot = split_foot(obody)
    gbody, gfoot = split_foot(strip_marker(g.content))
    if ofoot != gfoot:
        rep.problems.append(f"further-info foot: {ofoot} -> {gfoot}")
    ol, gl = normalise_lines(obody), normalise_lines(gbody)
    if ol != gl:
        diff = list(difflib.unified_diff(ol, gl, "original", "generated", lineterm="", n=1))
        rep.problems.append("body differs:\n    " + "\n    ".join(diff[:40]))
    rep.ok = not rep.problems
    return rep
```

- [x] **Step 5: Run the suite**

Run: `make brain-test`
Expected: `79 passed, 5 xfailed`.

- [x] **Step 6: Raise ISS-011 for the deferred link rewrite**

Create `docs-arc42-brain/wiki/issues/ISS-011-external-link-rewrite-deferred.md`:

```markdown
---
id: ISS-011
type: issue
title: The generator does not rewrite external markdown links to target-blank anchors
status: open
created: '2026-09-18'
updated: '2026-09-18'
sources: []
related:
- '[[section-9]]'
severity: minor
kind: contradiction
raised-by: agent
resolved: null
---

**What's unresolved.** Brain spec §4.4 says the generator rewrites every absolute `http(s)://`
markdown link into `<a target="_blank" rel="noopener noreferrer nofollow">` "so the bootstrap parity
holds". The corpus has both forms: section 9's guidance uses plain markdown links (three of them),
while tips and examples carry raw `<a target="_blank" …>` tags (ISS-007). Rewriting would break
parity on section 9, the section that gates phase 2, so the phase-2 generator passes every link
through unchanged.

**Affects.** [[section-9]] now; every section page with plain external links at its cut-over.

**Evidence.** `_pages/section-9.md`: `[architecture decision record](https://thinkrelevance.com/…)`,
`[Nygard 2011](https://cognitect.com/…)`, `[ADR Github collection](https://adr.github.io/)`.

**Options.**
1. Keep pass-through; decide with ISS-007 whether bodies should hold plain markdown links only and
   let the site's layout or a small script open external links in a new tab — no parity break.
2. Implement the rewrite after all section cut-overs, as one deliberate parity break with its own
   PR — every page's HTML changes once.
3. Drop the target-blank convention for markdown links — raw `<a>` tags stay as they are.

**Resolution.**
```

- [x] **Step 7: Index line and lint**

In `docs-arc42-brain/_system/index.md`, under `## Issues`, directly after the `ISS-010` line, add:

```markdown
- [ISS-011](../wiki/issues/ISS-011-external-link-rewrite-deferred.md) — open, contradiction: the generator does not rewrite external markdown links (spec §4.4) because section 9's parity depends on them staying plain
```

Run: `make brain-lint`
Expected: last line `33 findings, 0 errors, 33 warnings` (ISS-011 links only a section, which is exempt from the reciprocity warning).

- [x] **Step 8: Commit**

```bash
git add docs-arc42-brain/_system/generate/braingen/emit_body.py docs-arc42-brain/_system/generate/braingen/compare.py docs-arc42-brain/_system/generate/tests/test_emit_body.py docs-arc42-brain/_system/generate/tests/test_compare.py docs-arc42-brain/wiki/issues/ISS-011-external-link-rewrite-deferred.md docs-arc42-brain/_system/index.md docs/superpowers/plans/2026-09-18-docs-arc42-brain-phase-2-generator.md
git commit -m "brain: body transforms (callouts, directives, images, foot, marker) and the per-file parity rule; ISS-011

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
git log -1 --format=%B | tail -1
```

---

### Task 3: Front matter and the section emitter

Model: Haiku.

**Files:**
- Create: `docs-arc42-brain/_system/generate/braingen/emit.py`
- Create: `docs-arc42-brain/_system/generate/tests/vaultkit.py`
- Create: `docs-arc42-brain/_system/generate/tests/test_emit_section.py`
- Modify: `docs-arc42-brain/_system/generate/tests/test_roundtrip.py` (remove `@SECTIONS_PENDING` and its definition)

**Interfaces:**
- Consumes: `emit_body.marker`, `emit_body.section_document_body`; `parse.Page` (`.meta`, `.body`, `.path`, `.slug`), `parse.Vault` (`.rel(path) -> str`, `.pages`).
- Produces: `emit.Output(rel: str, text: str, source: str)` (frozen dataclass; `rel` site-relative, `source` vault-relative); `yaml_scalar(value, quote=False) -> str`; `render_frontmatter(items: list[tuple[str, object]], quoted: frozenset[str] = frozenset()) -> str` (a `related` item renders as a list of `{kind, title, url}`, omitted when empty, `url` omitted when empty); `document(front, source, body) -> str`; `emit_section(vault, page) -> Output`.
- Produces (tests): `tests/vaultkit.py` with `source`, `section`, `tip`, `example`, `term`, `keyword`, `system`, `asset` builders.

- [x] **Step 1: Write the test kit**

Create `docs-arc42-brain/_system/generate/tests/vaultkit.py`:

```python
"""Small vaults for the emitter, generator and parity tests.

Every page is written with the importer's write_page, so it looks exactly like
an imported page. Defaults describe a published section 9 with one callout, an
examples directive and the examples-link directive.
"""
from __future__ import annotations

from pathlib import Path

from braingen.importer import write_page

DAY = "2026-09-18"
SOURCE = "[[SRC-001-test]]"
SECTION_BODY = (
    "# 9. Architecture Decisions\n\n"
    "> [!arc42-help]\n"
    "> ## Background (on ADRs)\n"
    "> Text.\n"
    ">\n"
    "> %% examples: decisions %%\n"
    ">\n\n"
    "%% examples-link %%\n\n"
    "_&lt;describe here >_\n"
)


def _common(id_: str, type_: str, title: str, status: str) -> dict:
    return {"id": id_, "type": type_, "title": title, "status": status, "created": DAY,
            "updated": DAY, "sources": [SOURCE], "related": []}


def source(root: Path) -> None:
    meta = {"id": "SRC-001", "type": "source", "title": "Test source", "status": "ingested",
            "created": DAY, "updated": DAY, "origin": "raw/test/", "files": []}
    write_page(root / "raw/sources/SRC-001-test.md", meta, "Test.\n")


def section(root: Path, n: int = 9, body: str = SECTION_BODY, status: str = "published", **extra) -> None:
    meta = _common(f"section-{n}", "section", f"{n} - Architecture decisions", status)
    meta.update({"number": n, "name": "Architecture Decisions", "category": "decisions",
                 "posts-dir": f"{n:02d}-decisions", "permalink": f"/section-{n}/", "order": n + 4,
                 "faq-topic": "fundamental architecture and design decisions"})
    meta.update(extra)
    write_page(root / "wiki/sections" / f"section-{n}.md", meta, body)


def tip(root: Path, id_: str = "9-1", body: str = "Some tip.\n", status: str = "published", **extra) -> None:
    meta = _common(id_, "tip", f"Tip {id_}: Do it!", status)
    meta.update({"section": "[[section-9]]", "keywords": [], "terms": [], "legacy-tags": [],
                 "date": "2016-03-01", "permalink": f"/tips/{id_}/"})
    meta.update(extra)
    write_page(root / "wiki/tips" / f"tip-{id_}.md", meta, body)


def example(root: Path, id_: str = "09-decision-example-x", body: str = "An example.\n",
            status: str = "published", **extra) -> None:
    meta = _common(id_, "example", "Example Decision: X", status)
    meta.update({"section": "[[section-9]]", "system": "", "example-category": "decisions",
                 "keywords": [], "terms": [], "legacy-tags": [], "permalink": "/examples/decision-x/"})
    meta.update(extra)
    write_page(root / "wiki/examples" / f"{id_}.md", meta, body)


def term(root: Path, slug: str, display: str, status: str = "review", legacy=(), aliases=()) -> None:
    meta = _common(slug, "term", display, status)
    meta.update({"term": display, "aliases": list(aliases), "legacy-tags": list(legacy), "home": "[[section-9]]"})
    write_page(root / "wiki/terms" / f"{slug}.md", meta, "A definition.\n")


def keyword(root: Path, slug: str, status: str = "draft") -> None:
    meta = _common(slug, "keyword", slug, status)
    meta.update({"description": "A facet.", "featured": False})
    write_page(root / "wiki/keywords" / f"{slug}.md", meta, "")


def system(root: Path, slug: str, name: str, url: str = "") -> None:
    meta = _common(slug, "system", name, "draft")
    meta.update({"name": name, "url": url})
    write_page(root / "wiki/systems" / f"{slug}.md", meta, "A system.\n")


def asset(root: Path, rel: str, data: bytes = b"\x89PNG test") -> None:
    """rel is below wiki/assets/, e.g. "sections/09/d.png"."""
    p = root / "wiki/assets" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
```

- [x] **Step 2: Write the failing test**

Create `docs-arc42-brain/_system/generate/tests/test_emit_section.py`:

```python
import pytest
import yaml

from braingen.emit import emit_section, render_frontmatter, yaml_scalar
from braingen.parse import load_vault
from tests import vaultkit as vk


def test_yaml_scalar_plain_when_safe_quoted_otherwise():
    assert yaml_scalar(13) == "13"
    assert yaml_scalar("/tips/9-1/") == "/tips/9-1/"
    assert yaml_scalar("/section-9/#background-on-adrs") == "/section-9/#background-on-adrs"
    assert yaml_scalar("9 - Architecture decisions") == "9 - Architecture decisions"
    assert yaml_scalar("Tip 9-2: Criteria!", quote=True) == '"Tip 9-2: Criteria!"'
    assert yaml_scalar("a: b") == '"a: b"'
    assert yaml_scalar("yes") == '"yes"'
    assert yaml_scalar("") == '""'
    assert yaml_scalar('say "hi"', quote=True) == '"say \\"hi\\""'
    with pytest.raises(TypeError):
        yaml_scalar(True)


def test_render_frontmatter_reads_back_and_omits_empty_related():
    related = [
        {"kind": "tip", "title": 'Tip 9-2: "quoted"', "url": "/tips/9-2/"},
        {"kind": "term", "title": "ADR", "url": ""},
    ]
    text = render_frontmatter([("layout", "post"), ("title", "T: x"), ("related", related)], quoted=frozenset({"title"}))
    assert text.startswith('---\nlayout: post\ntitle: "T: x"\nrelated:\n- kind: tip\n')
    assert text.endswith("---\n")
    assert yaml.safe_load(text.split("---\n")[1]) == {
        "layout": "post",
        "title": "T: x",
        "related": [
            {"kind": "tip", "title": 'Tip 9-2: "quoted"', "url": "/tips/9-2/"},
            {"kind": "term", "title": "ADR"},
        ],
    }
    assert "related" not in render_frontmatter([("layout", "post"), ("related", [])])


def test_emit_section(tmp_path):
    vk.section(tmp_path)
    vault = load_vault(tmp_path)

    out = emit_section(vault, vault.pages["section-9"])

    assert out.rel == "_pages/section-9.md"
    assert out.source == "wiki/sections/section-9.md"
    assert out.text == (
        "---\nlayout: arc42-doc-section\ntitle: 9 - Architecture decisions\npermalink: /section-9/\n"
        "number: 9\norder: 13\n---\n"
        "<!-- generated from docs-arc42-brain/wiki/sections/section-9.md — do not edit -->\n\n"
        "# 9. Architecture Decisions\n\n"
        '<div class="arc42-help" markdown="1">\n'
        "## Background (on ADRs)\nText.\n\n"
        '{% include example.md category="decisions" %}\n\n'
        "</div>\n\n"
        '{% include examples-link.html variant="inline" %}\n\n'
        "_&lt;describe here >_\n\n\n"
        "{% include further-info.md\n"
        '   category="decisions"\n'
        '   topic="fundamental architecture and design decisions"\n'
        '   faqlink="https://faq.arc42.org/category_c/#c-sec-9" %}\n'
    )
```

Run: `make brain-test`
Expected: collection error in `test_emit_section.py` (`No module named 'braingen.emit'`).

- [x] **Step 3: Write `emit.py` (section part)**

Create `docs-arc42-brain/_system/generate/braingen/emit.py`:

```python
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
```

- [x] **Step 4: Run the suite — the section round trip now XPASSes**

Run: `make brain-test`
Expected: `3 failed, 82 passed, 2 xfailed`; the three failures are `test_section_round_trip[5|10|11]` with `[XPASS(strict)] section emitter arrives in Task 3`. That is the round trip passing.

- [x] **Step 5: Remove the section xfail marker**

In `tests/test_roundtrip.py` delete the line
`SECTIONS_PENDING = pytest.mark.xfail(strict=True, raises=ImportError, reason="section emitter arrives in Task 3")`
and the decorator line `@SECTIONS_PENDING` above `@pytest.mark.parametrize("n", [5, 10, 11])`. Leave `CONTENT_PENDING` alone.

Run: `make brain-test`
Expected: `85 passed, 2 xfailed`.

- [x] **Step 6: Commit**

```bash
git add docs-arc42-brain/_system/generate/braingen/emit.py docs-arc42-brain/_system/generate/tests/vaultkit.py docs-arc42-brain/_system/generate/tests/test_emit_section.py docs-arc42-brain/_system/generate/tests/test_roundtrip.py docs/superpowers/plans/2026-09-18-docs-arc42-brain-phase-2-generator.md
git commit -m "brain: section emitter and front-matter rendering; sections 5, 10, 11 round-trip

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
git log -1 --format=%B | tail -1
```

---

### Task 4: Tags, related links, tip and example emitters

Model: Haiku.

**Files:**
- Modify: `docs-arc42-brain/_system/generate/braingen/emit.py` (imports, two constants, five functions appended)
- Create: `docs-arc42-brain/_system/generate/tests/test_emit_content.py`
- Modify: `docs-arc42-brain/_system/generate/tests/test_roundtrip.py` (remove `CONTENT_PENDING`)

**Interfaces:**
- Consumes: Task 3's `Output`, `render_frontmatter`, `document`; `emit_body.content_body`; `Page.links_in(key) -> list[WikiLink]`, `Page.headings` (`.text`, `.anchor`), `Page.status`; `wikilinks.WikiLink` (`.target`, `.heading`, `.label`).
- Produces: `section_of(vault, page) -> Page` (raises `ValueError` naming the page slug); `tags_for(vault, page) -> list[str]`; `related_for(vault, page, emitted: set[str], site_tags: set[str]) -> list[dict]`; `emit_tip(vault, page, emitted, site_tags) -> Output`; `emit_example(vault, page, emitted, site_tags) -> Output`. `emitted` = slugs of the tips/examples written in the same run; `site_tags` = tags carried by those tips.

- [x] **Step 1: Write the failing test**

Create `docs-arc42-brain/_system/generate/tests/test_emit_content.py`:

```python
import frontmatter
import pytest

from braingen.emit import emit_example, emit_tip, related_for, section_of, tags_for
from braingen.parse import load_vault
from tests import vaultkit as vk

EMITTED = {"tip-9-1", "tip-9-2", "09-decision-example-x"}
SITE_TAGS = {"lean", "architecture-decision"}


def build(root):
    vk.section(root)
    vk.keyword(root, "lean")
    vk.term(root, "architecture-decision", "Architecture decision", legacy=["decision"])
    vk.term(root, "adr", "Architecture Decision Record (ADR)", status="retired")
    vk.system(root, "htmlsc", "HTML Sanity Checker", url="https://example.org/htmlsc")
    vk.tip(root, "9-1",
           section="[[section-9#Background (on ADRs)]]",
           keywords=["[[lean]]"],
           terms=["[[architecture-decision]]", "[[adr]]"],
           related=["[[tip-9-2]]", "[[tip-9-3]]", "[[architecture-decision]]",
                    "[[09-decision-example-x|The X example]]", "[[htmlsc]]", "[[section-4]]"])
    vk.tip(root, "9-2")
    vk.tip(root, "9-3", status="review")
    vk.example(root, keywords=["[[lean]]"], terms=["[[architecture-decision]]"], related=["[[tip-9-1]]"])
    return load_vault(root)


def test_tags_are_keywords_then_terms_without_retired(tmp_path):
    vault = build(tmp_path)
    assert tags_for(vault, vault.pages["tip-9-1"]) == ["lean", "architecture-decision"]


def test_related_starts_with_the_section_link_and_keeps_declared_order(tmp_path):
    vault = build(tmp_path)
    assert related_for(vault, vault.pages["tip-9-1"], EMITTED, SITE_TAGS) == [
        {"kind": "subsection", "title": "Background (on ADRs)", "url": "/section-9/#background-on-adrs"},
        {"kind": "tip", "title": "Tip 9-2: Do it!", "url": "/tips/9-2/"},
        {"kind": "term", "title": "Architecture decision", "url": "/keywords/#architecture-decision"},
        {"kind": "example", "title": "The X example", "url": "/examples/decision-x/"},
        {"kind": "system", "title": "HTML Sanity Checker", "url": "https://example.org/htmlsc"},
    ]


def test_related_term_has_no_url_when_no_post_carries_its_tag(tmp_path):
    vault = build(tmp_path)
    entries = related_for(vault, vault.pages["tip-9-1"], EMITTED, set())
    assert {"kind": "term", "title": "Architecture decision", "url": ""} in entries


def test_plain_section_link_is_a_section_entry(tmp_path):
    vault = build(tmp_path)
    assert related_for(vault, vault.pages["tip-9-2"], EMITTED, SITE_TAGS) == [
        {"kind": "section", "title": "9 - Architecture decisions", "url": "/section-9/"},
    ]


def test_section_of_rejects_a_link_that_is_not_a_section(tmp_path):
    vk.tip(tmp_path, "9-1", section="[[nowhere]]")
    vault = load_vault(tmp_path)
    with pytest.raises(ValueError, match="tip-9-1"):
        section_of(vault, vault.pages["tip-9-1"])


def test_emit_tip(tmp_path):
    vault = build(tmp_path)

    out = emit_tip(vault, vault.pages["tip-9-1"], EMITTED, SITE_TAGS)

    assert out.rel == "_posts/09-decisions/2016-03-01-t-9-1.md"
    assert out.source == "wiki/tips/tip-9-1.md"
    assert out.text.startswith(
        '---\nlayout: post\ntitle: "Tip 9-1: Do it!"\ntags: lean architecture-decision\n'
        "category: decisions\npermalink: /tips/9-1/\nrelated:\n- kind: subsection\n"
        '  title: "Background (on ADRs)"\n  url: /section-9/#background-on-adrs\n'
    )
    assert out.text.endswith(
        "---\n<!-- generated from docs-arc42-brain/wiki/tips/tip-9-1.md — do not edit -->\n\nSome tip.\n"
    )
    post = frontmatter.loads(out.text)
    assert len(post["related"]) == 5


def test_emit_example(tmp_path):
    vault = build(tmp_path)

    out = emit_example(vault, vault.pages["09-decision-example-x"], EMITTED, SITE_TAGS)

    assert out.rel == "_examples/09-decision-example-x.md"
    post = frontmatter.loads(out.text)
    assert post.metadata == {
        "layout": "post",
        "title": "Example Decision: X",
        "tags": "lean architecture-decision",
        "category": "decisions",
        "permalink": "/examples/decision-x/",
        "related": [
            {"kind": "section", "title": "9 - Architecture decisions", "url": "/section-9/"},
            {"kind": "tip", "title": "Tip 9-1: Do it!", "url": "/tips/9-1/"},
        ],
    }
    assert out.text.endswith("do not edit -->\n\nAn example.\n")
```

Run: `make brain-test`
Expected: collection error in `test_emit_content.py` (`cannot import name 'emit_example' from 'braingen.emit'`).

- [x] **Step 2: Extend `emit.py`**

Replace the import line `from .emit_body import marker, section_document_body` with:

```python
from .emit_body import content_body, marker, section_document_body
```

and directly after `from .parse import Page, Vault` add:

```python
from .wikilinks import WikiLink

KIND_BY_TYPE = {"section": "section", "tip": "tip", "example": "example", "faq": "faq",
                "term": "term", "keyword": "keyword", "system": "system"}
# Types whose pages exist on the site only once generated; a related link to an
# unpublished one would be dead, so it is left out.
PUBLISHED_ONLY = {"tip", "example", "faq"}
```

Append at the end of `emit.py`:

```python
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
```

- [x] **Step 3: Run the suite — the content round trips now XPASS**

Run: `make brain-test`
Expected: `2 failed, 92 passed`; the failures are `test_tip_round_trip` and `test_example_round_trip` with `[XPASS(strict)]`.

- [x] **Step 4: Remove the content xfail marker**

In `tests/test_roundtrip.py` delete the `CONTENT_PENDING = …` line and both `@CONTENT_PENDING` decorator lines. `import pytest` stays (the parametrize decorator uses it).

Run: `make brain-test`
Expected: `94 passed`.

- [x] **Step 5: Commit**

```bash
git add docs-arc42-brain/_system/generate/braingen/emit.py docs-arc42-brain/_system/generate/tests/test_emit_content.py docs-arc42-brain/_system/generate/tests/test_roundtrip.py docs/superpowers/plans/2026-09-18-docs-arc42-brain-phase-2-generator.md
git commit -m "brain: tip and example emitters with tags and structured related links

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
git log -1 --format=%B | tail -1
```

---

### Task 5: Idempotent generate with owned files, assets and drift check

Model: Haiku.

**Files:**
- Create: `docs-arc42-brain/_system/generate/braingen/generate.py`
- Create: `docs-arc42-brain/_system/generate/tests/test_generate.py`

**Interfaces:**
- Consumes: `emit.Output`, `emit_section`, `emit_tip`, `emit_example`, `section_of`, `tags_for`; `emit_body.is_generated`; `Page.images` (image paths as written in the body).
- Produces: `generate.plan(vault, statuses=frozenset({"published"}), section: int | None = None) -> Plan` (`Plan.outputs: list[Output]` sorted by `rel`, `Plan.assets: list[AssetOutput(rel, src)]`); `conflicts(vault, site, plan) -> list[str]`; `apply(vault, site, plan) -> Result(written, unchanged, deleted)` (raises `FileExistsError` starting with `refusing to overwrite:` and writes nothing when `conflicts` is non-empty); `check(vault, site, plan) -> list[str]`; `owned_files(site) -> list[str]`; `ASSET_MANIFEST = "_system/generated-assets.txt"`.

- [x] **Step 1: Write the failing test**

Create `docs-arc42-brain/_system/generate/tests/test_generate.py`:

```python
import pytest

from braingen.generate import ASSET_MANIFEST, apply, check, conflicts, owned_files, plan
from braingen.parse import load_vault
from tests import vaultkit as vk

TIP_1 = "_posts/09-decisions/2016-03-01-t-9-1.md"
TIP_2 = "_posts/09-decisions/2016-03-01-t-9-2.md"


def setup(tmp_path, **tip2):
    vault_root, site = tmp_path / "vault", tmp_path / "site"
    vk.source(vault_root)
    vk.section(vault_root)
    vk.tip(vault_root, "9-1", related=["[[tip-9-2]]"])
    vk.tip(vault_root, "9-2", related=["[[tip-9-1]]"], **tip2)
    vk.example(vault_root)
    (site / "_posts/09-decisions").mkdir(parents=True)
    (site / "_pages").mkdir()
    (site / "_examples").mkdir()
    return vault_root, site


def test_plan_emits_published_pages_only(tmp_path):
    vault_root, _ = setup(tmp_path, status="review")
    p = plan(load_vault(vault_root))
    assert [o.rel for o in p.outputs] == ["_examples/09-decision-example-x.md", "_pages/section-9.md", TIP_1]


def test_plan_with_statuses_and_section_filter(tmp_path):
    vault_root, _ = setup(tmp_path, status="review")
    vk.section(vault_root, n=4)
    vault = load_vault(vault_root)
    p = plan(vault, statuses=frozenset({"published", "review"}), section=9)
    assert [o.rel for o in p.outputs] == ["_examples/09-decision-example-x.md", "_pages/section-9.md", TIP_1, TIP_2]
    assert [o.rel for o in plan(vault, section=4).outputs] == ["_pages/section-4.md"]


def test_apply_writes_then_is_idempotent(tmp_path):
    vault_root, site = setup(tmp_path)
    first = apply(load_vault(vault_root), site, plan(load_vault(vault_root)))
    assert sorted(first.written) == ["_examples/09-decision-example-x.md", "_pages/section-9.md", TIP_1, TIP_2]
    second = apply(load_vault(vault_root), site, plan(load_vault(vault_root)))
    assert second.written == [] and second.deleted == []
    assert len(second.unchanged) == 4
    assert sorted(owned_files(site)) == sorted(first.written)


def test_unpublishing_deletes_the_generated_file_and_the_links_to_it(tmp_path):
    vault_root, site = setup(tmp_path)
    apply(load_vault(vault_root), site, plan(load_vault(vault_root)))
    vk.tip(vault_root, "9-2", related=["[[tip-9-1]]"], status="retired")

    res = apply(load_vault(vault_root), site, plan(load_vault(vault_root)))

    assert res.deleted == [TIP_2]
    assert res.written == [TIP_1]           # its related link to 9-2 is gone
    assert "/tips/9-2/" not in (site / TIP_1).read_text(encoding="utf-8")


def test_files_without_marker_are_never_touched(tmp_path):
    vault_root, site = setup(tmp_path)
    hand = site / "_posts/09-decisions/2016-03-01-t-9-9.md"
    hand.write_text("---\ntitle: hand\n---\nhand-written\n", encoding="utf-8")
    apply(load_vault(vault_root), site, plan(load_vault(vault_root)))
    assert hand.read_text(encoding="utf-8") == "---\ntitle: hand\n---\nhand-written\n"


def test_hand_written_original_blocks_the_whole_run(tmp_path):
    vault_root, site = setup(tmp_path)
    (site / TIP_2).write_text("---\ntitle: original\n---\nbody\n", encoding="utf-8")
    vault = load_vault(vault_root)

    assert conflicts(vault, site, plan(vault)) == [f"{TIP_2}: hand-written file; delete the original first (cut-over)"]
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        apply(vault, site, plan(vault))
    assert not (site / TIP_1).exists()      # nothing was written


def test_assets_are_copied_listed_and_removed_when_unreferenced(tmp_path):
    vault_root, site = setup(tmp_path)
    vk.asset(vault_root, "sections/09/d.png")
    vk.tip(vault_root, "9-1", body="![d](../assets/sections/09/d.png)\n", related=["[[tip-9-2]]"])

    res = apply(load_vault(vault_root), site, plan(load_vault(vault_root)))

    assert "assets/images/sections/09/d.png" in res.written
    assert (site / "assets/images/sections/09/d.png").read_bytes() == b"\x89PNG test"
    assert "{{ site.imageurl }}/09/d.png" in (site / TIP_1).read_text(encoding="utf-8")
    manifest = (vault_root / ASSET_MANIFEST).read_text(encoding="utf-8")
    assert manifest.splitlines()[1:] == ["assets/images/sections/09/d.png"]

    vk.tip(vault_root, "9-1", related=["[[tip-9-2]]"])
    res = apply(load_vault(vault_root), site, plan(load_vault(vault_root)))
    assert "assets/images/sections/09/d.png" in res.deleted
    assert not (site / "assets/images/sections/09/d.png").exists()


def test_hand_made_asset_with_other_content_is_a_conflict(tmp_path):
    vault_root, site = setup(tmp_path)
    vk.asset(vault_root, "sections/09/d.png")
    vk.tip(vault_root, "9-1", body="![d](../assets/sections/09/d.png)\n")
    hand = site / "assets/images/sections/09/d.png"
    hand.parent.mkdir(parents=True)
    hand.write_bytes(b"other")
    vault = load_vault(vault_root)
    assert conflicts(vault, site, plan(vault)) == ["assets/images/sections/09/d.png: hand-made asset with different content"]


def test_check_is_clean_after_generate_and_reports_every_drift(tmp_path):
    vault_root, site = setup(tmp_path)
    vault = load_vault(vault_root)
    apply(vault, site, plan(vault))
    assert check(vault, site, plan(vault)) == []

    (site / TIP_1).write_text((site / TIP_1).read_text(encoding="utf-8") + "edited\n", encoding="utf-8")
    (site / TIP_2).unlink()
    stale = site / "_posts/09-decisions/2016-03-01-t-9-7.md"
    stale.write_text((site / "_pages/section-9.md").read_text(encoding="utf-8"), encoding="utf-8")

    assert check(vault, site, plan(vault)) == [
        f"{TIP_1}: hand-edited or stale, run make generate (edit wiki/tips/tip-9-1.md instead)",
        f"{TIP_2}: missing, run make generate",
        "_posts/09-decisions/2016-03-01-t-9-7.md: generated file without a published brain page, run make generate",
    ]
```

Run: `make brain-test`
Expected: collection error (`No module named 'braingen.generate'`).

- [x] **Step 2: Write `generate.py`**

Create `docs-arc42-brain/_system/generate/braingen/generate.py`:

```python
"""Generate the Jekyll content files from the vault, idempotently.

`make generate` owns exactly the files that carry the marker line (see
emit_body.MARKER_PREFIX) plus the assets listed in the asset manifest; everything
else in the site is never written or deleted.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .emit import Output, emit_example, emit_section, emit_tip, section_of, tags_for
from .emit_body import is_generated
from .parse import Page, Vault

OWNED_GLOBS = ["_pages/section-*.md", "_posts/*/*.md", "_examples/*.md"]
ASSET_MANIFEST = "_system/generated-assets.txt"   # vault-relative
ASSET_TARGETS = {"sections": "assets/images/sections", "examples": "assets/images/examples"}


@dataclass(frozen=True)
class AssetOutput:
    rel: str      # site-relative destination, e.g. "assets/images/sections/10/q42.svg"
    src: Path     # absolute source under wiki/assets/


@dataclass
class Plan:
    outputs: list[Output] = field(default_factory=list)
    assets: list[AssetOutput] = field(default_factory=list)


@dataclass
class Result:
    written: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)


def _selected(page: Page, statuses: set[str], section: int | None, vault: Vault) -> bool:
    if page.status not in statuses:
        return False
    if section is None:
        return True
    sec = page if page.type == "section" else section_of(vault, page)
    return int(sec.meta["number"]) == section


def plan(vault: Vault, statuses: set[str] = frozenset({"published"}), section: int | None = None) -> Plan:
    """Everything one run writes. `statuses`/`section` exist for the parity check."""
    sections = [p for p in vault.by_type("section") if _selected(p, statuses, section, vault)]
    tips = [p for p in vault.by_type("tip") if _selected(p, statuses, section, vault)]
    examples = [p for p in vault.by_type("example") if _selected(p, statuses, section, vault)]
    emitted = {p.slug for p in tips + examples}
    site_tags = {t for p in tips for t in tags_for(vault, p)}
    out = Plan()
    out.outputs += [emit_section(vault, p) for p in sections]
    out.outputs += [emit_tip(vault, p, emitted, site_tags) for p in tips]
    out.outputs += [emit_example(vault, p, emitted, site_tags) for p in examples]
    out.outputs.sort(key=lambda o: o.rel)
    out.assets = _assets(vault, sections + tips + examples)
    return out


def _assets(vault: Vault, pages: list[Page]) -> list[AssetOutput]:
    seen: dict[str, AssetOutput] = {}
    for p in pages:
        for img in p.images:
            src = (p.path.parent / img).resolve()
            try:
                rel = src.relative_to((vault.root / "wiki/assets").resolve())
            except ValueError:
                continue
            kind, rest = rel.parts[0], Path(*rel.parts[1:])
            if kind in ASSET_TARGETS:
                dst = f"{ASSET_TARGETS[kind]}/{rest.as_posix()}"
                seen[dst] = AssetOutput(dst, src)
    return [seen[k] for k in sorted(seen)]


def owned_files(site: Path) -> list[str]:
    """Site-relative paths of every content file that carries the marker."""
    found: list[str] = []
    for pattern in OWNED_GLOBS:
        for f in sorted(site.glob(pattern)):
            if is_generated(f.read_text(encoding="utf-8")):
                found.append(f.relative_to(site).as_posix())
    return found


def read_asset_manifest(vault: Vault) -> list[str]:
    f = vault.root / ASSET_MANIFEST
    if not f.exists():
        return []
    return [l.strip() for l in f.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]


def write_asset_manifest(vault: Vault, rels: list[str]) -> None:
    header = "# assets written by `make generate`; it deletes these, and only these, when stale\n"
    f = vault.root / ASSET_MANIFEST
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(header + "".join(f"{r}\n" for r in sorted(rels)), encoding="utf-8")


def conflicts(vault: Vault, site: Path, p: Plan) -> list[str]:
    """Hand-made files a run would overwrite. `apply` writes nothing while any exist."""
    site = Path(site)
    found: list[str] = []
    for o in p.outputs:
        f = site / o.rel
        if f.exists():
            current = f.read_text(encoding="utf-8")
            if current != o.text and not is_generated(current):
                found.append(f"{o.rel}: hand-written file; delete the original first (cut-over)")
    owned_assets = set(read_asset_manifest(vault))
    for a in p.assets:
        f = site / a.rel
        if f.exists() and a.rel not in owned_assets and f.read_bytes() != a.src.read_bytes():
            found.append(f"{a.rel}: hand-made asset with different content")
    return found


def apply(vault: Vault, site: Path, p: Plan) -> Result:
    """Write `p` into `site` and delete the stale files it owns. Idempotent."""
    site = Path(site)
    found = conflicts(vault, site, p)
    if found:
        raise FileExistsError("refusing to overwrite:\n  " + "\n  ".join(found))
    res = Result()
    for o in p.outputs:
        f = site / o.rel
        if f.exists() and f.read_text(encoding="utf-8") == o.text:
            res.unchanged.append(o.rel)
            continue
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(o.text, encoding="utf-8")
        res.written.append(o.rel)
    targets = {o.rel for o in p.outputs}
    for rel in owned_files(site):
        if rel not in targets:
            (site / rel).unlink()
            res.deleted.append(rel)

    old_assets = set(read_asset_manifest(vault))
    new_assets = {a.rel for a in p.assets}
    for a in p.assets:
        f = site / a.rel
        data = a.src.read_bytes()
        if f.exists() and f.read_bytes() == data:
            res.unchanged.append(a.rel)
            continue
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(data)
        res.written.append(a.rel)
    for rel in sorted(old_assets - new_assets):
        f = site / rel
        if f.exists():
            f.unlink()
            res.deleted.append(rel)
    if old_assets != new_assets:
        write_asset_manifest(vault, sorted(new_assets))
    return res


def check(vault: Vault, site: Path, p: Plan) -> list[str]:
    """Problems that make the committed generated files differ from a fresh generate."""
    site = Path(site)
    problems: list[str] = []
    targets = {o.rel: o for o in p.outputs}
    for o in p.outputs:
        f = site / o.rel
        if not f.exists():
            problems.append(f"{o.rel}: missing, run make generate")
        elif f.read_text(encoding="utf-8") != o.text:
            current = f.read_text(encoding="utf-8")
            what = "hand-edited or stale" if is_generated(current) else "hand-written file where a generated one belongs"
            problems.append(f"{o.rel}: {what}, run make generate (edit {o.source} instead)")
    for rel in owned_files(site):
        if rel not in targets:
            problems.append(f"{rel}: generated file without a published brain page, run make generate")
    listed = set(read_asset_manifest(vault))
    for a in p.assets:
        f = site / a.rel
        if not f.exists() or f.read_bytes() != a.src.read_bytes():
            problems.append(f"{a.rel}: differs from {a.src.name} in wiki/assets, run make generate")
        elif a.rel not in listed:
            problems.append(f"{a.rel}: not in {ASSET_MANIFEST}, run make generate")
    return problems
```

- [x] **Step 3: Run the suite**

Run: `make brain-test`
Expected: `103 passed`.

- [x] **Step 4: Commit**

```bash
git add docs-arc42-brain/_system/generate/braingen/generate.py docs-arc42-brain/_system/generate/tests/test_generate.py docs/superpowers/plans/2026-09-18-docs-arc42-brain-phase-2-generator.md
git commit -m "brain: idempotent generate that owns only marked files and manifest-listed assets; drift check

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
git log -1 --format=%B | tail -1
```

---

### Task 6: Parity check per section, with the section-9 integration test

Model: Sonnet (the integration test runs against the real vault and `raw/ingested/`; if it fails, diagnose against real data instead of changing the assertion).

**Files:**
- Create: `docs-arc42-brain/_system/generate/braingen/parity.py`
- Create: `docs-arc42-brain/_system/generate/tests/test_parity.py`

**Interfaces:**
- Consumes: `generate.plan`, `generate.Plan`; `compare.FileReport`, `compare_file`, `split_tags`; `Page.headings` (`.anchor`, `.text`), `Page.directives` (`.name`, `.arg`).
- Produces: `parity.PARITY_STATUSES = frozenset({"draft", "review", "published"})`; `EXPECTED_ANCHORS`; `SectionReport(section, files: list[FileReport], notes: list[str])` with `.ok`; `check_section(vault, site, section: int, out_dir: Path) -> SectionReport` (writes into `out_dir/section-N/`); `format_report(rep) -> str` whose first line is `section N: PASS|FAIL (K files compared)`; `alias_table(vault)`, `anchor_check`, `not_ingested`, `keyword_page_changes(site, plan) -> (lost, gained)`.

- [x] **Step 1: Write the failing test**

Create `docs-arc42-brain/_system/generate/tests/test_parity.py`:

```python
import shutil
from pathlib import Path

import yaml

from braingen import parity
from braingen.generate import plan
from braingen.parity import PARITY_STATUSES, check_section, format_report, keyword_page_changes
from braingen.parse import load_vault
from tests import vaultkit as vk

# tests/ -> generate/ -> _system/ -> docs-arc42-brain/
REPO_VAULT = Path(__file__).resolve().parents[3]
BUILT_IDS = ["9-architecture-decisions", "background-on-adrs", "examples",
             "practical-tips", "related-questions", "complete-examples"]


def setup(tmp_path):
    vault_root, site = tmp_path / "vault", tmp_path / "site"
    vk.section(vault_root, status="draft")
    vk.term(vault_root, "architecture-decision", "Architecture decision", legacy=["decision"])
    vk.tip(vault_root, "9-1", status="review", terms=["[[architecture-decision]]"])
    vk.example(vault_root, status="review")
    return vault_root, site


def write_originals(vault_root, site, tags="decision"):
    """The site as it was before the brain: generated text minus marker, legacy tags."""
    for o in plan(load_vault(vault_root), statuses=PARITY_STATUSES).outputs:
        lines = [l for l in o.text.splitlines() if not l.startswith("<!-- generated")]
        text = "\n".join(lines) + "\n"
        if o.rel.startswith("_posts/"):
            text = text.replace("tags: architecture-decision", f"tags: {tags}")
        f = site / o.rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")


def built_page(site, ids):
    f = site / "_site/section-9/index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("\n".join(f'<h2 class="x" id="{i}">t</h2>' for i in ids), encoding="utf-8")


def test_matching_site_passes_whatever_the_status(tmp_path):
    vault_root, site = setup(tmp_path)
    write_originals(vault_root, site)

    rep = check_section(load_vault(vault_root), site, 9, tmp_path / "out")

    assert rep.ok
    assert [f.rel for f in rep.files] == ["_examples/09-decision-example-x.md", "_pages/section-9.md",
                                          "_posts/09-decisions/2016-03-01-t-9-1.md"]
    assert (tmp_path / "out/section-9/_pages/section-9.md").exists()
    assert "anchors not compared: _site/section-9/index.html not built (make site)" in rep.notes
    tip = rep.files[2]
    assert tip.notes[0] == "tags on the site: -['decision'] +['architecture-decision']"
    assert "keyword page loses tags: ['decision']" in rep.notes
    assert "keyword page gains tags: ['architecture-decision']" in rep.notes


def test_changed_value_fails_and_is_formatted(tmp_path):
    vault_root, site = setup(tmp_path)
    write_originals(vault_root, site)
    f = site / "_posts/09-decisions/2016-03-01-t-9-1.md"
    f.write_text(f.read_text(encoding="utf-8").replace("/tips/9-1/", "/tips/old/"), encoding="utf-8")

    rep = check_section(load_vault(vault_root), site, 9, tmp_path / "out")

    assert not rep.ok
    text = format_report(rep)
    assert text.startswith("section 9: FAIL (3 files compared)")
    assert "FAIL _posts/09-decisions/2016-03-01-t-9-1.md" in text
    assert "! front matter: permalink: '/tips/old/' -> '/tips/9-1/'" in text


def test_brain_page_without_original_is_new_and_site_file_without_page_is_not_ingested(tmp_path):
    vault_root, site = setup(tmp_path)
    write_originals(vault_root, site)
    vk.tip(vault_root, "9-2", status="review")
    (site / "_posts/09-decisions/2016-03-01-t-9-9.md").write_text("---\ntags: x\n---\nold\n", encoding="utf-8")
    (site / "_examples/09-other.md").write_text("---\ncategory: decisions\n---\nold\n", encoding="utf-8")

    rep = check_section(load_vault(vault_root), site, 9, tmp_path / "out")

    assert rep.ok
    new = [f for f in rep.files if f.rel == "_posts/09-decisions/2016-03-01-t-9-2.md"][0]
    assert new.notes == ["new: no original on the site"]
    assert "not ingested: 2 site files of this section have no brain page" in rep.notes


def test_section_not_in_brain(tmp_path):
    vault_root, site = setup(tmp_path)
    rep = check_section(load_vault(vault_root), site, 5, tmp_path / "out")
    assert rep.ok and rep.files == []
    assert rep.notes == ["section-5 is not in the brain"]


def test_keyword_page_changes_ignore_tags_still_used_elsewhere(tmp_path):
    vault_root, site = setup(tmp_path)
    write_originals(vault_root, site)
    other = site / "_posts/04-strategy/2016-01-01-t-4-1.md"
    other.parent.mkdir(parents=True)
    other.write_text("---\ntags: decision\n---\nx\n", encoding="utf-8")
    lost, gained = keyword_page_changes(site, plan(load_vault(vault_root), statuses=PARITY_STATUSES))
    assert lost == set()
    assert gained == {"architecture-decision"}


def test_anchors_against_the_built_page(tmp_path, monkeypatch):
    vault_root, site = setup(tmp_path)
    write_originals(vault_root, site)
    built_page(site, BUILT_IDS)
    assert check_section(load_vault(vault_root), site, 9, tmp_path / "out").ok

    built_page(site, [i for i in BUILT_IDS if i != "background-on-adrs"] + ["background"])
    rep = check_section(load_vault(vault_root), site, 9, tmp_path / "out")
    assert not rep.ok
    assert rep.files[-1].problems == ["anchor background-on-adrs ('Background (on ADRs)') not on the built page"]

    monkeypatch.setattr(parity, "EXPECTED_ANCHORS", [(9, "background-on-adrs", "background", "test reason")])
    rep = check_section(load_vault(vault_root), site, 9, tmp_path / "out")
    assert rep.ok
    assert "expected difference: anchor background-on-adrs is background on the site (test reason)" in rep.notes


def site_from_raw(tmp: Path, section: int) -> Path:
    """Rebuild the section's pre-brain site files from the immutable raw/ingested/ batches."""
    site = tmp / "site"
    for batch in sorted((REPO_VAULT / "raw/ingested").glob(f"section-{section}-*")):
        manifest = yaml.safe_load((batch / "manifest.yaml").read_text(encoding="utf-8"))
        for sub, dest in (("pages", "_pages"), ("posts", f"_posts/{manifest['posts_dir']}"), ("examples", "_examples")):
            for f in sorted((batch / sub).glob("*.md")):
                target = site / dest / f.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, target)
    return site


def test_section_9_parity_against_the_ingested_originals(tmp_path):
    """Brain spec §10: the section-9 parity, kept after cut-over so the emitters cannot regress."""
    site = site_from_raw(tmp_path, 9)

    rep = check_section(load_vault(REPO_VAULT), site, 9, tmp_path / "parity")

    assert [f.rel for f in rep.files if not f.ok] == [], format_report(rep)
    assert len(rep.files) == 14
    assert not [n for n in rep.notes if n.startswith("not ingested")]
```

Run: `make brain-test`
Expected: collection error (`No module named 'braingen.parity'`).

- [x] **Step 2: Write `parity.py`**

Create `docs-arc42-brain/_system/generate/braingen/parity.py`:

```python
"""Parity check (brain spec §6): generate one section, compare it with the site.

The section's pages are generated whatever their status (retired excepted)
into <out>/section-N/, and every generated file is compared with the file at
the same path in the site by compare.compare_file. On top of that the report
carries, as notes that never fail:

- heading anchors vs. the built page in _site/ (if built; EXPECTED_ANCHORS
  lists the known divergences, anything else fails);
- site files of the section that have no brain page yet ("not ingested");
- tags that appear on or disappear from the /keywords/ page, which lists the
  tags of posts only (site.tags).
"""
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import frontmatter

from .compare import FileReport, compare_file, split_tags
from .generate import Plan, plan
from .parse import Vault

PARITY_STATUSES = frozenset({"draft", "review", "published"})
H_ID_RE = re.compile(r'<h[1-6][^>]*\sid="([^"]*)"')

# (section number, brain anchor, anchor on the built site, why)
EXPECTED_ANCHORS: list[tuple[int, str, str, str]] = [
    (7, "motivation-1", "motivation",
     'kramdown numbers headings inside markdown="1" divs separately; braingen keeps one counter'),
]


@dataclass
class SectionReport:
    section: int
    files: list[FileReport] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(f.ok for f in self.files)


def alias_table(vault: Vault) -> dict[str, str]:
    """Legacy tag / alias / slug → the tag the brain emits for it."""
    table: dict[str, str] = {}
    for p in vault.by_type("keyword"):
        table[p.slug] = p.slug
    for p in vault.by_type("term"):
        table[p.slug] = p.slug
        for a in list(p.meta.get("aliases") or []) + list(p.meta.get("legacy-tags") or []):
            table[str(a)] = p.slug
    return table


def anchor_check(vault: Vault, site: Path, section: int) -> tuple[list[str], list[str]]:
    """(problems, notes) from comparing the brain's anchors with the built page."""
    page = vault.pages.get(f"section-{section}")
    built = site / "_site" / f"section-{section}" / "index.html"
    if page is None:
        return [], []
    if not built.exists():
        return [], [f"anchors not compared: _site/section-{section}/index.html not built (make site)"]
    ids = set(H_ID_RE.findall(built.read_text(encoding="utf-8")))
    problems: list[str] = []
    notes: list[str] = []
    for h in page.headings:
        if not h.anchor or h.anchor in ids:
            continue
        known = [x for x in EXPECTED_ANCHORS if x[0] == section and x[1] == h.anchor and x[2] in ids]
        if known:
            notes.append(f"expected difference: anchor {h.anchor} is {known[0][2]} on the site ({known[0][3]})")
        else:
            problems.append(f"anchor {h.anchor} ('{h.text}') not on the built page")
    return problems, notes


def not_ingested(vault: Vault, site: Path, section: int, generated: set[str]) -> list[str]:
    """Site files of this section (tips by posts-dir, examples by directive category) without a brain page."""
    sec = vault.pages.get(f"section-{section}")
    if sec is None:
        return []
    missing: list[str] = []
    for f in sorted((site / "_posts" / str(sec.meta["posts-dir"])).glob("*.md")):
        if f.relative_to(site).as_posix() not in generated:
            missing.append(f.relative_to(site).as_posix())
    cats = {d.arg for d in sec.directives if d.name == "examples" and d.arg}
    for f in sorted((site / "_examples").glob("*.md")):
        rel = f.relative_to(site).as_posix()
        if rel not in generated and frontmatter.load(f).get("category") in cats:
            missing.append(rel)
    return missing


def keyword_page_changes(site: Path, p: Plan) -> tuple[set[str], set[str]]:
    """(lost, gained) tags of the /keywords/ page if `p`'s posts replaced the site's."""
    generated = {o.rel: o.text for o in p.outputs if o.rel.startswith("_posts/")}
    before: set[str] = set()
    after: set[str] = set()
    for f in sorted((site / "_posts").glob("*/*.md")):
        tags = set(split_tags(frontmatter.load(f).get("tags")))
        before |= tags
        if f.relative_to(site).as_posix() not in generated:
            after |= tags
    for text in generated.values():
        after |= set(split_tags(frontmatter.loads(text).get("tags")))
    return before - after, after - before


def check_section(vault: Vault, site: Path, section: int, out_dir: Path) -> SectionReport:
    site = Path(site)
    rep = SectionReport(section)
    if f"section-{section}" not in vault.pages:
        rep.notes.append(f"section-{section} is not in the brain")
        return rep
    p = plan(vault, statuses=PARITY_STATUSES, section=section)
    target = Path(out_dir) / f"section-{section}"
    if target.exists():
        shutil.rmtree(target)
    aliases = alias_table(vault)
    for o in p.outputs:
        dst = target / o.rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(o.text, encoding="utf-8")
        orig = site / o.rel
        if orig.exists():
            rep.files.append(compare_file(o.rel, orig.read_text(encoding="utf-8"), o.text, section, aliases))
        else:
            rep.files.append(FileReport(o.rel, notes=["new: no original on the site"]))
    problems, notes = anchor_check(vault, site, section)
    if problems:
        rep.files.append(FileReport(f"_site/section-{section}/index.html", ok=False, problems=problems))
    rep.notes += notes
    missing = not_ingested(vault, site, section, {o.rel for o in p.outputs})
    if missing:
        rep.notes.append(f"not ingested: {len(missing)} site files of this section have no brain page")
    lost, gained = keyword_page_changes(site, p)
    if lost:
        rep.notes.append(f"keyword page loses tags: {sorted(lost)}")
    if gained:
        rep.notes.append(f"keyword page gains tags: {sorted(gained)}")
    return rep


def format_report(rep: SectionReport) -> str:
    lines = [f"section {rep.section}: {'PASS' if rep.ok else 'FAIL'} ({len(rep.files)} files compared)"]
    for f in rep.files:
        if f.problems or f.notes:
            lines.append(f"  {'ok  ' if f.ok else 'FAIL'} {f.rel}")
            lines += [f"       ! {x}" for x in f.problems]
            lines += [f"       - {x}" for x in f.notes]
    lines += [f"  - {x}" for x in rep.notes]
    return "\n".join(lines)
```

- [x] **Step 3: Run the suite**

Run: `make brain-test`
Expected: `110 passed`.

- [x] **Step 4: Run the parity check on the real repo, all twelve sections (no CLI yet)**

Run from the repo root:

```bash
uv run --directory docs-arc42-brain/_system/generate python -c "
from pathlib import Path
from braingen.parse import load_vault
from braingen.parity import check_section, format_report
root = Path('$(pwd)')
v = load_vault(root / 'docs-arc42-brain')
for n in range(1, 13):
    print(format_report(check_section(v, root, n, root / 'docs-arc42-brain/build/parity')))
"
```

Expected: twelve lines starting `section N: PASS`; section 7 has the note `expected difference: anchor motivation-1 is motivation on the site …` (only if `_site/` is built, otherwise `anchors not compared …`); section 10's `_pages/section-10.md` has `expected difference: hard-coded image path …`; section 11's has `normalised: 0 blank lines after the front matter …`; section 9 compares 14 files and has no `not ingested` note. Paste the full output into your report. `docs-arc42-brain/build/` is gitignored; do not commit it.

- [x] **Step 5: Commit**

```bash
git add docs-arc42-brain/_system/generate/braingen/parity.py docs-arc42-brain/_system/generate/tests/test_parity.py docs/superpowers/plans/2026-09-18-docs-arc42-brain-phase-2-generator.md
git commit -m "brain: per-section parity check with anchor, not-ingested and keyword-page notes; section-9 integration test

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
git log -1 --format=%B | tail -1
```

---

### Task 7: CLI commands, make targets, `make check`, workflow docs

Model: Sonnet.

**Files:**
- Modify: `docs-arc42-brain/_system/generate/braingen/cli.py`
- Create: `docs-arc42-brain/_system/generate/tests/test_cli_generate.py`
- Modify: `docs-arc42-brain/_system/brain.mk`
- Modify: `Makefile` (root): the `check` target only
- Modify: `docs-arc42-brain/CLAUDE.md` (the `## Commands` block)
- Modify: `docs-arc42-brain/_system/workflows/cutover.md` (full rewrite)
- Modify: `docs-arc42-brain/_system/log.md` (format comment line only)

**Interfaces:**
- Consumes: `generate.plan`, `apply`, `check`; `parity.check_section`, `format_report`; `lint.lint`.
- Produces: `braingen generate --vault V --site S` (exit 1 on lint errors or conflicts); `braingen generate-check --vault V --site S --out DIR [--section N]` (exit 1 if any section fails; default: every section page in the brain); `braingen check-generated --vault V --site S` (exit 1 on any drift). Make: `generate`, `generate-check [SECTION=N]`, `brain-check-generated`; `make check` runs `brain-lint` and `brain-check-generated` before the site build. These are the targets the phase-3 dashboard calls (`make brain-lint && make generate`; preview = the parity generator into `build/parity/`).

- [x] **Step 1: Write the failing test**

Create `docs-arc42-brain/_system/generate/tests/test_cli_generate.py`:

```python
from braingen.cli import main
from tests import vaultkit as vk


def build(tmp_path):
    vault_root, site = tmp_path / "vault", tmp_path / "site"
    vk.source(vault_root)
    vk.section(vault_root)
    vk.tip(vault_root, "9-1")
    vk.example(vault_root)
    return vault_root, site


def test_generate_then_check_generated_then_parity(tmp_path, capsys):
    vault_root, site = build(tmp_path)
    args = ["--vault", str(vault_root), "--site", str(site)]

    assert main(["check-generated", *args]) == 1
    assert "_pages/section-9.md: missing, run make generate" in capsys.readouterr().out

    assert main(["generate", *args]) == 0
    assert "3 written, 0 deleted, 0 unchanged" in capsys.readouterr().out

    assert main(["check-generated", *args]) == 0
    assert "generated files: 0 problems" in capsys.readouterr().out

    assert main(["generate-check", *args, "--section", "9", "--out", str(tmp_path / "parity")]) == 0
    out = capsys.readouterr().out
    assert "section 9: PASS (3 files compared)" in out
    assert "1 sections checked, 0 failed" in out
    assert (tmp_path / "parity/section-9/_pages/section-9.md").exists()


def test_generate_stops_on_lint_errors(tmp_path, capsys):
    vault_root, site = tmp_path / "vault", tmp_path / "site"
    vk.section(vault_root)   # its source page does not exist: unresolved link, a lint error
    assert main(["generate", "--vault", str(vault_root), "--site", str(site)]) == 1
    assert "generate stopped: 1 lint errors" in capsys.readouterr().out
    assert not site.exists()


def test_generate_refuses_to_overwrite_a_hand_written_original(tmp_path, capsys):
    vault_root, site = build(tmp_path)
    (site / "_pages").mkdir(parents=True)
    (site / "_pages/section-9.md").write_text("---\ntitle: hand\n---\nhand\n", encoding="utf-8")
    assert main(["generate", "--vault", str(vault_root), "--site", str(site)]) == 1
    assert "refusing to overwrite" in capsys.readouterr().out
```

Run: `make brain-test`
Expected: 3 failures in `test_cli_generate.py` (argparse `invalid choice: 'check-generated'`, raised as `SystemExit: 2`).

- [x] **Step 2: Extend `cli.py`**

Change the module docstring to:

```python
"""braingen command line: lint | raw | import | generate | generate-check | check-generated."""
```

Insert these three functions directly above `def build_parser()`:

```python
def cmd_generate(args: argparse.Namespace) -> int:
    from .generate import apply, plan

    vault = load_vault(args.vault)
    errors = [x for x in lint(vault) if x.level == "error"]
    if errors:
        for x in errors:
            print(x)
        print(f"generate stopped: {len(errors)} lint errors")
        return 1
    try:
        res = apply(vault, args.site, plan(vault))
    except FileExistsError as e:
        print(e)
        return 1
    for rel in res.written:
        print(f"wrote   {rel}")
    for rel in res.deleted:
        print(f"deleted {rel}")
    print(f"{len(res.written)} written, {len(res.deleted)} deleted, {len(res.unchanged)} unchanged")
    return 0


def cmd_generate_check(args: argparse.Namespace) -> int:
    from .parity import check_section, format_report

    vault = load_vault(args.vault)
    if args.section is not None:
        sections = [args.section]
    else:
        sections = sorted(int(p.meta["number"]) for p in vault.by_type("section"))
    failed = 0
    for n in sections:
        rep = check_section(vault, args.site, n, args.out)
        print(format_report(rep))
        failed += 0 if rep.ok else 1
    print(f"{len(sections)} sections checked, {failed} failed; generated files under {args.out}")
    return 1 if failed else 0


def cmd_check_generated(args: argparse.Namespace) -> int:
    from .generate import check, plan

    vault = load_vault(args.vault)
    problems = check(vault, args.site, plan(vault))
    for x in problems:
        print(x)
    print(f"generated files: {len(problems)} problems")
    return 1 if problems else 0
```

In `build_parser()`, replace the two lines

```python
    i.set_defaults(func=cmd_import)
    return ap
```

with

```python
    i.set_defaults(func=cmd_import)
    g = sub.add_parser("generate", help="write the Jekyll files of every published page")
    g.add_argument("--vault", type=Path, required=True)
    g.add_argument("--site", type=Path, required=True)
    g.set_defaults(func=cmd_generate)
    pc = sub.add_parser("generate-check", help="parity check: generate into --out and compare with the site")
    pc.add_argument("--vault", type=Path, required=True)
    pc.add_argument("--site", type=Path, required=True)
    pc.add_argument("--section", type=int, default=None, help="one section; default: every section in the brain")
    pc.add_argument("--out", type=Path, required=True, help="scratch folder, e.g. docs-arc42-brain/build/parity")
    pc.set_defaults(func=cmd_generate_check)
    cg = sub.add_parser("check-generated", help="fail if a generated file differs from a fresh generate")
    cg.add_argument("--vault", type=Path, required=True)
    cg.add_argument("--site", type=Path, required=True)
    cg.set_defaults(func=cmd_check_generated)
    return ap
```

Run: `make brain-test`
Expected: `113 passed`.

- [x] **Step 3: Make targets**

In `docs-arc42-brain/_system/brain.mk`, replace the line

```make
.PHONY: brain-test brain-lint brain-raw brain-import
```

with

```make
.PHONY: brain-test brain-lint brain-raw brain-import generate generate-check brain-check-generated
```

and append at the end of the file:

```make

PARITY_DIR := $(BRAIN_DIR)/build/parity

generate: ## Write the Jekyll files of every published brain page (lint first; idempotent; deletes stale generated files)
	$(BRAINGEN) generate --vault $(BRAIN_DIR) --site $(CURDIR)

generate-check: ## Parity check into build/parity/: brain vs. current site (SECTION=9; default: every section)
	$(BRAINGEN) generate-check --vault $(BRAIN_DIR) --site $(CURDIR) --out $(PARITY_DIR) $(if $(SECTION),--section $(SECTION))

brain-check-generated: ## Fail if a generated file was hand-edited or is stale (part of make check)
	$(BRAINGEN) check-generated --vault $(BRAIN_DIR) --site $(CURDIR)
```

(`SECTION ?=` is already defined earlier in `brain.mk`; recipe lines start with a TAB.)

In the root `Makefile`, replace

```make
check: ## Build the site (via the running dev server) and run project sanity checks
	sh scripts/check-site.sh
```

with

```make
check: brain-lint brain-check-generated ## Lint the brain, check generated files, build the site and run sanity checks
	sh scripts/check-site.sh
```

- [x] **Step 4: Run the targets on the real repo**

```bash
make generate
make brain-check-generated
make generate-check SECTION=9
make generate-check
make help | grep -E "generate|check"
```

Expected: `make generate` prints `0 written, 0 deleted, 0 unchanged` (nothing is published yet) and changes no file (`git status --short` shows only your task's files); `make brain-check-generated` prints `generated files: 0 problems`; `make generate-check SECTION=9` prints `section 9: PASS (14 files compared)` and `1 sections checked, 0 failed`; `make generate-check` ends with `12 sections checked, 0 failed`; `make help` lists `generate`, `generate-check`, `brain-check-generated` and the new `check` description.

- [x] **Step 5: `make check` (Docker)**

Run: `make check`
Expected: brain-lint prints `33 findings, 0 errors, 33 warnings`, check-generated prints `generated files: 0 problems`, then the site build and every sanity check `PASS`; exit 0.

- [x] **Step 6: Docs**

In `docs-arc42-brain/CLAUDE.md`, replace the `## Commands` code block with:

```
make brain-lint                      validate the vault (must pass before every commit)
make brain-raw SECTION=9 WHAT=all    copy site files into raw/section-9-all/
make brain-import BATCH=section-9-all  convert the batch into draft pages
make brain-test                      unit tests of the tooling
make generate-check SECTION=9        parity: generate into build/parity/ and compare with the site
make generate                        write the Jekyll files of every published page
make brain-check-generated           fail if a generated file was hand-edited (runs in make check)
```

and add this paragraph directly below that code block:

```markdown
Generated files (`_pages/section-N.md`, `_posts/…`, `_examples/…` with the line
`<!-- generated from docs-arc42-brain/… — do not edit -->` after the front matter)
are never edited by hand: edit the brain page and run `make generate`.
```

Replace the whole content of `docs-arc42-brain/_system/workflows/cutover.md` with:

```markdown
# Workflow: Cut-over

One section per PR (D10). Preconditions: the section page, every tip in its
`posts-dir` and every example its directives name have brain pages; `make
brain-lint` reports 0 errors.

1. `make generate-check SECTION=N` must print `PASS` and no `not ingested`
   note. Read every note: tag changes per page and `keyword page loses/gains
   tags` go into the PR description; any other difference is a bug in the
   brain page or the generator, never something to accept.
2. Set `status: published` and `updated:` to today on the section page, its
   tips and its examples. Terms, keywords and systems keep their status; they
   are not pages on the site.
3. Delete the hand-written originals: `_pages/section-N.md`,
   `_posts/<posts-dir>/*.md`, and the section's `_examples/*.md`. `make
   generate` refuses to overwrite a file without the marker line, so this
   comes before step 4.
4. `make generate`. The files come back at the same paths, each with the
   marker line after the front matter, tips and examples with `related:`.
   Run it twice; the second run must print `0 written, 0 deleted`.
5. `make generate-check SECTION=N`, `make brain-test`, `make check`, `make
   check-links`.
6. Append a `cutover` entry to `_system/log.md`.
7. One commit: status flips, generated files, log. The diff shows per file:
   front-matter changes (tags, `related:`), the marker line, blank lines
   after the front matter — never a body change.
```

In `docs-arc42-brain/_system/log.md`, change the format comment line

```
## [YYYY-MM-DD] <bootstrap|ingest|audit|report> | <subject>
```

to

```
## [YYYY-MM-DD] <bootstrap|ingest|audit|report|cutover|generate> | <subject>
```

- [x] **Step 7: Commit**

```bash
git add docs-arc42-brain/_system/generate/braingen/cli.py docs-arc42-brain/_system/generate/tests/test_cli_generate.py docs-arc42-brain/_system/brain.mk Makefile docs-arc42-brain/CLAUDE.md docs-arc42-brain/_system/workflows/cutover.md docs-arc42-brain/_system/log.md docs/superpowers/plans/2026-09-18-docs-arc42-brain-phase-2-generator.md
git commit -m "brain: generate, generate-check and check-generated targets; make check runs brain-lint and the drift check; cut-over workflow

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
git log -1 --format=%B | tail -1
```

---

### Task 8: Related-links include in the article layout

Model: Sonnet. The only hand-made site change phase 2 allows (D2, spec §4.5). No page has `related:` yet, so the site must build byte-identical HTML after this task; the rendered block is verified in Task 9.

**Files:**
- Create: `_includes/related.html`
- Modify: `_layouts/post.html` (one line)

**Interfaces:**
- Consumes: `page.related`, a list of `{kind, title, url?}` written by `emit.related_for` (kinds `section`, `subsection`, `tip`, `example`, `faq`, `term`, `keyword`, `system`).
- Produces: `<aside class="related-links">` at the foot of every tip and example that has `related:`; nothing otherwise.

- [ ] **Step 1: Snapshot two built pages before the change**

```bash
make site
S=/private/tmp/claude-501/-Users-gernotstarke-projects-arc42-docs-arc42-org-site/a6c54d87-d882-443a-8f9c-fb4f6aeebd86/scratchpad/task8
mkdir -p $S
cp _site/tips/9-1/index.html $S/tip-9-1.before.html
cp _site/examples/decision-use-adrs/index.html $S/example-adr.before.html
```

- [ ] **Step 2: Write the include**

Create `_includes/related.html`:

```liquid
{%- comment -%}
  "Related" block at the foot of a generated tip or example.

  page.related is written by the docs-arc42-brain generator (brain spec §4.5):
  a list of {kind, title, url}, the page's own section link first, then the
  brain page's `related:` in declared order. This include groups the entries
  by kind in a fixed order. Hand-written pages carry no page.related and
  render nothing.

  An entry without url (a term that no tip carries as a tag yet, a system
  without a page) is listed as plain text.

  Parameters
    page  required — the page or post being rendered.
{%- endcomment -%}
{%- assign related = include.page.related -%}
{%- if related and related.size > 0 %}
<aside class="related-links" aria-labelledby="related-links-heading">
    <h2 id="related-links-heading">Related</h2>
    {%- assign groups = "section subsection|tip|example|faq|term keyword|system" | split: "|" -%}
    {%- assign labels = "Sections|Tips|Examples|Questions|Terms|Example systems" | split: "|" -%}
    {%- for group in groups -%}
    {%- assign kinds = group | split: " " -%}
    {%- capture items -%}
        {%- for r in related -%}
        {%- if kinds contains r.kind %}
        <li>{% if r.url %}<a href="{{ r.url | relative_url }}">{{ r.title | escape }}</a>{% else %}{{ r.title | escape }}{% endif %}</li>
        {%- endif -%}
        {%- endfor -%}
    {%- endcapture -%}
    {%- assign items = items | strip -%}
    {%- if items != "" %}
    <h3>{{ labels[forloop.index0] }}</h3>
    <ul>
        {{ items }}
    </ul>
    {%- endif -%}
    {%- endfor %}
</aside>
{%- endif -%}
```

- [ ] **Step 3: Call it from the article layout**

In `_layouts/post.html`, directly after the line `        </section>` (the one closing `<section class="post-content">`), insert:

```liquid
        {% include related.html page=page %}
```

`git diff _layouts/post.html` must show exactly one added line.

- [ ] **Step 4: The built pages are unchanged**

```bash
make site
S=/private/tmp/claude-501/-Users-gernotstarke-projects-arc42-docs-arc42-org-site/a6c54d87-d882-443a-8f9c-fb4f6aeebd86/scratchpad/task8
nb() { grep -v '^[[:space:]]*$' "$1"; }   # the include line may leave one whitespace-only line
diff <(nb $S/tip-9-1.before.html) <(nb _site/tips/9-1/index.html) && echo tip-unchanged
diff <(nb $S/example-adr.before.html) <(nb _site/examples/decision-use-adrs/index.html) && echo example-unchanged
grep -rl "related-links" _site | head -1 || echo "no related block anywhere"
```

Expected: `tip-unchanged`, `example-unchanged`, `no related block anywhere`. Only a whitespace-only line may differ; any other difference means the include renders something for pages without `related:` — fix the include, not the layout line.

- [ ] **Step 5: `make check`**

Run: `make check`
Expected: exit 0, as in Task 7.

- [ ] **Step 6: Commit**

```bash
git add _includes/related.html _layouts/post.html docs/superpowers/plans/2026-09-18-docs-arc42-brain-phase-2-generator.md
git commit -m "site: related-links include at the foot of tips and examples (renders page.related, nothing without it)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
git log -1 --format=%B | tail -1
```

---

### Task 9: Cut-over of section 9

Model: Opus. Follows `docs-arc42-brain/_system/workflows/cutover.md` (Task 7). Stop and report instead of improvising if any expected output differs. Do not push, do not open a PR.

**Files:**
- Modify: `docs-arc42-brain/wiki/sections/section-9.md`, `docs-arc42-brain/wiki/tips/tip-9-{1..10}.md`, `docs-arc42-brain/wiki/examples/09-decision-example-{adr,htmlsc-1,tpu-2}.md` (`status`, `updated`)
- Replace (delete original, generate): `_pages/section-9.md`, `_posts/09-decisions/*.md` (10 files), `_examples/09-decision-example-{adr,htmlsc-1,tpu-2}.md`
- Modify: `docs-arc42-brain/_system/log.md` (cutover entry)

**Interfaces:**
- Consumes: `make generate-check`, `make generate`, `make brain-check-generated`, `make check`, `make check-links`, `_includes/related.html`.
- Produces: the section-9 PR content on the branch, and a report for the human reviewer.

- [ ] **Step 1: Pre-flight**

```bash
make brain-lint | tail -1
make generate-check SECTION=9 | tee /private/tmp/claude-501/-Users-gernotstarke-projects-arc42-docs-arc42-org-site/a6c54d87-d882-443a-8f9c-fb4f6aeebd86/scratchpad/task9-precheck.txt
```

Expected: `33 findings, 0 errors, 33 warnings` (any error stops the task); `section 9: PASS (14 files compared)`; no `not ingested` line; notes: tag changes on all 13 pages and `keyword page gains tags: ['architecture-decision', 'decision-criteria', 'quality-requirement']`, no `loses` line (the old tags `decision`, `criteria`, `quality` survive on other sections' posts). Keep this file; its notes go into the report.

- [ ] **Step 2: Publish the section-9 pages**

```bash
cd docs-arc42-brain/wiki
for f in sections/section-9.md tips/tip-9-*.md examples/09-decision-example-*.md; do
  sed -i '' -e '1,/^---$/!b' -e 's/^status: .*/status: published/' -e "s/^updated: .*/updated: '2026-09-18'/" "$f"
done
grep -c "^status: published" sections/section-9.md tips/tip-9-*.md examples/09-decision-example-*.md
cd ../..
make brain-lint | tail -1
```

Expected: 14 lines each ending `:1`; lint still `0 errors`. Check `git diff --stat docs-arc42-brain/wiki` shows 14 files with 2 changed lines each (`section-9.md`: `status: draft` → `published`; the others `review` → `published`). Only the front matter may change — the sed range stops at the closing `---`; if any body line changed, `git checkout` the file and edit it by hand.

- [ ] **Step 3: Delete the hand-written originals, then generate**

```bash
rm _pages/section-9.md _posts/09-decisions/*.md _examples/09-decision-example-adr.md _examples/09-decision-example-htmlsc-1.md _examples/09-decision-example-tpu-2.md
make generate
make generate
```

Expected: first run `14 written, 0 deleted, 0 unchanged` preceded by 14 `wrote` lines; second run `0 written, 0 deleted, 14 unchanged`.

- [ ] **Step 4: Verify**

```bash
make brain-test | tail -1
make brain-check-generated | tail -1
make generate-check SECTION=9 | head -1
make generate-check | tail -1
git status --short
```

Expected: `113 passed`; `generated files: 0 problems`; `section 9: PASS (14 files compared)`; `12 sections checked, 0 failed`; `git status` lists exactly 14 ` M` site files (`_pages/section-9.md`, ten `_posts/09-decisions/…`, three `_examples/09-decision-example-…`), the 14 wiki pages and this plan file — nothing else. No `D` or `??` lines.

- [ ] **Step 5: Site checks (Docker)**

```bash
make check
make check-links
```

Expected: both exit 0. html-proofer validates every `related:` URL, including the subsection anchors (`/section-9/#background-on-adrs`, `/section-9/#our-proposal-concerning-decisions`) and the `/keywords/#…` anchors. If check-links fails on a related URL, stop and report the failing URL; do not edit generated files.

- [ ] **Step 6: Inspect the rendered result**

```bash
grep -c 'class="related-links"' _site/tips/9-1/index.html _site/tips/9-5/index.html _site/examples/decision-use-adrs/index.html
grep -o 'href="/section-9/#[a-z-]*"' _site/tips/9-1/index.html _site/tips/9-5/index.html
grep -c 'related-links' _site/tips/8-1/index.html
grep -o 'id="architecture-decision"' _site/keywords/index.html
make generate-check SECTION=9 | grep "anchors\|expected"
```

Expected: 1 for each of the three section-9 pages; `/section-9/#our-proposal-concerning-decisions` in 9-1, `/section-9/#background-on-adrs` in 9-5; `0` for tip 8-1 (a hand-written page); the keyword anchor exists; no `anchor … not on the built page` problem. Open `_site/tips/9-1/index.html` in a text editor and describe the rendered block (headings, entries) in your report.

- [ ] **Step 7: Describe the diff**

```bash
git diff --stat
git diff _posts/09-decisions/2016-03-01-t-9-2.md
git diff _pages/section-9.md
```

For every one of the 14 site files, confirm the body is unchanged apart from the marker line and blank lines directly after the front matter (`make generate-check SECTION=9` already proves this against the originals now in git history; `test_section_9_parity_against_the_ingested_originals` proves it against `raw/ingested/`). Record in the report: lines added/removed per file, which front-matter keys changed (expected: `tags` on all 13 tips/examples, `related` added on the 13, quoting style of `title` unchanged, `section-9.md` front matter identical), and the full tag changes from Step 1.

- [ ] **Step 8: Log entry**

Append to `docs-arc42-brain/_system/log.md`:

```markdown

## [2026-09-18] cutover | section 9
- published: section-9, tip-9-1 … tip-9-10, 09-decision-example-adr, -htmlsc-1, -tpu-2 (14 pages)
- generated: _pages/section-9.md, _posts/09-decisions/ (10), _examples/09-decision-example-* (3); hand-written originals deleted first, generated files now at the same paths
- parity: make generate-check SECTION=9 PASS before and after; 12 sections checked, 0 failed
- tags: decision → architecture-decision (13 pages), criteria → decision-criteria, quality → quality-requirement (9-1, 9-4); adr and decision-criteria added where the brain maps terms the legacy tags lacked; keyword page gains architecture-decision, decision-criteria, quality-requirement, loses nothing
- site: related-links block on the 13 tips/examples; make check and make check-links green
```

Adjust the tag line to exactly what Step 1 printed.

- [ ] **Step 9: Commit**

```bash
git add docs-arc42-brain/wiki/sections/section-9.md docs-arc42-brain/wiki/tips/tip-9-*.md docs-arc42-brain/wiki/examples/09-decision-example-*.md _pages/section-9.md _posts/09-decisions/*.md _examples/09-decision-example-adr.md _examples/09-decision-example-htmlsc-1.md _examples/09-decision-example-tpu-2.md docs-arc42-brain/_system/log.md docs/superpowers/plans/2026-09-18-docs-arc42-brain-phase-2-generator.md
git commit -m "brain: cut over section 9 — pages published, site files generated from the brain

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
git log -1 --format=%B | tail -1
git show --stat HEAD | tail -5
```

- [ ] **Step 10: Report**

Write the report with: the Step 1 pre-check output; generate outputs; the test, check and link-check results; the rendered related block of tip 9-1; the per-file diff summary of Step 7; tag changes; anything that deviated from an expected output and what you did about it.
