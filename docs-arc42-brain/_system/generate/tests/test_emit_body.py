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
    assert marker("wiki/tips/tip-9-1.md") == "# generated from docs-arc42-brain/wiki/tips/tip-9-1.md — do not edit"


def test_is_generated_only_when_marker_is_last_front_matter_line():
    m = marker("wiki/tips/tip-9-1.md")
    assert is_generated(f"---\na: 1\n{m}\n---\n\nbody\n")
    assert not is_generated("---\na: 1\n---\n\nbody\n")
    assert not is_generated(f"---\na: 1\n---\n\n{m}\n")
    assert not is_generated(f"{m}\n")
    assert not is_generated("---\na: 1\n")


def test_is_generated_false_when_marker_is_not_the_last_front_matter_line():
    m = marker("wiki/tips/tip-9-1.md")
    assert not is_generated(f"---\n{m}\na: 1\n---\n\nbody\n")


def test_is_generated_false_for_the_old_body_marker():
    old = "<!-- generated from docs-arc42-brain/wiki/tips/tip-9-1.md — do not edit -->"
    assert not is_generated(f"---\na: 1\n---\n{old}\n\nbody\n")


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
