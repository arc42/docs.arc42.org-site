from render import render


def test_callout_directive_wikilinks():
    body = ("> [!arc42-help]\n> ## Hello\n> Some *text*.\n\n"
            "%% examples: decisions %%\n\n"
            "See [[tip-9-1|the tip]] and [[nowhere]].\n")
    html = render(body, {"tip-9-1"})
    assert '<div class="callout arc42-help">' in html
    assert "<h2" in html and "<em>text</em>" in html
    assert '<p class="directive">examples: decisions</p>' in html
    assert '<a class="wikilink" href="/page/tip-9-1">the tip</a>' in html
    assert '<span class="wikilink broken">nowhere</span>' in html


def test_table():
    assert "<table>" in render("| a | b |\n|---|---|\n| 1 | 2 |\n", set())


def test_wikilink_and_directive_text_is_escaped():
    html = render('[[tip-9-1|<script>x</script>]] [[a"b]]\n\n%% examples: <b> %%\n', {"tip-9-1"})
    assert "<script>" not in html and "&lt;script&gt;" in html
    assert 'a&quot;b' in html and "&lt;b&gt;" in html
