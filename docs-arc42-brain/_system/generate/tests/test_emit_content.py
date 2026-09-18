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
        "# generated from docs-arc42-brain/wiki/tips/tip-9-1.md — do not edit\n---\n\nSome tip.\n"
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
    assert out.text.endswith("do not edit\n---\n\nAn example.\n")


def test_generated_tip_body_is_exactly_the_brain_body(tmp_path):
    vault = build(tmp_path)

    out = emit_tip(vault, vault.pages["tip-9-1"], EMITTED, SITE_TAGS)

    # Nothing may precede the first paragraph: Jekyll's excerpt (and with it the
    # meta description) is the body up to the first blank line.
    assert frontmatter.loads(out.text).content == vault.pages["tip-9-1"].body
