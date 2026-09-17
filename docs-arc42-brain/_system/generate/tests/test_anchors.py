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
