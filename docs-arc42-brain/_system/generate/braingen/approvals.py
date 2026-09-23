"""Approved edits to published bodies (ADR-0006).

`tests/test_parity.py::test_parity_against_the_ingested_originals` compares
every ingested section against the immutable copy in `raw/ingested/`. That is
the only guard that survives cut-over, and it is also the reason the brain
could not correct a single word of a published page: any deliberate edit made
the guard fail, and the only way past it was to weaken the guard.

This module is the way past it that keeps the guard. An edit to a published
body is recorded in `_system/approved-body-edits.tsv` as

    <site path>\t<fingerprint>\t<ISS-NNN>\t<date>\t<reason>

where the fingerprint is the sha256 of the *normalised* body the edit
produces. The comparison then treats that one body as expected and reports it
as a note instead of a failure.

The fingerprint is what makes this per-change rather than per-file. A later
edit to the same page produces a different body, so its fingerprint no longer
matches and the guard fails again until that edit is approved in its turn. A
line in this file exempts one version of one page and nothing else — not the
page's front matter, not its tags, and not the next edit.

Approvals are granted by a human: `braingen approve-edit` prints the diff the
edit makes and records nothing unless it is re-run with `--yes`.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from .compare import normalise_lines, split_foot

REGISTER = "_system/approved-body-edits.tsv"

HEADER = """\
# Approved edits to published bodies — append-only, see _system/adr/0006-approved-body-edits.md
# Each line exempts ONE version of ONE page from the raw-parity body comparison.
# <site path>\tsha256 of the normalised new body\tissue\tdate\treason
"""


@dataclass(frozen=True)
class Approval:
    rel: str
    fingerprint: str
    issue: str
    date: str
    reason: str

    def line(self) -> str:
        return "\t".join((self.rel, self.fingerprint, self.issue, self.date, self.reason))


def fingerprint(body: str) -> str:
    """sha256 of the body as the comparison sees it: foot removed, lines normalised.

    Whitespace the comparison already ignores must not invalidate an approval,
    or a reflowed paragraph would need re-approving for no change a reader sees.
    """
    text, _ = split_foot(body)
    return hashlib.sha256("\n".join(normalise_lines(text)).encode("utf-8")).hexdigest()


def register_path(vault: Path) -> Path:
    return Path(vault) / REGISTER


def load(vault: Path) -> dict[tuple[str, str], Approval]:
    """(site path, fingerprint) → approval. Missing register means no approvals."""
    path = register_path(vault)
    if not path.exists():
        return {}
    out: dict[tuple[str, str], Approval] = {}
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 5:
            raise ValueError(f"{REGISTER}:{n}: expected 5 tab-separated fields, got {len(parts)}")
        a = Approval(*parts)
        out[(a.rel, a.fingerprint)] = a
    return out


def append(vault: Path, approval: Approval) -> Path:
    path = register_path(vault)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(HEADER, encoding="utf-8")
    with path.open("a", encoding="utf-8") as f:
        f.write(approval.line() + "\n")
    return path


def original_from_raw(vault: Path, rel: str) -> str | None:
    """The hand-written original of a site file, from the immutable raw batches.

    `raw/ingested/<batch>/{pages,posts,examples}/<name>` mirrors the site's
    `_pages/`, `_posts/<dir>/` and `_examples/`, so the basename is enough to
    find it; batch names are unique per section and the basenames are the
    site's own.
    """
    name = Path(rel).name
    for batch in sorted((Path(vault) / "raw" / "ingested").glob("*")):
        for sub in ("pages", "posts", "examples"):
            f = batch / sub / name
            if f.exists():
                return f.read_text(encoding="utf-8")
    return None
