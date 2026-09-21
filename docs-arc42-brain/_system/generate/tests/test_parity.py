import re
import shutil
from pathlib import Path

import pytest
import yaml

from braingen import parity
from braingen.generate import plan
from braingen.parity import PARITY_STATUSES, check_section, format_report, keyword_page_changes
from braingen.parse import load_vault
from tests import vaultkit as vk

# tests/ -> generate/ -> _system/ -> docs-arc42-brain/
REPO_VAULT = Path(__file__).resolve().parents[3]
BUILT_IDS = ["9-architecture-decisions", "background-on-adrs", "examples",
             "practical-tips", "related-questions", "complete-examples"]


def setup(tmp_path):
    vault_root, site = tmp_path / "vault", tmp_path / "site"
    vk.section(vault_root, status="draft")
    vk.term(vault_root, "architecture-decision", "Architecture decision", legacy=["decision"])
    vk.tip(vault_root, "9-1", status="review", terms=["[[architecture-decision]]"])
    vk.example(vault_root, status="review")
    return vault_root, site


def write_originals(vault_root, site, tags="decision"):
    """The site as it was before the brain: generated text minus marker, legacy tags."""
    for o in plan(load_vault(vault_root), statuses=PARITY_STATUSES).outputs:
        lines = [l for l in o.text.splitlines() if not l.startswith("# generated from docs-arc42-brain/")]
        text = "\n".join(lines) + "\n"
        if o.rel.startswith("_posts/"):
            text = text.replace("tags: architecture-decision", f"tags: {tags}")
        f = site / o.rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")


def built_page(site, ids):
    f = site / "_site/section-9/index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("\n".join(f'<h2 class="x" id="{i}">t</h2>' for i in ids), encoding="utf-8")


def test_matching_site_passes_whatever_the_status(tmp_path):
    vault_root, site = setup(tmp_path)
    write_originals(vault_root, site)

    rep = check_section(load_vault(vault_root), site, 9, tmp_path / "out")

    assert rep.ok
    assert [f.rel for f in rep.files] == ["_examples/09-decision-example-x.md", "_pages/section-9.md",
                                          "_posts/09-decisions/2016-03-01-t-9-1.md"]
    assert (tmp_path / "out/section-9/_pages/section-9.md").exists()
    assert "anchors not compared: _site/section-9/index.html not built (make site)" in rep.notes
    tip = rep.files[2]
    assert tip.notes[0] == "tags on the site: -['decision'] +['architecture-decision']"
    assert "keyword page tag counts: architecture-decision 0→1, decision 1→0" in rep.notes
    assert "keyword page loses tags: ['decision']" in rep.notes
    assert "keyword page gains tags: ['architecture-decision']" in rep.notes


def test_changed_value_fails_and_is_formatted(tmp_path):
    vault_root, site = setup(tmp_path)
    write_originals(vault_root, site)
    f = site / "_posts/09-decisions/2016-03-01-t-9-1.md"
    f.write_text(f.read_text(encoding="utf-8").replace("/tips/9-1/", "/tips/old/"), encoding="utf-8")

    rep = check_section(load_vault(vault_root), site, 9, tmp_path / "out")

    assert not rep.ok
    text = format_report(rep)
    assert text.startswith("section 9: FAIL (3 files compared)")
    assert "FAIL _posts/09-decisions/2016-03-01-t-9-1.md" in text
    assert "! front matter: permalink: '/tips/old/' -> '/tips/9-1/'" in text


def test_brain_page_without_original_is_new_and_site_file_without_page_is_not_ingested(tmp_path):
    vault_root, site = setup(tmp_path)
    write_originals(vault_root, site)
    vk.tip(vault_root, "9-2", status="review")
    (site / "_posts/09-decisions/2016-03-01-t-9-9.md").write_text("---\ntags: x\n---\nold\n", encoding="utf-8")
    (site / "_examples/09-other.md").write_text("---\ncategory: decisions\n---\nold\n", encoding="utf-8")

    rep = check_section(load_vault(vault_root), site, 9, tmp_path / "out")

    assert rep.ok
    new = [f for f in rep.files if f.rel == "_posts/09-decisions/2016-03-01-t-9-2.md"][0]
    assert new.notes == ["new: no original on the site"]
    assert "not ingested: 2 site files of this section have no brain page" in rep.notes


def test_section_not_in_brain(tmp_path):
    vault_root, site = setup(tmp_path)
    rep = check_section(load_vault(vault_root), site, 5, tmp_path / "out")
    assert rep.ok and rep.files == []
    assert rep.notes == ["section-5 is not in the brain"]


def test_keyword_page_changes_ignore_tags_still_used_elsewhere(tmp_path):
    vault_root, site = setup(tmp_path)
    write_originals(vault_root, site)
    other = site / "_posts/04-strategy/2016-01-01-t-4-1.md"
    other.parent.mkdir(parents=True)
    other.write_text("---\ntags: decision\n---\nx\n", encoding="utf-8")
    changes = keyword_page_changes(site, plan(load_vault(vault_root), statuses=PARITY_STATUSES))
    assert changes == {"decision": (2, 1), "architecture-decision": (0, 1)}


