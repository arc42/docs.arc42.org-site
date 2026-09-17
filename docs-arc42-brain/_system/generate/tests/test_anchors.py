"""Every expectation here is a heading id copied out of a real build of the site.

Reproduce with:

    make site
    grep -o '<h[1-6] id="[^"]*"' _site/section-N/index.html

The site runs kramdown's **GFM** parser (`_config.yml`: `kramdown.input: GFM`,
`Gemfile.lock` pins `kramdown-parser-gfm`), whose id rule is GitHub's, not
kramdown's own. The difference is visible on every numbered heading: base
kramdown drops everything before the first letter, GFM keeps the digits.
"""
from braingen.anchors import assign_anchors, gfm_heading_id


def test_numbered_subsection_keeps_its_digits():
    # _site/section-5: <h2 id="51-whitebox-overall-system">5.1 Whitebox Overall System</h2>
    assert gfm_heading_id("5.1 Whitebox Overall System") == "51-whitebox-overall-system"


def test_numbered_subsection_with_short_title():
    # _site/section-1: <h2 id="13-stakeholder">1.3 Stakeholder</h2>
    assert gfm_heading_id("1.3 Stakeholder") == "13-stakeholder"


def test_page_title_keeps_its_leading_number():
    # _site/section-9: <h1 id="9-architecture-decisions">9. Architecture Decisions</h1>
    assert gfm_heading_id("9. Architecture Decisions") == "9-architecture-decisions"


def test_entities_are_decoded_and_emphasis_markers_are_consumed():
    # _site/section-1: <h3 id="insert-requirements-overview"><em>&lt;insert …&gt;</em></h3>
    assert gfm_heading_id("_&lt;insert requirements overview>_") == "insert-requirements-overview"


def test_parentheses_are_deleted_not_hyphenated():
    # _site/section-9: <h2 id="background-on-adrs">Background (on ADRs)</h2>
    assert gfm_heading_id("Background (on ADRs)") == "background-on-adrs"


def test_slash_is_deleted_and_joins_the_two_words():
    # _site/section-5: <h3 id="describe-motivationreasoning-for-overall-system-decomposition">
    assert (
        gfm_heading_id("_&lt;describe motivation/reasoning for overall system decomposition>_")
        == "describe-motivationreasoning-for-overall-system-decomposition"
    )


def test_emphasis_in_the_middle_of_a_numbered_heading():
    # _site/section-5: <h3 id="521-white-box-building-block-1">5.2.1 White Box <em>…</em></h3>
    assert (
        gfm_heading_id("5.2.1 White Box _&lt;building block 1&gt;_")
        == "521-white-box-building-block-1"
    )


def test_leading_space_inside_the_emphasis_becomes_a_leading_hyphen():
    # _site/section-1: <h3 id="-insert-table-of-quality-goals-here">
    # The space is not stripped and not collapsed: one space, one hyphen.
    assert (
        gfm_heading_id("_&lt; insert table of quality goals here>_")
        == "-insert-table-of-quality-goals-here"
    )


def test_two_spaces_become_two_hyphens():
    # _site/section-7: <h4 id="721--infrastructure-element-1">7.2.1 <em>&lt; Infrastructure …</em></h4>
    # "7.2.1 " + "" (the deleted "<") + " Infrastructure …" leaves two adjacent spaces.
    assert (
        gfm_heading_id("7.2.1 _&lt; Infrastructure element 1>_")
        == "721--infrastructure-element-1"
    )


def test_tab_becomes_a_hyphen_like_a_space():
    # kramdown's GFM id rule translates " \t" alike; no heading in _pages/ has an
    # interior tab, so this pins the rule rather than a page.
    assert gfm_heading_id("Quality\tGoals") == "quality-goals"


def test_ellipsis_placeholder_yields_no_id_at_all():
    # _pages/section-6.md line 56 is "### ...". _site/section-6 renders it as
    # "<h3>…</h3>" — no id attribute. Nothing is left after the rule, and
    # kramdown's GFM parser emits no "section" fallback.
    assert gfm_heading_id("...") == ""
    assert gfm_heading_id("…") == ""


def test_underscore_inside_a_word_survives():
    # \w keeps "_"; only paired emphasis markers are consumed.
    assert gfm_heading_id("snake_case") == "snake_case"


def test_duplicates_get_numeric_suffixes():
    # _site/section-1: motivation, motivation-1, motivation-2 under 1.1/1.2/1.3.
    assert assign_anchors(["Content", "Motivation", "Content", "Content"]) == [
        "content",
        "motivation",
        "content-1",
        "content-2",
    ]


def test_the_include_injected_examples_heading_takes_the_bare_id():
    # _site/section-10: the include's "### Examples" is emitted first and takes
    # "examples"; the body's own "## Examples" further down becomes "examples-1".
    assert assign_anchors(["Examples", "Examples"]) == ["examples", "examples-1"]


def test_id_less_headings_stay_empty():
    # Deliberate divergence, unreachable from the corpus: kramdown counts the
    # empty id like any other (kramdown-parser-gfm 1.1.0 gfm.rb:113), so a
    # second id-less heading on one page would be "-1" there. No page in
    # _pages/ or the vault has two, and no id is emitted for them anyway.
    assert assign_anchors(["...", "Content", "..."]) == ["", "content", ""]
