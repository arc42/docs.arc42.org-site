"""ADR-0006: a body edit to a published page passes the parity comparison only
when it is approved, and an approval covers exactly the body it was shown."""
from pathlib import Path

import pytest

from braingen import approvals
from braingen.approvals import Approval, append, fingerprint, load, original_from_raw
from braingen.cli import main
from braingen.compare import compare_file

ORIGINAL = "---\ntitle: t\ntags: decision\n---\n\nOne line.\n"
EDITED = "---\ntitle: t\ntags: decision\n---\n\nOne line, corrected.\n"


def report(tmp_path, generated=EDITED, approvals_map=None):
    return compare_file("_pages/section-9.md", ORIGINAL, generated, 9, {}, approvals_map)


def test_an_unapproved_body_edit_still_fails(tmp_path):
    rep = report(tmp_path)
    assert not rep.ok
    assert rep.problems[0].startswith("body differs:")


def test_an_approved_body_edit_passes_as_a_note(tmp_path):
    a = Approval("_pages/section-9.md", fingerprint("\nOne line, corrected.\n"),
                 "ISS-002", "2026-09-23", "why")
    rep = report(tmp_path, approvals_map={(a.rel, a.fingerprint): a})
    assert rep.ok
    assert rep.notes == ["approved body edit (ISS-002, 2026-09-23): why"]


def test_an_approval_does_not_cover_the_next_edit(tmp_path):
    """The point of the fingerprint: one line exempts one version of one page."""
    a = Approval("_pages/section-9.md", fingerprint("\nOne line, corrected.\n"),
                 "ISS-002", "2026-09-23", "why")
    rep = report(tmp_path, generated=EDITED.replace("corrected", "corrected again"),
                 approvals_map={(a.rel, a.fingerprint): a})
    assert not rep.ok


def test_an_approval_does_not_cover_another_page(tmp_path):
    a = Approval("_pages/section-4.md", fingerprint("\nOne line, corrected.\n"),
                 "ISS-002", "2026-09-23", "why")
    rep = report(tmp_path, approvals_map={(a.rel, a.fingerprint): a})
    assert not rep.ok


def test_the_fingerprint_ignores_whitespace_the_comparison_ignores():
    assert fingerprint("\n\nOne line.  \n\n") == fingerprint("One line.  ")
    assert fingerprint("One line.") != fingerprint("One line, corrected.")


def test_register_round_trip_and_missing_file(tmp_path):
    assert load(tmp_path) == {}
    a = Approval("_pages/section-9.md", "abc", "ISS-002", "2026-09-23", "why")
    path = append(tmp_path, a)
    assert path.read_text(encoding="utf-8").startswith("# Approved edits")
    assert load(tmp_path) == {("_pages/section-9.md", "abc"): a}


def test_a_malformed_register_line_is_an_error_not_a_silent_skip(tmp_path):
    approvals.register_path(tmp_path).parent.mkdir(parents=True, exist_ok=True)
    approvals.register_path(tmp_path).write_text("a\tb\tc\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected 5 tab-separated fields"):
        load(tmp_path)


def test_original_from_raw_finds_the_ingested_copy(tmp_path):
    f = tmp_path / "raw/ingested/section-9-all/pages/section-9.md"
    f.parent.mkdir(parents=True)
    f.write_text(ORIGINAL, encoding="utf-8")
    assert original_from_raw(tmp_path, "_pages/section-9.md") == ORIGINAL
    assert original_from_raw(tmp_path, "_pages/section-4.md") is None


def test_approve_edit_records_nothing_without_yes(tmp_path, capsys, monkeypatch):
    """The whole point of the command: the diff is shown, the register is not touched."""
    from tests import vaultkit as vk

    vault = tmp_path / "vault"
    vk.section(vault, status="published")
    raw = vault / "raw/ingested/section-9-all/pages/section-9.md"
    raw.parent.mkdir(parents=True)
    raw.write_text("---\nlayout: page\ntitle: 9 - Architecture decisions\n---\n\nold body\n",
                   encoding="utf-8")

    args = ["approve-edit", "--vault", str(vault), "--rel", "_pages/section-9.md",
            "--issue", "ISS-002", "--reason", "why"]
    assert main(args) == 0, "the preview is the expected first step, not a failure"
    out = capsys.readouterr().out
    assert "not recorded" in out and "as it would be published" in out
    assert not approvals.register_path(vault).exists()

    assert main(args + ["--yes", "--today", "2026-09-23"]) == 0
    recorded = load(vault)
    assert [a.issue for a in recorded.values()] == ["ISS-002"]


def test_body_diff_applies_the_documented_ingest_normalisations():
    """compare_file rewrites section 10's hard-coded image paths before diffing;
    body_diff must do the same or every section 10 page looks edited."""
    from braingen.approvals import body_diff

    original = "---\ntitle: t\n---\n\n![x](/assets/images/sections/10/a.png)\n"
    generated = "---\ntitle: t\n---\n\n![x]({{ site.imageurl }}/10/a.png)\n"
    assert body_diff(original, generated, section=10)[0] == ""
    assert body_diff(original, generated, section=9)[0] != ""


def test_pending_lists_changed_bodies_and_marks_the_approved_ones(tmp_path):
    from braingen.approvals import Approval, append, fingerprint, pending

    raw = tmp_path / "raw/ingested/section-9-all/pages"
    raw.mkdir(parents=True)
    (raw / "section-9.md").write_text(ORIGINAL, encoding="utf-8")
    (raw / "section-4.md").write_text(ORIGINAL, encoding="utf-8")

    outputs = {
        "_pages/section-9.md": (EDITED, 9),
        "_pages/section-4.md": (ORIGINAL, 4),          # unchanged: not pending
        "_pages/section-7.md": (EDITED, 7),            # no original in raw/: skipped
    }
    items = pending(tmp_path, outputs)
    assert [p.rel for p in items] == ["_pages/section-9.md"]
    assert items[0].approved is None
    assert items[0].diff.startswith("--- as ingested")

    append(tmp_path, Approval("_pages/section-9.md", items[0].fingerprint,
                              "ISS-002", "2026-09-23", "why"))
    again = pending(tmp_path, outputs)
    assert again[0].approved is not None and again[0].approved.issue == "ISS-002"
    assert again[0].as_dict()["approved"]["reason"] == "why"
