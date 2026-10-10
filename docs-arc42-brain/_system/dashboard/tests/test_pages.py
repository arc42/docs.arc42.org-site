import subprocess
import tomllib
from pathlib import Path

import pytest

import version

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


def test_section_chips_filter_and_toggle(client):
    html = client.get("/tips?section=9").get_data(as_text=True)
    assert "tip-9-1" in html
    # 9 is on: its chip is pressed and clicking it again drops the filter.
    assert '<a class="chip on" aria-current="true" href="/tips">9</a>' in html
    # 3 is off: clicking it adds 3 to the selection, 9 stays.
    assert '<a class="chip" href="/tips?section=3&amp;section=9">3</a>' in html
    assert '<a class="chip" href="/tips">All</a>' in html
    # The status/system form carries the selection along.
    assert '<input type="hidden" name="section" value="9">' in html


def test_section_chips_several_on_and_other_filters_kept(client):
    html = client.get("/tips?status=draft&section=3&section=9").get_data(as_text=True)
    assert "tip-9-2" in html and "tip-9-1" not in html
    assert '<a class="chip on" aria-current="true" href="/tips?status=draft&amp;section=9">3</a>' in html
    assert '<a class="chip" href="/tips?status=draft">All</a>' in html


def test_section_filter_with_no_match_and_junk(client):
    assert "No pages match this filter." in client.get("/tips?section=3").get_data(as_text=True)
    html = client.get("/tips?section=abc").get_data(as_text=True)
    assert "tip-9-1" in html and '<a class="chip on" aria-current="true" href="/tips">All</a>' in html


def test_section_chips_only_where_pages_have_a_section(client):
    assert 'class="chip' in client.get("/examples").get_data(as_text=True)
    assert 'class="chip' not in client.get("/keywords").get_data(as_text=True)


@pytest.mark.parametrize("path", ["/", "/tips", "/who"])
def test_footer_says_where_and_which_version(client, path):
    html = client.get(path).get_data(as_text=True)
    assert "Made with <span" in html and "in Cologne" in html
    assert f"v{version.VERSION}" in html


def test_version_matches_pyproject():
    meta = tomllib.loads((Path(__file__).parent.parent / "pyproject.toml").read_text())
    assert meta["project"]["version"] == version.VERSION == "0.2.2"


def test_contributors_page_lists_real_names(repo, client):
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / ".mailmap").write_text("Real Name <real@example.org> <old@example.org>\n")
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=host@laptop", "-c", "user.email=old@example.org",
                    "commit", "-q", "--allow-empty", "-m", "x"], check=True)
    html = client.get("/contributors").get_data(as_text=True)
    assert "Real Name" in html and 'href="mailto:real@example.org"' in html
    assert "host@laptop" in html


def test_contributors_page_without_git(client):
    assert "No commits found." in client.get("/contributors").get_data(as_text=True)


def test_log_and_menu_link_to_contributors(client):
    assert 'href="/contributors"' in client.get("/log").get_data(as_text=True)


def test_who_shows_the_yoda_avatar_only_for_the_facilitator(client):
    import json
    for cid in ("first", "second"):
        client.post("/ping", data=json.dumps({"client_id": cid}), content_type="application/json")
    html = client.get("/who").get_data(as_text=True)
    table = html[html.index('class="who-table"'):]
    assert table.count('src="/static/yoda.jpg"') == 1   # Yoda's row only
    assert "Yoda" in table


def test_masthead_carries_the_hidden_me_slot_with_yoda_avatar(client):
    html = client.get("/").get_data(as_text=True)
    assert 'id="presence-me"' in html and 'id="presence-avatar"' in html
    assert client.get("/static/yoda.jpg").status_code == 200
