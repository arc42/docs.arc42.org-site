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
    # The three headings the brain writes, plus the ones the Jekyll includes
    # inject: "### Examples" at the `%% examples: … %%` position and the fixed
    # foot. See _includes/example.md, further-info.md and examples-link.html.
    assert [(h.level, h.text, h.synthetic) for h in page.headings] == [
        (1, "9. Architecture Decisions", False),
        (2, "Content", False),
        (3, "Examples", True),
        (2, "Background (on ADRs)", False),
        (2, "Practical Tips", True),
        (3, "Related Questions", True),
        (3, "Complete Examples", True),
    ]
    assert [(d.name, d.arg) for d in page.directives] == [
        ("examples", "decisions"),
        ("examples-link", None),
    ]
    assert page.has_liquid is False


SECTION_WITH_OWN_EXAMPLES_HEADING = """---
id: section-10
type: section
title: 10 - Quality requirements
status: draft
---

# 10. Quality Requirements

%% examples: quality %%

## Examples

Excerpts from real documents.
"""


def test_body_examples_heading_comes_second_and_gets_the_suffix(tmp_path):
    """_site/section-10 renders the include's heading as `examples` and the
    body's own `## Examples` as `examples-1`; the brain only sees a directive."""
    p = write(tmp_path, "wiki/sections/section-10.md", SECTION_WITH_OWN_EXAMPLES_HEADING)
    page = parse_page(p)
    assert [(h.text, h.anchor, h.synthetic) for h in page.headings] == [
        ("10. Quality Requirements", "10-quality-requirements", False),
        ("Examples", "examples", True),
        ("Examples", "examples-1", False),
        ("Practical Tips", "practical-tips", True),
        ("Related Questions", "related-questions", True),
        ("Complete Examples", "complete-examples", True),
    ]


def test_section_foot_headings_are_present_so_a_wikilink_heading_resolves(tmp_path):
    p = write(tmp_path, "wiki/sections/section-10.md", SECTION_WITH_OWN_EXAMPLES_HEADING)
    page = parse_page(p)
    foot = [h for h in page.headings if h.text == "Practical Tips"]
    assert len(foot) == 1 and foot[0].level == 2 and foot[0].synthetic is True
    # and it sits past the body, so the emitter can tell it is not body content
    assert foot[0].line > max(h.line for h in page.headings if not h.synthetic)


def test_only_section_pages_gain_the_injected_headings(tmp_path):
    body = "---\nid: 9-1\ntype: tip\n---\n\n## Examples\n\n%% examples: decisions %%\n"
    page = parse_page(write(tmp_path, "wiki/tips/tip-9-1.md", body))
    assert [(h.text, h.anchor, h.synthetic) for h in page.headings] == [
        ("Examples", "examples", False),
    ]


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
