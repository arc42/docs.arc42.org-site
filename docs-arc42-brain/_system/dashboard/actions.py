"""Generate/preview actions: the dashboard's only way to touch the site
(D18). A `Runner` serializes jobs with a process-wide lock, gates
`generate` on `brain-lint`, caches `generate-check` parity, writes a run
log for every job, and appends one log.md line per successful generate.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import threading
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

GENERATED_PATHS = ["_pages", "_posts", "_examples", "assets/images",
                    "docs-arc42-brain/_system/generated-assets.txt"]

_GEN_SUMMARY_RE = re.compile(r"(\d+) written, (\d+) deleted")
_PREVIEW_SECTION_RE = re.compile(r"^section (\d+): (PASS|FAIL)", re.MULTILINE)

_LOG_PATH = "docs-arc42-brain/_system/log.md"
_PARITY_PATH = "docs-arc42-brain/build/dashboard/parity.json"
_RUNS_DIR = "docs-arc42-brain/build/dashboard/runs"


@dataclass
class Job:
    kind: str                     # "generate" | "preview"
    started: str                  # ISO timestamp (local time, seconds)
    lines: list[str] = field(default_factory=list)
    finished: str | None = None
    exit_code: int | None = None
    stage: str | None = None      # "lint" | "generate" | "preview"
    summary: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "started": self.started,
            "finished": self.finished,
            "exit_code": self.exit_code,
            "stage": self.stage,
            "summary": self.summary,
            "tail": self.lines[-200:],
        }


class Runner:
    """Runs `generate`/`preview` through `make`, one job at a time."""

    def __init__(self, repo: Path, make: str = "make",
                 braingen: str = f"{sys.executable} -m braingen.cli",
                 now=datetime.now, on_finish=None):
        self.repo = Path(repo)
        self.make = make
        self.braingen = braingen
        self.now = now
        self.on_finish = on_finish
        self.lock = threading.Lock()
        self.current: Job | None = None
        self.last: Job | None = None
        self._parity: dict[str, str] = {}

    def parity(self) -> dict[str, str]:
        """The sections dict of the most recent preview, or {} if none."""
        return self._parity

    def start(self, kind: str) -> tuple[Job, bool]:
        """Start a job in a background thread. Returns (job, started);
        when another job is already running, returns (self.current, False)
        without starting anything."""
        if not self.lock.acquire(blocking=False):
            return self.current, False

        dt = self.now()
        job = Job(kind=kind, started=dt.isoformat(timespec="seconds"))
        self.current = job

        def body() -> None:
            try:
                self._execute(job, dt)
            finally:
                self.last = job
                self.current = None
                self.lock.release()
                if self.on_finish is not None:
                    self.on_finish()

        threading.Thread(target=body, daemon=True).start()
        return job, True

    def run(self, kind: str) -> Job:
        """Synchronous body: run a job to completion and return it. The
        caller holds no lock (used directly by tests, and by `start()`'s
        background thread via `_execute`)."""
        dt = self.now()
        job = Job(kind=kind, started=dt.isoformat(timespec="seconds"))
        return self._execute(job, dt)

    # -- shared implementation -------------------------------------------------

    def _execute(self, job: Job, dt: datetime) -> Job:
        if job.kind == "generate":
            self._generate(job, dt)
        elif job.kind == "preview":
            self._preview(job, dt)
        else:
            raise ValueError(f"unknown job kind: {job.kind!r}")
        return self._finalize(job, dt)

    def _generate(self, job: Job, dt: datetime) -> None:
        proc = self._make(job, "brain-lint")
        if proc.returncode != 0:
            job.stage = "lint"
            job.exit_code = proc.returncode
            return

        proc = self._make(job, "generate")
        if proc.returncode != 0:
            job.stage = "generate"
            job.exit_code = proc.returncode
            return

        match = _GEN_SUMMARY_RE.search(proc.stdout)
        changed = (int(match.group(1)) + int(match.group(2))) if match else 0
        job.summary["changed"] = changed

        self._append_log(dt, changed)

        job.summary["git_status"] = self._git(job, ["status", "--short"])
        job.summary["git_diff_stat"] = self._git(job, ["diff", "--stat"])

        job.exit_code = 0
        job.stage = "generate"

    def _preview(self, job: Job, dt: datetime) -> None:
        proc = self._make(job, "generate-check")
        job.stage = "preview"
        job.exit_code = proc.returncode

        sections = {m.group(1): m.group(2) for m in _PREVIEW_SECTION_RE.finditer(proc.stdout)}
        job.summary["sections"] = sections
        self._parity = sections

        parity_path = self.repo / _PARITY_PATH
        parity_path.parent.mkdir(parents=True, exist_ok=True)
        parity_path.write_text(
            json.dumps({"at": dt.isoformat(timespec="seconds"), "sections": sections}),
            encoding="utf-8",
        )

    def _finalize(self, job: Job, dt: datetime) -> Job:
        job.finished = self.now().isoformat(timespec="seconds")

        run_dir = self.repo / _RUNS_DIR
        run_dir.mkdir(parents=True, exist_ok=True)
        ts = dt.strftime("%Y%m%d-%H%M%S")
        run_path = run_dir / f"{ts}-{job.kind}.log"
        content = "\n".join(job.lines)
        run_path.write_text(content + "\n" if content else "", encoding="utf-8")
        job.summary["run_file"] = str(run_path.relative_to(self.repo))

        return job

    # -- commands ---------------------------------------------------------------

    def _make_argv(self, target: str) -> list[str]:
        return [self.make, "-C", str(self.repo), target, f"BRAINGEN={self.braingen}"]

    def _make(self, job: Job, target: str) -> subprocess.CompletedProcess:
        return self._run(job, self._make_argv(target))

    def _git(self, job: Job, args: list[str]) -> str:
        argv = ["git", "-C", str(self.repo), *args, "--", *GENERATED_PATHS]
        proc = self._run(job, argv)
        return proc.stdout if proc.returncode == 0 else proc.stderr

    def _run(self, job: Job, argv: list[str]) -> subprocess.CompletedProcess:
        job.lines.append("$ " + " ".join(argv))
        proc = subprocess.run(argv, cwd=self.repo, capture_output=True, text=True)
        if proc.stdout:
            job.lines.extend(proc.stdout.splitlines())
        if proc.stderr:
            job.lines.extend(proc.stderr.splitlines())
        return proc

    def _append_log(self, dt: datetime, changed: int) -> None:
        log_path = self.repo / _LOG_PATH
        text = log_path.read_text(encoding="utf-8")
        text = text.rstrip("\n") + "\n\n"
        text += f"## [{dt.strftime('%Y-%m-%d')}] generate | dashboard, {changed} files changed\n"
        log_path.write_text(text, encoding="utf-8")
