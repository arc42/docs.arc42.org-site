"""Compare one generated file with its hand-written original (brain spec §6).

Pass condition:
- body identical after normalisation: trailing whitespace per line (a trailing
  run of 2+ spaces is markdown's hard line break and is kept, normalised to
  exactly two; any other trailing whitespace is stripped), leading and
  trailing blank lines, and the further-info foot, which is
  compared by its arguments because its line layout varies between the
  hand-written pages;
- every front-matter key of the original has an identical value in the
  generated file, except `tags`; new keys (`related`) are allowed;
- `tags` differences are reported as notes, raw and after alias
  normalisation, and never fail.

EXPECTED_BODY lists the documented differences; each is applied to the
original before comparing and reported as a note.

A body difference the brain introduced on purpose passes only when it is
recorded in `_system/approved-body-edits.tsv` (ADR-0006): `approvals` maps
(site path, fingerprint of the new body) to the approval, and a hit turns the
failure into a note naming the issue that authorised it. An unapproved
difference still fails, and so does a *further* edit to an approved page,
because its body has a different fingerprint.
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field

import frontmatter

from .emit_body import is_generated

FOOT_RE = re.compile(r"\{%\s*include further-info\.md(.*?)%\}", re.S)
ARG_RE = re.compile(r'([a-z]+)="([^"]*)"')

# (section number, text in the original, replacement, why)
EXPECTED_BODY: list[tuple[int, str, str, str]] = [
    (10, "](/assets/images/sections/", "]({{ site.imageurl }}/",
     "hard-coded image path normalised to {{ site.imageurl }} at ingest (spec Appendix A)"),
]


@dataclass
class FileReport:
    rel: str
    ok: bool = True
    problems: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


HARD_BREAK_RE = re.compile(r" {2,}$")


def _fingerprint(body: str) -> str:
    from .approvals import fingerprint

    return fingerprint(body)


def normalise_line(line: str) -> str:
    """Strip trailing whitespace, but keep a markdown hard line break (2+ trailing
    spaces) as exactly two spaces rather than stripping it away."""
    m = HARD_BREAK_RE.search(line)
    return line[: m.start()] + "  " if m else line.rstrip()


def normalise_lines(text: str) -> list[str]:
    lines = [normalise_line(l) for l in text.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return lines


def split_foot(body: str) -> tuple[str, dict[str, str] | None]:
    m = FOOT_RE.search(body)
    if not m:
        return body, None
    return body[: m.start()] + body[m.end():], dict(ARG_RE.findall(m.group(1)))


def split_tags(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return value.split()
    return [str(t) for t in value]


def leading_blank_lines(text: str) -> int:
    end = text.find("\n---\n", 3)
    rest = text[end + 5:] if text.startswith("---\n") and end >= 0 else text
    return len(rest) - len(rest.lstrip("\n"))


def compare_file(rel: str, original: str, generated: str, section: int, aliases: dict[str, str],
                 approvals: dict | None = None) -> FileReport:
    rep = FileReport(rel)
    o, g = frontmatter.loads(original), frontmatter.loads(generated)
    for key, value in o.metadata.items():
        if key == "tags":
            continue
        if key not in g.metadata:
            rep.problems.append(f"front matter: key '{key}' missing")
        elif g.metadata[key] != value:
            rep.problems.append(f"front matter: {key}: {value!r} -> {g.metadata[key]!r}")
    old, new = split_tags(o.metadata.get("tags")), split_tags(g.metadata.get("tags"))
    if set(old) != set(new):
        rep.notes.append(f"tags on the site: -{sorted(set(old) - set(new))} +{sorted(set(new) - set(old))}")
        norm = {aliases.get(t, t) for t in old}
        if norm != set(new):
            rep.notes.append(f"tags after alias normalisation: -{sorted(norm - set(new))} +{sorted(set(new) - norm)}")
    lead = leading_blank_lines(original)
    if lead != 1 and not is_generated(original):
        rep.notes.append(f"normalised: {lead} blank lines after the front matter in the original, 1 generated")
    obody = o.content
    for n, old_text, new_text, why in EXPECTED_BODY:
        if n == section and old_text in obody:
            obody = obody.replace(old_text, new_text)
            rep.notes.append(f"expected difference: {why}")
    obody, ofoot = split_foot(obody)
    gbody, gfoot = split_foot(g.content)
    if ofoot != gfoot:
        rep.problems.append(f"further-info foot: {ofoot} -> {gfoot}")
    ol, gl = normalise_lines(obody), normalise_lines(gbody)
    if ol != gl:
        approved = (approvals or {}).get((rel, _fingerprint(gbody)))
        if approved:
            rep.notes.append(
                f"approved body edit ({approved.issue}, {approved.date}): {approved.reason}")
        else:
            diff = list(difflib.unified_diff(ol, gl, "original", "generated", lineterm="", n=1))
            rep.problems.append("body differs:\n    " + "\n    ".join(diff[:40]))
    rep.ok = not rep.problems
    return rep
