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
