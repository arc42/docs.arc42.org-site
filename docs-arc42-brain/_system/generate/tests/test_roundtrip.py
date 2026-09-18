"""Round trip on real pages: original -> importer -> wiki page -> emitter -> original.

The fixtures under fixtures/roundtrip/ are verbatim copies of site files:
sections 5, 10 and 11 were picked for their irregularities (5: two callouts
under one heading and callouts under H3 headings; 10: the hard-coded image
path and H2 guidance headings inside a subsection; 11: no blank line after the
front matter and a raw <a> inside a blockquote), plus one tip and one example
of section 9. The emitters are the importer inverted; this test is their
contract, and compare_file is the parity check's per-file rule.
"""
from pathlib import Path

import pytest
import yaml

from braingen.importer import convert_example, convert_section, convert_tip, write_page
from braingen.parse import load_vault

FIX = Path(__file__).parent / "fixtures" / "roundtrip"
TODAY = "2026-09-18"
SRC = "SRC-999-roundtrip"
SECTION_9_MANIFEST = {"section": 9, "posts_dir": "09-decisions"}
SECTION_9_META = {
    "id": "section-9", "type": "section", "title": "9 - Architecture decisions", "status": "draft",
    "created": TODAY, "updated": TODAY, "sources": [], "related": [], "number": 9,
    "name": "Architecture Decisions", "category": "decisions", "posts-dir": "09-decisions",
    "permalink": "/section-9/", "order": 13, "faq-topic": "fundamental architecture and design decisions",
}
EXPECTED_NOTES = {
    5: [],
    10: ["expected difference: hard-coded image path normalised to {{ site.imageurl }} at ingest (spec Appendix A)"],
    11: ["normalised: 0 blank lines after the front matter in the original, 1 generated"],
}

@pytest.mark.parametrize("n", [5, 10, 11])
def test_section_round_trip(tmp_path, n):
    from braingen.compare import compare_file
    from braingen.emit import emit_section

    original = (FIX / f"section-{n}.md").read_text(encoding="utf-8")
    manifest = yaml.safe_load((FIX / f"section-{n}.manifest.yaml").read_text(encoding="utf-8"))
    meta, body = convert_section(original, manifest, TODAY, SRC)
    write_page(tmp_path / "wiki/sections" / f"section-{n}.md", meta, body)
    vault = load_vault(tmp_path)

    out = emit_section(vault, vault.pages[f"section-{n}"])

    assert out.rel == f"_pages/section-{n}.md"
    rep = compare_file(out.rel, original, out.text, n, {})
    assert rep.problems == []
    assert rep.notes == EXPECTED_NOTES[n]


def _section_9(root: Path) -> None:
    write_page(root / "wiki/sections/section-9.md", SECTION_9_META, "# 9. Architecture Decisions\n")


def test_tip_round_trip(tmp_path):
    from braingen.compare import compare_file
    from braingen.emit import emit_tip

    name = "2016-03-01-t-9-2.md"
    original = (FIX / name).read_text(encoding="utf-8")
    _section_9(tmp_path)
    meta, body = convert_tip(name, original, SECTION_9_MANIFEST, TODAY, SRC)
    write_page(tmp_path / "wiki/tips/tip-9-2.md", meta, body)
    vault = load_vault(tmp_path)

    out = emit_tip(vault, vault.pages["tip-9-2"], set(), set())

    assert out.rel == "_posts/09-decisions/" + name
    rep = compare_file(out.rel, original, out.text, 9, {})
    assert rep.problems == []   # tags differ (legacy tags are not mapped here): notes only


def test_example_round_trip(tmp_path):
    from braingen.compare import compare_file
    from braingen.emit import emit_example

    name = "09-decision-example-adr.md"
    original = (FIX / name).read_text(encoding="utf-8")
    _section_9(tmp_path)
    meta, body = convert_example(name, original, SECTION_9_MANIFEST, TODAY, SRC)
    write_page(tmp_path / "wiki/examples" / name, meta, body)
    vault = load_vault(tmp_path)

    out = emit_example(vault, vault.pages["09-decision-example-adr"], set(), set())

    assert out.rel == "_examples/" + name
    rep = compare_file(out.rel, original, out.text, 9, {})
    assert rep.problems == []
