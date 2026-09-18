from pathlib import Path

import yaml

from braingen.lint import lint
from braingen.parse import load_vault


def page(root: Path, rel: str, meta: dict, body: str = "") -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    fm = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True)
    p.write_text(f"---\n{fm}---\n\n{body}\n", encoding="utf-8")


BASE = {"status": "draft", "created": "2026-09-17", "updated": "2026-09-17", "sources": [], "related": []}


def section(root, n=9, body="", **extra):
    meta = {
        "id": f"section-{n}", "type": "section", "title": f"{n} - X", **BASE,
        "number": n, "name": "X", "category": "decisions", "posts-dir": "09-decisions",
        "permalink": f"/section-{n}/", "order": 13, "faq-topic": "decisions", **extra,
    }
    page(root, f"wiki/sections/section-{n}.md", meta, body)


def tip(root, id="9-1", body="", **extra):
    meta = {"id": id, "type": "tip", "title": f"Tip {id}", **BASE, "section": "[[section-9]]",
            "keywords": [], "terms": [], "legacy-tags": [], "date": "2016-03-01",
            "permalink": f"/tips/{id}/", **extra}
    page(root, f"wiki/tips/tip-{id}.md", meta, body)


def errors(vault_root):
    return [str(f) for f in lint(load_vault(vault_root)) if f.level == "error"]


def warnings(vault_root):
    return [str(f) for f in lint(load_vault(vault_root)) if f.level == "warning"]


def test_clean_vault_has_no_findings(tmp_path):
    section(tmp_path, body="# 9\n\n> [!arc42-help]\n> %% examples: decisions %%\n")
    tip(tmp_path)
    assert lint(load_vault(tmp_path)) == []


def test_unknown_type_and_wrong_folder(tmp_path):
    page(tmp_path, "wiki/tips/x.md", {"id": "x", "type": "banana", **BASE, "title": "x"})
    page(tmp_path, "wiki/terms/section-1.md", {"id": "section-1", "type": "section", **BASE, "title": "x"})
    e = "\n".join(errors(tmp_path))
    assert "unknown type 'banana'" in e
    assert "section-1: type section belongs in wiki/sections" in e


def test_missing_required_fields_and_bad_status(tmp_path):
    page(tmp_path, "wiki/tips/tip-9-1.md", {"id": "9-1", "type": "tip", "title": "t", "status": "bogus"})
    e = "\n".join(errors(tmp_path))
    for f in ("created", "updated", "section", "date", "permalink"):
        assert f"missing field '{f}'" in e
    assert "invalid status 'bogus'" in e


def test_issue_and_source_have_their_own_status_sets(tmp_path):
    page(tmp_path, "wiki/issues/ISS-001-q.md", {"id": "ISS-001", "type": "issue", "title": "q", **BASE,
         "status": "open", "severity": "minor", "kind": "question", "raised-by": "agent"})
    page(tmp_path, "raw/sources/SRC-001-x.md", {"id": "SRC-001", "type": "source", "title": "x", **BASE,
         "status": "ingested", "origin": "raw/x/", "files": []})
    assert errors(tmp_path) == []


def test_duplicate_id_within_type(tmp_path):
    tip(tmp_path, id="9-1")
    page(tmp_path, "wiki/tips/tip-9-1-copy.md", {"id": "9-1", "type": "tip", "title": "t", **BASE,
         "section": "[[section-9]]", "date": "2016-03-01", "permalink": "/tips/9-1/"})
    section(tmp_path, body="> %% examples: decisions %%")
    assert any("duplicate id 9-1" in e for e in errors(tmp_path))


def test_unresolved_and_ambiguous_heading_links(tmp_path):
    section(tmp_path, body="# 9\n\n## Content\n\n## Content\n\n## Form\n\n> %% examples: decisions %%")
    tip(tmp_path, body="[[nowhere]] [[section-9#Form]] [[section-9#Content]] [[section-9#Nope]]")
    e = "\n".join(errors(tmp_path))
    assert "unresolved link [[nowhere]]" in e
    assert "heading 'Content' is not unique on section-9" in e
    assert "heading 'Nope' not found on section-9" in e
    assert "[[section-9#Form]]" not in e


