"""Generate/preview actions: the dashboard's only way to touch the site
(D18). A `Runner` serializes jobs with a process-wide lock, gates
`generate` on `brain-lint`, caches `generate-check` parity, writes a run
log for every job, and appends one log.md line per successful generate.

`Approvals` is the second, much smaller action: approving a correction to a
body the brain already publishes (ADR-0006). It is not a Runner job — the
calls are fast and synchronous, and the point is that a human reads a diff
and then says yes, which is a page and a button rather than a log tail.
"""
from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import sys
import threading
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from model import Brain, lint_view, sections_view

GENERATED_PATHS = ["_pages", "_posts", "_examples", "assets/images",
                    "docs-arc42-brain/_system/generated-assets.txt"]

_GEN_SUMMARY_RE = re.compile(r"(\d+) written, (\d+) deleted")
_PREVIEW_SECTION_RE = re.compile(r"^section (\d+): (PASS|FAIL)", re.MULTILINE)

_LOG_PATH = "docs-arc42-brain/_system/log.md"
_PARITY_PATH = "docs-arc42-brain/build/dashboard/parity.json"
_RUNS_DIR = "docs-arc42-brain/build/dashboard/runs"

_MAKE_TIMEOUT = 900   # seconds; brain-lint/generate/generate-check can be slow (Docker, braingen).
_GIT_TIMEOUT = 30
_TIMEOUT_EXIT_CODE = 124  # shell convention for "command timed out".


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
            "summary": dict(self.summary),
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
        """The sections dict of the most recent preview. Falls back to the
        on-disk `parity.json` (written by the last preview before this
        process started, e.g. before a restart) when there is no
        in-memory result yet."""
        if self._parity:
            return self._parity
        parity_path = self.repo / _PARITY_PATH
        try:
            data = json.loads(parity_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            return {}
        return data.get("sections", {})

    def start(self, kind: str) -> tuple[Job, bool]:
        """Start a job in a background thread. Returns (job, started);
        when another job is already running, returns (self.current, False)
        without starting anything. `self.current` can briefly be None while
        the lock is still held (just before a job is installed, or just
        after `body` clears it), so that case falls back to `self.last`
        rather than handing the caller a None job."""
        if not self.lock.acquire(blocking=False):
            return (self.current or self.last), False

        try:
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
        except Exception:
            # Creating the Job or starting the thread failed before `body`
            # (and its `finally`) ever got a chance to release the lock.
            self.current = None
            self.lock.release()
            raise
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
        """Run the job body and always finalize it, even when the body
        raises (e.g. log.md missing or unreadable in `_append_log`). A job
        that raised still ends up finished, with exit_code 1 and the last
        line of the traceback recorded, instead of being left in limbo
        with `finished`/`exit_code` stuck at None and no run file."""
        try:
            if job.kind == "generate":
                self._generate(job, dt)
            elif job.kind == "preview":
                self._preview(job, dt)
            else:
                raise ValueError(f"unknown job kind: {job.kind!r}")
        except Exception:
            job.exit_code = 1
            tb_lines = traceback.format_exc().rstrip("\n").splitlines()
            if tb_lines:
                job.lines.append(tb_lines[-1])
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

    @staticmethod
    def _unique_run_path(run_dir: Path, ts: str, kind: str) -> Path:
        """`{ts}-{kind}.log`, or `-2`, `-3`, … appended when two jobs finish
        in the same second (kind differs by job, so a collision only
        happens between two jobs of the same kind)."""
        path = run_dir / f"{ts}-{kind}.log"
        i = 2
        while path.exists():
            path = run_dir / f"{ts}-{kind}-{i}.log"
            i += 1
        return path

    def _finalize(self, job: Job, dt: datetime) -> Job:
        job.finished = self.now().isoformat(timespec="seconds")

        run_dir = self.repo / _RUNS_DIR
        run_dir.mkdir(parents=True, exist_ok=True)
        ts = dt.strftime("%Y%m%d-%H%M%S")
        run_path = self._unique_run_path(run_dir, ts, job.kind)
        content = "\n".join(job.lines)
        run_path.write_text(content + "\n" if content else "", encoding="utf-8")
        job.summary["run_file"] = str(run_path.relative_to(self.repo))

        return job

    # -- commands ---------------------------------------------------------------

    def _make_argv(self, target: str) -> list[str]:
        return [self.make, "-C", str(self.repo), target, f"BRAINGEN={self.braingen}"]

    def _make(self, job: Job, target: str) -> subprocess.CompletedProcess:
        return self._run(job, self._make_argv(target), timeout=_MAKE_TIMEOUT)

    def _git(self, job: Job, args: list[str]) -> str:
        argv = ["git", "-C", str(self.repo), *args, "--", *GENERATED_PATHS]
        proc = self._run(job, argv, timeout=_GIT_TIMEOUT)
        return proc.stdout if proc.returncode == 0 else proc.stderr

    def _run(self, job: Job, argv: list[str], timeout: float) -> subprocess.CompletedProcess:
        """Run `argv` in its own process group (`start_new_session=True`),
        so that on a timeout we can kill the whole group with `os.killpg`
        instead of only the direct child. `make` forks braingen as a
        grandchild; killing just `make` (what `subprocess.run(timeout=)`
        does) leaves that grandchild running past the timeout."""
        job.lines.append("$ " + " ".join(argv))
        proc = subprocess.Popen(
            argv, cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, start_new_session=True,
        )
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except ProcessLookupError:
                pass
            stdout, stderr = proc.communicate()
            if stdout:
                job.lines.extend(stdout.splitlines())
            if stderr:
                job.lines.extend(stderr.splitlines())
            job.lines.append(f"TIMEOUT after {timeout}s: " + " ".join(argv))
            return subprocess.CompletedProcess(argv, _TIMEOUT_EXIT_CODE, stdout or "", stderr or "")
        if stdout:
            job.lines.extend(stdout.splitlines())
        if stderr:
            job.lines.extend(stderr.splitlines())
        return subprocess.CompletedProcess(argv, proc.returncode, stdout, stderr)

    def _append_log(self, dt: datetime, changed: int) -> None:
        """Append one entry to log.md — never a read-modify-write of the
        whole file, which could lose a concurrent edit (Obsidian, Claude
        Code) or briefly expose a truncated file to another thread's
        `log_entries`/`Model.stamp`. Only the last couple of bytes are
        inspected, to add exactly the newline(s) needed so one blank line
        precedes the new entry."""
        log_path = self.repo / _LOG_PATH
        entry = f"## [{dt.strftime('%Y-%m-%d')}] generate | dashboard, {changed} files changed\n"
        with open(log_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            tail_len = min(size, 2)
            f.seek(size - tail_len, os.SEEK_SET)
            tail = f.read()
        trailing_newlines = len(tail) - len(tail.rstrip(b"\n"))
        prefix = "\n" * max(0, 2 - trailing_newlines) if size else ""
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(prefix + entry)


def actions_view(b: Brain, runner: Runner) -> dict:
    """Render-ready data for `/actions`: the current or last job (as a
    dict, or None), whether it is still running, lint groups when that
    job's stage is "lint" (the brain-lint gate that blocked generate), and
    one parity row per section."""
    job = runner.current or runner.last
    return {
        "job": job.to_dict() if job is not None else None,
        "is_current": runner.current is not None,
        "lint": lint_view(b) if job is not None and job.stage == "lint" else None,
        "parity_rows": sections_view(b, runner.parity())["rows"],
    }


_BRAINGEN_TIMEOUT = 120   # listing and approving are fast; this is a stuck-process guard.


class Approvals:
    """The ADR-0006 register, through `braingen`.

    Every correction to a published body has to be approved against its diff,
    and the register is append-only, so this class only ever lists and
    appends. It shells out rather than importing braingen because the
    dashboard runs in its own container with its own environment, exactly as
    the Runner does.
    """

    def __init__(self, repo: Path, braingen: str = f"{sys.executable} -m braingen.cli"):
        self.repo = Path(repo)
        self.braingen = braingen
        self.vault = self.repo / "docs-arc42-brain"

    def _argv(self, *args: str) -> list[str]:
        return [*self.braingen.split(), *args, "--vault", str(self.vault)]

    def _run(self, argv: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(argv, cwd=self.repo, capture_output=True, text=True,
                              timeout=_BRAINGEN_TIMEOUT)

    def pending(self) -> list[dict]:
        """Bodies that differ from the copy captured at ingest, unapproved first."""
        proc = self._run(self._argv("pending-edits", "--json"))
        if proc.returncode != 0:
            return []
        try:
            items = json.loads(proc.stdout)
        except json.JSONDecodeError:
            return []
        return sorted(items, key=lambda i: (i["approved"] is not None, i["rel"]))

    def approve(self, rel: str, issue: str, reason: str) -> tuple[bool, str]:
        """Append one approval. Returns (ok, output) for the flash message."""
        argv = self._argv("approve-edit", "--rel", rel, "--issue", issue,
                          "--reason", reason, "--yes")
        proc = self._run(argv)
        return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


def approvals_view(approvals: Approvals) -> dict:
    items = approvals.pending()
    return {
        "items": items,
        "waiting": sum(1 for i in items if i["approved"] is None),
    }
