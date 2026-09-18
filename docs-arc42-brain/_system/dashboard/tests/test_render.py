from render import render, render_inline, render_meta


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


# -- render_inline / render_meta: front-matter values (detail page) --------


def test_render_inline_resolves_wikilinks_and_escapes_the_rest():
    html = render_inline('See [[section-4]] & [[nowhere|Nowhere]] <b>', {"section-4"})
    assert '<a class="wikilink" href="/page/section-4">section-4</a>' in html
    assert '<span class="wikilink broken">Nowhere</span>' in html
    assert "&amp;" in html and "&lt;b&gt;" in html and "<b>" not in html


def test_render_meta_scalars():
    assert render_meta(None, set()) == "—"
    assert render_meta(True, set()) == "yes"
    assert render_meta(False, set()) == "no"
    assert render_meta(3, set()) == "3"
    assert render_meta([], set()) == "—"
    assert render_meta({}, set()) == "—"


def test_render_meta_renders_wikilinks_in_strings_lists_and_dicts():
    known = {"section-4"}
    assert render_meta("[[section-4]]", known) == '<a class="wikilink" href="/page/section-4">section-4</a>'
    rendered_list = render_meta(["[[section-4]]", "plain"], known)
    assert rendered_list == '<a class="wikilink" href="/page/section-4">section-4</a>, plain'
    rendered_dict = render_meta({"home": "[[section-4]]"}, known)
    assert rendered_dict == 'home: <a class="wikilink" href="/page/section-4">section-4</a>'
