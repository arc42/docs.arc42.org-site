from braingen.cli import main
from tests import vaultkit as vk


def build(tmp_path):
    vault_root, site = tmp_path / "vault", tmp_path / "site"
    vk.source(vault_root)
    vk.section(vault_root)
    vk.tip(vault_root, "9-1")
    vk.example(vault_root)
    return vault_root, site


def test_generate_then_check_generated_then_parity(tmp_path, capsys):
    vault_root, site = build(tmp_path)
    args = ["--vault", str(vault_root), "--site", str(site)]

    assert main(["check-generated", *args]) == 1
    assert "_pages/section-9.md: missing, run make generate" in capsys.readouterr().out

    assert main(["generate", *args]) == 0
    assert "3 written, 0 deleted, 0 unchanged" in capsys.readouterr().out

    assert main(["check-generated", *args]) == 0
    assert "generated files: 0 problems" in capsys.readouterr().out

    assert main(["generate-check", *args, "--section", "9", "--out", str(tmp_path / "parity")]) == 0
    out = capsys.readouterr().out
    assert "section 9: PASS (3 files compared)" in out
    assert "1 sections checked, 0 failed" in out
    assert (tmp_path / "parity/section-9/_pages/section-9.md").exists()


def test_generate_stops_on_lint_errors(tmp_path, capsys):
    vault_root, site = tmp_path / "vault", tmp_path / "site"
    vk.section(vault_root)   # its source page does not exist: unresolved link, a lint error
    assert main(["generate", "--vault", str(vault_root), "--site", str(site)]) == 1
    assert "generate stopped: 1 lint errors" in capsys.readouterr().out
    assert not site.exists()


def test_generate_refuses_to_overwrite_a_hand_written_original(tmp_path, capsys):
    vault_root, site = build(tmp_path)
    (site / "_pages").mkdir(parents=True)
    (site / "_pages/section-9.md").write_text("---\ntitle: hand\n---\nhand\n", encoding="utf-8")
    assert main(["generate", "--vault", str(vault_root), "--site", str(site)]) == 1
    assert "refusing to overwrite" in capsys.readouterr().out
