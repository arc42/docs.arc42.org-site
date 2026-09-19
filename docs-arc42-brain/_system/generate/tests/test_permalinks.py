from braingen.cli import main
from braingen.generate import plan
from braingen.lint import lint
from braingen.parse import load_vault
from braingen.permalinks import REGISTRY, RETIRED, check, read_registry, record
from tests import vaultkit as vk


def build(tmp_path):
    vault_root, site = tmp_path / "vault", tmp_path / "site"
    vk.source(vault_root)
    vk.section(vault_root)
    vk.tip(vault_root, "9-1")
    vk.example(vault_root)
    return vault_root, site


def test_record_lists_every_planned_permalink_with_its_page(tmp_path):
    vault_root, _ = build(tmp_path)
    vault = load_vault(vault_root)
    assert record(vault, plan(vault)) == 3
    assert read_registry(vault) == {
        "/section-9/": "section-9", "/tips/9-1/": "9-1", "/examples/decision-x/": "09-decision-example-x"}
    assert record(vault, plan(vault)) == 0          # idempotent
    text = (vault_root / REGISTRY).read_text()
    assert text.startswith("# ") and "/tips/9-1/\t9-1\n" in text


def test_registry_is_append_only(tmp_path):
    vault_root, _ = build(tmp_path)
    vault = load_vault(vault_root)
    record(vault, plan(vault))
    vk.tip(vault_root, "9-1", status="draft")
    vault = load_vault(vault_root)
    record(vault, plan(vault))
    assert "/tips/9-1/" in read_registry(vault)


def test_unpublishing_a_page_drops_its_url(tmp_path):
    vault_root, _ = build(tmp_path)
    vault = load_vault(vault_root)
    record(vault, plan(vault))
    vk.tip(vault_root, "9-1", status="draft")
    vault = load_vault(vault_root)
    assert check(vault, plan(vault)) == [
        "/tips/9-1/ (was 9-1) would no longer be served; keep the page published and the permalink "
        f"unchanged, or list the URL in {RETIRED} with a reason"]


def test_changing_a_permalink_drops_the_old_url(tmp_path):
    vault_root, _ = build(tmp_path)
    vault = load_vault(vault_root)
    record(vault, plan(vault))
    vk.tip(vault_root, "9-1", permalink="/tips/nine-one/")
    vault = load_vault(vault_root)
    problems = check(vault, plan(vault))
    assert len(problems) == 1 and problems[0].startswith("/tips/9-1/ (was 9-1)")


def test_retired_permalinks_are_allowed_to_go(tmp_path):
    vault_root, _ = build(tmp_path)
    vault = load_vault(vault_root)
    record(vault, plan(vault))
    vk.tip(vault_root, "9-1", status="draft")
    (vault_root / RETIRED).write_text("# header\n/tips/9-1/\tmerged into 9-2, see ISS-099\n")
    vault = load_vault(vault_root)
    assert check(vault, plan(vault)) == []


def test_retired_entry_needs_a_reason(tmp_path):
    vault_root, _ = build(tmp_path)
    vault = load_vault(vault_root)
    record(vault, plan(vault))
    vk.tip(vault_root, "9-1", status="draft")
    (vault_root / RETIRED).write_text("/tips/9-1/\n")
    vault = load_vault(vault_root)
    problems = check(vault, plan(vault))
    assert any("no reason" in p for p in problems)


def test_no_registry_means_nothing_to_protect(tmp_path):
    vault_root, _ = build(tmp_path)
    vault = load_vault(vault_root)
    assert check(vault, plan(vault)) == []


def test_generate_refuses_to_drop_a_url_and_writes_nothing(tmp_path, capsys):
    vault_root, site = build(tmp_path)
    args = ["--vault", str(vault_root), "--site", str(site)]
    assert main(["generate", *args]) == 0
    assert (vault_root / REGISTRY).exists()
    capsys.readouterr()
    vk.tip(vault_root, "9-1", status="draft")
    assert main(["generate", *args]) == 1
    out = capsys.readouterr().out
    assert "generate stopped: 1 published URLs would disappear" in out
    assert (site / "_posts/09-decisions/2016-03-01-t-9-1.md").exists()
    assert main(["check-generated", *args]) == 1
    assert "/tips/9-1/ (was 9-1) would no longer be served" in capsys.readouterr().out


def test_lint_flags_duplicate_permalinks(tmp_path):
    vault_root, _ = build(tmp_path)
    vk.tip(vault_root, "9-2", permalink="/tips/9-1/")
    rules = [(f.rule, f.page) for f in lint(load_vault(vault_root)) if f.level == "error"]
    assert ("permalink", "tip-9-2") in rules
