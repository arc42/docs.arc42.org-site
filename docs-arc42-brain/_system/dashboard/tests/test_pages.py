import pytest

PAGES = ["/", "/sections", "/tips", "/examples", "/faq", "/terms", "/keywords", "/systems", "/tags",
         "/issues", "/lint", "/log", "/review", "/cutover", "/gaps", "/help",
         "/page/tip-9-1", "/page/section-9"]


@pytest.mark.parametrize("path", PAGES)
def test_page_renders(client, path):
    assert client.get(path).status_code == 200


def test_home_has_every_tile(client):
    html = client.get("/").get_data(as_text=True)
    for title in ["Sections", "Tips", "Examples", "FAQ", "Tags", "Issues", "Lint", "Latest changes",
                  "Generate", "Review queue", "Cut-over readiness", "Gaps", "Link health"]:
        assert f">{title}<" in html, title
    assert "136 answers in faq.arc42.org, not yet ingested" in html


def test_list_filters(client):
    html = client.get("/tips?status=draft").get_data(as_text=True)
    assert "tip-9-2" in html and "tip-9-1" not in html


def test_detail(client):
    html = client.get("/page/tip-9-1").get_data(as_text=True)
    assert "ISS-001" in html and "obsidian://open?vault=docs-arc42-brain" in html
    assert 'href="/page/09-decision-example-x"' in html
    assert client.get("/page/nope").status_code == 404


def test_sections_shows_page_status_and_ingest_state_apart(client):
    """The two columns the table exists to keep apart: section 3 has nothing
    ingested, section 9 is cut over, and both carry their own page status."""
    html = client.get("/sections").get_data(as_text=True)
    assert "<th>Page</th><th>Ingest</th>" in html
    assert '<span class="ingest-badge not-ingested">not ingested</span>' in html
    assert '<span class="ingest-badge cut-over">cut over</span>' in html
    assert '<span class="status-badge draft">draft</span>' in html
    assert 'href="/help#sections"' in html


def test_help_explains_the_write_actions(client):
    """The help page is prose, but these are the terms it exists to define."""
    html = client.get("/help").get_data(as_text=True)
    for anchor in ["flow", "sections", "status", "ingest", "lint", "publish", "parity", "cutover"]:
        assert f'id="{anchor}"' in html, anchor
    assert "Publishing is not deploying" in html


def test_section_detail_renders_callout(client):
    html = client.get("/page/section-9").get_data(as_text=True)
    assert 'class="callout arc42-help"' in html and 'class="directive"' in html
