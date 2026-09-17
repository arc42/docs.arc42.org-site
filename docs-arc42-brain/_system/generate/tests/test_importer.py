from pathlib import Path

import frontmatter
import pytest

from braingen.importer import (
    convert_example,
    convert_section,
    convert_tip,
    import_batch,
    next_source_id,
    write_page,
)
from braingen.lint import lint
from braingen.parse import load_vault
from braingen.raw import make_raw
from tests.test_raw import EXAMPLE, PAGE, TIP, build_site

TODAY = "2026-09-17"
MANIFEST = {
    "section": 9, "what": "all", "name": "Architecture Decisions", "category": "decisions",
    "permalink": "/section-9/", "posts_dir": "09-decisions", "order": 13,
    "title": "9 - Architecture decisions", "example_categories": ["decisions"], "files": [],
}


def test_convert_section_callouts_directives_images_and_foot():
    meta, body = convert_section(PAGE, MANIFEST, TODAY, "SRC-001-section-9-all")
    assert list(meta) == ["id", "type", "title", "status", "created", "updated", "sources", "related",
                          "number", "name", "category", "posts-dir", "permalink", "order", "faq-topic"]
    assert meta["id"] == "section-9" and meta["type"] == "section" and meta["status"] == "draft"
    assert meta["sources"] == ["[[SRC-001-section-9-all]]"]
    assert meta["faq-topic"] == "fundamental architecture and design decisions"
    assert meta["posts-dir"] == "09-decisions" and meta["order"] == 13
    assert "> [!arc42-help]\n>\n> ## Content\n> Important decisions.\n" in body
    assert "> ![flow](../assets/sections/09/flow.png)" in body
    assert "> %% examples: decisions %%" in body
    assert "\n%% examples-link %%\n" in body
    assert "further-info" not in body and "{%" not in body and "{{" not in body
    assert "<div" not in body and "</div>" not in body


def test_convert_tip_maps_frontmatter_and_legacy_tags():
    meta, body = convert_tip("2016-03-01-t-9-1.md", TIP, MANIFEST, TODAY, "SRC-001-x")
    assert list(meta) == ["id", "type", "title", "status", "created", "updated", "sources", "related",
                          "section", "keywords", "terms", "legacy-tags", "date", "permalink"]
    assert meta["id"] == "9-1" and meta["date"] == "2016-03-01"
    assert meta["section"] == "[[section-9]]"
    assert meta["legacy-tags"] == ["decision", "quality", "stakeholder", "lean"]
    assert meta["keywords"] == [] and meta["terms"] == []
    assert meta["permalink"] == "/tips/9-1/"
    assert body.strip() == "Body of the tip."


def test_convert_tip_accepts_list_tags():
    text = TIP.replace("tags: decision quality stakeholder lean", "tags: [decision, lean]")
    meta, _ = convert_tip("2016-03-01-t-9-1.md", text, MANIFEST, TODAY, "SRC-001-x")
    assert meta["legacy-tags"] == ["decision", "lean"]


def test_convert_example_maps_category_system_and_images():
    meta, body = convert_example("09-decision-example-adr.md", EXAMPLE, MANIFEST, TODAY, "SRC-001-x")
    assert meta["id"] == "09-decision-example-adr" and meta["type"] == "example"
    assert meta["example-category"] == "decisions" and meta["system"] == ""
    assert meta["legacy-tags"] == ["decision", "example"]
    assert "![table](../assets/examples/adr-table.png)" in body
    meta2, _ = convert_example("05-buildingblock-example-hsc.md", EXAMPLE, MANIFEST, TODAY, "SRC-001-x")
    assert meta2["system"] == "[[htmlsc]]"
    meta3, _ = convert_example("07-deployment-example-tpu-1.md", EXAMPLE, MANIFEST, TODAY, "SRC-001-x")
    assert meta3["system"] == "[[tpu]]"


def test_write_page_quotes_wikilinks_and_keeps_order(tmp_path):
    p = tmp_path / "x.md"
    write_page(p, {"id": "a", "related": ["[[b]]"], "z": 1, "a": 2}, "body\n")
    text = p.read_text()
    assert text.startswith("---\nid: a\nrelated:\n- '[[b]]'\nz: 1\na: 2\n---\n\nbody\n")
    assert frontmatter.loads(text)["related"] == ["[[b]]"]


def test_next_source_id(tmp_path):
    (tmp_path / "raw/sources").mkdir(parents=True)
    assert next_source_id(tmp_path) == 1
    (tmp_path / "raw/sources/SRC-007-foo.md").write_text("---\nid: SRC-007\n---\n")
    assert next_source_id(tmp_path) == 8


def test_import_batch_end_to_end_lints_clean(tmp_path):
    site = build_site(tmp_path)
    vault = tmp_path / "vault"
    make_raw(site, vault, 9, "all")
    report = import_batch(vault, "section-9-all", TODAY)
    assert report.source_slug == "SRC-001-section-9-all"
    assert (vault / "wiki/sections/section-9.md").exists()
    assert (vault / "wiki/tips/tip-9-1.md").exists()
    assert (vault / "wiki/examples/09-decision-example-adr.md").exists()
    assert (vault / "wiki/assets/sections/09/flow.png").read_bytes() == b"png"
    assert (vault / "wiki/assets/examples/adr-table.png").read_bytes() == b"png"
    src = frontmatter.load(vault / "raw/sources/SRC-001-section-9-all.md")
    assert src["origin"] == "raw/section-9-all/"
    paths = [f["path"] for f in src["files"]]
    assert "pages/section-9.md" in paths and all(len(f["sha256"]) == 64 for f in src["files"])
    assert set(src["ingested-pages"]) == {"[[section-9]]", "[[tip-9-1]]", "[[09-decision-example-adr]]"}
    findings = lint(load_vault(vault))
    assert [str(f) for f in findings if f.level == "error"] == []


def test_import_batch_refuses_to_overwrite_existing_page(tmp_path):
    site = build_site(tmp_path)
    vault = tmp_path / "vault"
    make_raw(site, vault, 9, "page")
    import_batch(vault, "section-9-page", TODAY)
    make_raw(site, vault, 9, "all")
    with pytest.raises(FileExistsError, match="section-9.md"):
        import_batch(vault, "section-9-all", TODAY)
