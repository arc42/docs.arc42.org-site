def test_home_renders_with_title_and_nav(client):
    r = client.get("/")
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert "<title>docs-arc42-brain</title>" in html
    assert 'href="/static/style.css' in html
    assert "cdn" not in html.lower()
