from braingen.lint import lint
from braingen.parse import load_vault


def test_fixture_lint_matches_the_plan(vault_root):
    findings = lint(load_vault(vault_root))
    errors = sorted((f.rule, f.page) for f in findings if f.level == "error")
    warnings = sorted((f.rule, f.page) for f in findings if f.level == "warning")
    assert errors == [("example-category", "09-decision-example-y")]
    assert warnings == [("reciprocity", "ISS-001"), ("reciprocity", "ISS-002")]
