import pytest

from braingen.generate import ASSET_MANIFEST, apply, check, conflicts, owned_files, plan
from braingen.parse import load_vault
from tests import vaultkit as vk

TIP_1 = "_posts/09-decisions/2016-03-01-t-9-1.md"
TIP_2 = "_posts/09-decisions/2016-03-01-t-9-2.md"


def setup(tmp_path, **tip2):
    vault_root, site = tmp_path / "vault", tmp_path / "site"
    vk.source(vault_root)
    vk.section(vault_root)
    vk.tip(vault_root, "9-1", related=["[[tip-9-2]]"])
    vk.tip(vault_root, "9-2", related=["[[tip-9-1]]"], **tip2)
    vk.example(vault_root)
    (site / "_posts/09-decisions").mkdir(parents=True)
    (site / "_pages").mkdir()
    (site / "_examples").mkdir()
    return vault_root, site


def test_plan_emits_published_pages_only(tmp_path):
    vault_root, _ = setup(tmp_path, status="review")
    p = plan(load_vault(vault_root))
    assert [o.rel for o in p.outputs] == ["_examples/09-decision-example-x.md", "_pages/section-9.md", TIP_1]


def test_plan_with_statuses_and_section_filter(tmp_path):
    vault_root, _ = setup(tmp_path, status="review")
    vk.section(vault_root, n=4)
    vault = load_vault(vault_root)
    p = plan(vault, statuses=frozenset({"published", "review"}), section=9)
    assert [o.rel for o in p.outputs] == ["_examples/09-decision-example-x.md", "_pages/section-9.md", TIP_1, TIP_2]
    assert [o.rel for o in plan(vault, section=4).outputs] == ["_pages/section-4.md"]


def test_apply_writes_then_is_idempotent(tmp_path):
    vault_root, site = setup(tmp_path)
    first = apply(load_vault(vault_root), site, plan(load_vault(vault_root)))
    assert sorted(first.written) == ["_examples/09-decision-example-x.md", "_pages/section-9.md", TIP_1, TIP_2]
    second = apply(load_vault(vault_root), site, plan(load_vault(vault_root)))
    assert second.written == [] and second.deleted == []
    assert len(second.unchanged) == 4
    assert sorted(owned_files(site)) == sorted(first.written)


def test_unpublishing_deletes_the_generated_file_and_the_links_to_it(tmp_path):
    vault_root, site = setup(tmp_path)
    apply(load_vault(vault_root), site, plan(load_vault(vault_root)))
    vk.tip(vault_root, "9-2", related=["[[tip-9-1]]"], status="retired")

    res = apply(load_vault(vault_root), site, plan(load_vault(vault_root)))

    assert res.deleted == [TIP_2]
    assert res.written == [TIP_1]           # its related link to 9-2 is gone
    assert "/tips/9-2/" not in (site / TIP_1).read_text(encoding="utf-8")


def test_files_without_marker_are_never_touched(tmp_path):
    vault_root, site = setup(tmp_path)
    hand = site / "_posts/09-decisions/2016-03-01-t-9-9.md"
    hand.write_text("---\ntitle: hand\n---\nhand-written\n", encoding="utf-8")
    apply(load_vault(vault_root), site, plan(load_vault(vault_root)))
    assert hand.read_text(encoding="utf-8") == "---\ntitle: hand\n---\nhand-written\n"


def test_hand_written_original_blocks_the_whole_run(tmp_path):
    vault_root, site = setup(tmp_path)
    (site / TIP_2).write_text("---\ntitle: original\n---\nbody\n", encoding="utf-8")
    vault = load_vault(vault_root)

    assert conflicts(vault, site, plan(vault)) == [f"{TIP_2}: hand-written file; delete the original first (cut-over)"]
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        apply(vault, site, plan(vault))
    assert not (site / TIP_1).exists()      # nothing was written


def test_assets_are_copied_listed_and_removed_when_unreferenced(tmp_path):
    vault_root, site = setup(tmp_path)
    vk.asset(vault_root, "sections/09/d.png")
    vk.tip(vault_root, "9-1", body="![d](../assets/sections/09/d.png)\n", related=["[[tip-9-2]]"])

    res = apply(load_vault(vault_root), site, plan(load_vault(vault_root)))

    assert "assets/images/sections/09/d.png" in res.written
    assert (site / "assets/images/sections/09/d.png").read_bytes() == b"\x89PNG test"
    assert "{{ site.imageurl }}/09/d.png" in (site / TIP_1).read_text(encoding="utf-8")
    manifest = (vault_root / ASSET_MANIFEST).read_text(encoding="utf-8")
    assert manifest.splitlines()[1:] == ["assets/images/sections/09/d.png"]

    vk.tip(vault_root, "9-1", related=["[[tip-9-2]]"])
    res = apply(load_vault(vault_root), site, plan(load_vault(vault_root)))
    assert "assets/images/sections/09/d.png" in res.deleted
    assert not (site / "assets/images/sections/09/d.png").exists()


def test_hand_made_asset_with_other_content_is_a_conflict(tmp_path):
    vault_root, site = setup(tmp_path)
    vk.asset(vault_root, "sections/09/d.png")
    vk.tip(vault_root, "9-1", body="![d](../assets/sections/09/d.png)\n")
    hand = site / "assets/images/sections/09/d.png"
    hand.parent.mkdir(parents=True)
    hand.write_bytes(b"other")
    vault = load_vault(vault_root)
    assert conflicts(vault, site, plan(vault)) == ["assets/images/sections/09/d.png: hand-made asset with different content"]


def test_check_is_clean_after_generate_and_reports_every_drift(tmp_path):
    vault_root, site = setup(tmp_path)
    vault = load_vault(vault_root)
    apply(vault, site, plan(vault))
    assert check(vault, site, plan(vault)) == []

    (site / TIP_1).write_text((site / TIP_1).read_text(encoding="utf-8") + "edited\n", encoding="utf-8")
    (site / TIP_2).unlink()
    stale = site / "_posts/09-decisions/2016-03-01-t-9-7.md"
    stale.write_text((site / "_pages/section-9.md").read_text(encoding="utf-8"), encoding="utf-8")

    assert check(vault, site, plan(vault)) == [
        f"{TIP_1}: hand-edited or stale, run make generate (edit wiki/tips/tip-9-1.md instead)",
        f"{TIP_2}: missing, run make generate",
        "_posts/09-decisions/2016-03-01-t-9-7.md: generated file without a published brain page, run make generate",
    ]
