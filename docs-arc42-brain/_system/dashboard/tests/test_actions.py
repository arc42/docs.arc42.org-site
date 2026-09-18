import json
from datetime import datetime

import pytest

from . import fake_make
from actions import Runner, actions_view
from model import Model

NOW = lambda: datetime(2026, 9, 18, 10, 30, 0)


@pytest.fixture
def runner(repo, tmp_path, monkeypatch):
    rec = fake_make.install(tmp_path, monkeypatch)
    r = Runner(repo, braingen="BG", now=NOW)
    r.record = rec
    return r


def calls(r):
    return [json.loads(l) for l in r.record.read_text().splitlines()]


def log_text(repo):
    return (repo / "docs-arc42-brain/_system/log.md").read_text()


def test_generate_success(runner, repo):
    job = runner.run("generate")
    assert [c[2] for c in calls(runner)] == ["brain-lint", "generate"]
    assert calls(runner)[0] == ["-C", str(repo), "brain-lint", "BRAINGEN=BG"]
    assert job.exit_code == 0 and job.stage == "generate" and job.summary["changed"] == 3
    assert log_text(repo).endswith("\n\n## [2026-09-18] generate | dashboard, 3 files changed\n")
    run_file = repo / job.summary["run_file"]
    assert run_file.name == "20260918-103000-generate.log" and "2 written" in run_file.read_text()


def test_lint_gates_generate(runner, repo, monkeypatch):
    monkeypatch.setenv("FAKE_LINT_EXIT", "1")
    before = log_text(repo)
    job = runner.run("generate")
    assert [c[2] for c in calls(runner)] == ["brain-lint"]
    assert job.stage == "lint" and job.exit_code == 1
    assert log_text(repo) == before


def test_failure_shape(runner, repo, monkeypatch):
    monkeypatch.setenv("FAKE_GEN_EXIT", "2")
    monkeypatch.setenv("FAKE_GEN_LINES", "300")
    before = log_text(repo)
    job = runner.run("generate")
    d = job.to_dict()
    assert d["exit_code"] == 2 and d["stage"] == "generate" and len(d["tail"]) == 200
    assert log_text(repo) == before
    assert "wrote   f0.md" in (repo / job.summary["run_file"]).read_text()


def test_preview_caches_parity_without_log(runner, repo):
    before = log_text(repo)
    job = runner.run("preview")
    assert job.summary["sections"] == {"3": "PASS", "9": "FAIL"}
    assert runner.parity() == {"3": "PASS", "9": "FAIL"}
    assert json.loads((repo / "docs-arc42-brain/build/dashboard/parity.json").read_text())["sections"]["9"] == "FAIL"
    assert log_text(repo) == before


def test_one_job_at_a_time(runner):
    runner.lock.acquire()
    try:
        from actions import Job
        runner.current = Job("generate", "t")
        job, started = runner.start("preview")
        assert started is False and job is runner.current
    finally:
        runner.lock.release()


def test_start_runs_in_background_and_releases(runner):
    job, started = runner.start("preview")
    assert started is True
    for _ in range(100):
        if runner.current is None:
            break
        import time; time.sleep(0.05)
    assert runner.current is None and runner.last.kind == "preview" and not runner.lock.locked()


# -- actions_view (render-ready data for /actions) ---------------------------


def test_actions_view_no_runs_yet(runner, repo):
    b = Model(repo).get()
    view = actions_view(b, runner)
    assert view["job"] is None and view["is_current"] is False and view["lint"] is None
    assert {r["number"] for r in view["parity_rows"]} == {3, 9}
    assert all(r["parity"] is None for r in view["parity_rows"])


def test_actions_view_shows_last_job_and_parity(runner, repo):
    b = Model(repo).get()
    runner.last = runner.run("preview")  # run() itself doesn't set .last; start() does
    view = actions_view(b, runner)
    assert view["job"]["kind"] == "preview" and view["is_current"] is False
    assert view["lint"] is None
    rows = {r["number"]: r for r in view["parity_rows"]}
    assert rows[3]["parity"] == "PASS" and rows[9]["parity"] == "FAIL"


def test_actions_view_shows_lint_groups_when_lint_gated(runner, repo, monkeypatch):
    monkeypatch.setenv("FAKE_LINT_EXIT", "1")
    b = Model(repo).get()
    runner.last = runner.run("generate")  # run() itself doesn't set .last; start() does
    view = actions_view(b, runner)
    assert view["job"]["stage"] == "lint"
    assert view["lint"] is not None and "example-category" in view["lint"]["errors"]
