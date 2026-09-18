from braingen.compare import (
    compare_file,
    leading_blank_lines,
    normalise_lines,
    split_foot,
    split_tags,
)
from braingen.emit_body import marker

MARK = marker("wiki/tips/tip-9-1.md")
ORIG = (
    '---\nlayout: post\ntitle: "Tip 9-1: X"\ntags: decision lean\ncategory: decisions\n'
    "permalink: /tips/9-1/\n---\nBody line\n\nsecond\n"
)
GEN = (
    '---\nlayout: post\ntitle: "Tip 9-1: X"\ntags: lean architecture-decision\ncategory: decisions\n'
    'permalink: /tips/9-1/\nrelated:\n- kind: tip\n  title: "Tip 9-2"\n  url: /tips/9-2/\n'
    f"{MARK}\n---\n\nBody line\n\nsecond\n"
)


def test_normalise_lines():
    assert normalise_lines("\n\na  \n\nb\t\n\n") == ["a  ", "", "b"]


def test_normalise_lines_flattens_longer_runs_and_strips_a_single_space():
    assert normalise_lines("a   \nb \nc\n") == ["a  ", "b", "c"]


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


def test_lost_hard_line_break_fails():
    orig = "---\ntitle: t\n---\n\nBody line  \nsecond\n"
    gen = f"---\ntitle: t\n{marker('wiki/tips/tip-9-1.md')}\n---\n\nBody line\nsecond\n"
    rep = compare_file("x.md", orig, gen, 9, {})
    assert not rep.ok
    assert rep.problems[0].startswith("body differs:")


def test_one_trailing_space_vs_none_still_passes():
    orig = "---\ntitle: t\n---\n\nBody line \nsecond\n"
    gen = f"---\ntitle: t\n{marker('wiki/tips/tip-9-1.md')}\n---\n\nBody line\nsecond\n"
    rep = compare_file("x.md", orig, gen, 9, {})
    assert rep.ok


def test_expected_difference_applies_to_its_section_only():
    orig = "---\ntitle: t\n---\n\n![q](/assets/images/sections/10/q.svg)\n"
    gen = f"---\ntitle: t\n{marker('wiki/sections/section-10.md')}\n---\n\n![q]({{{{ site.imageurl }}}}/10/q.svg)\n"
    ten = compare_file("_pages/section-10.md", orig, gen, 10, {})
    assert ten.ok
    assert ten.notes == ["expected difference: hard-coded image path normalised to {{ site.imageurl }} at ingest (spec Appendix A)"]
    assert not compare_file("_pages/section-9.md", orig, gen, 9, {}).ok


def test_foot_layout_is_ignored_but_its_arguments_are_compared():
    orig = '---\ntitle: t\n---\n\nx\n\n{% include further-info.md category="a"\n  topic="t"\n  faqlink="u" %}\n'
    gen = (
        f"---\ntitle: t\n{marker('wiki/sections/section-1.md')}\n---\n\nx\n\n\n"
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