def test_anchors_against_the_built_page(tmp_path, monkeypatch):
    vault_root, site = setup(tmp_path)
    write_originals(vault_root, site)
    built_page(site, BUILT_IDS)
    assert check_section(load_vault(vault_root), site, 9, tmp_path / "out").ok

    built_page(site, [i for i in BUILT_IDS if i != "background-on-adrs"] + ["background"])
    rep = check_section(load_vault(vault_root), site, 9, tmp_path / "out")
    assert not rep.ok
    assert rep.files[-1].problems == ["anchor background-on-adrs ('Background (on ADRs)') not on the built page"]

    monkeypatch.setattr(parity, "EXPECTED_ANCHORS", [(9, "background-on-adrs", "background", "test reason")])
    rep = check_section(load_vault(vault_root), site, 9, tmp_path / "out")
    assert rep.ok
    assert "expected difference: anchor background-on-adrs is background on the site (test reason)" in rep.notes


# Site files live in these batch subfolders; `assets/` is copied by generate
# but never compared, so it is not part of a section's file count.
COMPARED_SUBS = ("pages", "posts", "examples")

# Sections whose content was ingested when this test was parametrised. The
# parametrisation itself is discovered (see `ingested_sections`), and this is
# the floor that keeps a discovery bug from quietly reducing it to nothing.
SECTIONS_INGESTED_BY_2026_09_21 = {1, 2, 4, 9}


def section_batches(section: int) -> list[Path]:
    """The raw/ingested batches of exactly this section.

    The batch kinds are spelled out (`content|page|all`, the values of
    `braingen raw --what`) rather than left to `section-{n}-*`, so anything
    else that ends up in `raw/ingested/` is not swept into a section's
    originals. `section-{n}-*` is in fact safe for the digits themselves —
    it needs the hyphen, so `section-1-*` never matches `section-10-page`.
    """
    pattern = re.compile(rf"^section-{section}-(content|page|all)$")
    return sorted(b for b in (REPO_VAULT / "raw/ingested").glob("section-*")
                   if pattern.match(b.name))


def ingested_sections() -> list[int]:
    """Every section with a content batch in raw/ingested/, discovered rather
    than listed, so the next ingest is covered the moment its batch lands."""
    found = {int(m.group(1))
             for b in (REPO_VAULT / "raw/ingested").glob("section-*-content")
             if (m := re.match(r"^section-(\d+)-content$", b.name))}
    return sorted(found)


def original_file_count(section: int) -> int:
    """How many site files the raw batches hold for this section, read from
    the manifests. Derived from the raw side on purpose: a count taken from
    the brain would rise and fall with the emitters it is meant to police."""
    return sum(
        1
        for batch in section_batches(section)
        for f in yaml.safe_load((batch / "manifest.yaml").read_text(encoding="utf-8")).get("files", [])
        if f.split("/")[0] in COMPARED_SUBS
    )


def site_from_raw(tmp: Path, section: int) -> Path:
    """Rebuild the section's pre-brain site files from the immutable raw/ingested/ batches."""
    site = tmp / "site"
    for batch in section_batches(section):
        manifest = yaml.safe_load((batch / "manifest.yaml").read_text(encoding="utf-8"))
        for sub, dest in (("pages", "_pages"), ("posts", f"_posts/{manifest['posts_dir']}"), ("examples", "_examples")):
            for f in sorted((batch / sub).glob("*.md")):
                target = site / dest / f.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, target)
    return site


def test_every_ingested_section_is_covered_by_the_parity_test():
    """The parametrisation is discovered, so it can silently shrink. Two
    guards: it never drops below the sections ingested when this was written,
    and every discovered section really has originals to compare against."""
    sections = set(ingested_sections())
    assert SECTIONS_INGESTED_BY_2026_09_21 <= sections, (
        f"discovery lost sections: {SECTIONS_INGESTED_BY_2026_09_21 - sections}")
    for section in sorted(sections):
        assert original_file_count(section) > 0, f"section {section}: no originals in raw/ingested/"


@pytest.mark.parametrize("section", ingested_sections(), ids=lambda n: f"section-{n}")
def test_parity_against_the_ingested_originals(tmp_path, section):
    """Brain spec §10, for every ingested section: compare the brain against
    the originals captured in `raw/ingested/` at ingest time.

    This is the only guard that survives cut-over. Once a section is
    published, `make generate-check` compares the generated site files with
    themselves and passes whatever the emitters do; the raw batch is the last
    copy of the hand-written original outside git history.
    """
    site = site_from_raw(tmp_path, section)

    rep = check_section(load_vault(REPO_VAULT), site, section, tmp_path / "parity")

    assert [f.rel for f in rep.files if not f.ok] == [], format_report(rep)
    assert len(rep.files) == original_file_count(section)
    assert not [n for n in rep.notes if n.startswith("not ingested")]