def test_related_reciprocity_is_a_warning_except_for_sections(tmp_path):
    section(tmp_path, body="> %% examples: decisions %%")
    tip(tmp_path, id="9-1", related=["[[tip-9-2]]", "[[section-9]]"])
    tip(tmp_path, id="9-2")
    assert errors(tmp_path) == []
    w = "\n".join(warnings(tmp_path))
    assert "tip-9-1: related [[tip-9-2]] is not reciprocated" in w
    assert "section-9" not in w


def test_published_requires_sources_and_no_legacy_tags(tmp_path):
    section(tmp_path, body="> %% examples: decisions %%")
    tip(tmp_path, status="published", sources=[], **{"legacy-tags": ["decision"]})
    e = "\n".join(errors(tmp_path))
    assert "published without sources" in e
    assert "legacy-tags still present" in e


def test_term_may_keep_legacy_tags_in_review(tmp_path):
    """L13 is about tags the importer parks on a page; on a term the list is the permanent
    mapping of old tag spellings (spec 4.2), so it must survive the step out of draft."""
    section(tmp_path, body="> %% examples: decisions %%")
    page(tmp_path, "wiki/terms/architecture-decision.md",
         {"id": "architecture-decision", "type": "term", "title": "Architecture decision", **BASE,
          "status": "review", "term": "Architecture decision", "home": "[[section-9]]",
          "legacy-tags": ["decision"]})
    tip(tmp_path, status="review", **{"legacy-tags": ["decision"]})
    e = "\n".join(errors(tmp_path))
    assert "architecture-decision" not in e
    assert "tip-9-1: legacy-tags still present: ['decision']" in e


def test_images_must_exist_and_liquid_is_forbidden(tmp_path):
    section(tmp_path, body="> %% examples: decisions %%")
    (tmp_path / "wiki/assets/sections/09").mkdir(parents=True)
    (tmp_path / "wiki/assets/sections/09/ok.png").write_bytes(b"x")
    tip(tmp_path, body="![a](../assets/sections/09/ok.png) ![b](../assets/sections/09/missing.png) {{ site.imageurl }}")
    e = "\n".join(errors(tmp_path))
    assert "missing image ../assets/sections/09/missing.png" in e
    assert "ok.png" not in e
    assert "Liquid syntax in body" in e


def test_example_category_must_be_referenced_exactly_once(tmp_path):
    section(tmp_path, n=9, body="> %% examples: decisions %%\n> %% bogus %%")
    section(tmp_path, n=8, body="> %% examples: decisions %%", category="concepts", **{"posts-dir": "08-concepts"})
    page(tmp_path, "wiki/examples/ex-a.md", {"id": "ex-a", "type": "example", "title": "a", **BASE,
         "section": "[[section-9]]", "example-category": "decisions", "permalink": "/examples/a/"})
    page(tmp_path, "wiki/examples/ex-b.md", {"id": "ex-b", "type": "example", "title": "b", **BASE,
         "section": "[[section-9]]", "example-category": "orphaned", "permalink": "/examples/b/"})
    e = "\n".join(errors(tmp_path))
    w = "\n".join(warnings(tmp_path))
    assert "example-category 'orphaned' is not referenced by any section directive" in e
    assert "unknown directive 'bogus'" in e
    assert "example-category 'decisions' is referenced by 2 directives" in w


def test_findings_carry_rule_ids(tmp_path):
    from braingen.lint import Finding, lint
    from braingen.parse import load_vault
    from tests import vaultkit as vk

    vk.source(tmp_path)
    vk.section(tmp_path)
    vk.tip(tmp_path, "9-1", related=["[[tip-9-2]]", "[[nowhere]]"], status="draft")
    vk.tip(tmp_path, "9-2", status="draft")
    vk.example(tmp_path, "09-decision-example-y", status="draft", **{"example-category": "orphans"})
    rules = {(f.page, f.rule) for f in lint(load_vault(tmp_path))}
    assert ("tip-9-1", "link") in rules
    assert ("tip-9-1", "reciprocity") in rules
    assert ("09-decision-example-y", "example-category") in rules
    assert str(Finding("error", "p", "m", "link")) == "ERROR   p: m"
