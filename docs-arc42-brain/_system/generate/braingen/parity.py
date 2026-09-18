"""Parity check (brain spec §6): generate one section, compare it with the site.

The section's pages are generated whatever their status (retired excepted)
into <out>/section-N/, and every generated file is compared with the file at
the same path in the site by compare.compare_file. On top of that the report
carries, as notes that never fail:

- heading anchors vs. the built page in _site/ (if built; EXPECTED_ANCHORS
  lists the known divergences, anything else fails);
- site files of the section that have no brain page yet ("not ingested");
- tags that appear on or disappear from the /keywords/ page, which lists the
  tags of posts only (site.tags).
"""
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import frontmatter

from .compare import FileReport, compare_file, split_tags
from .generate import Plan, plan
from .parse import Vault

PARITY_STATUSES = frozenset({"draft", "review", "published"})
H_ID_RE = re.compile(r'<h[1-6][^>]*\sid="([^"]*)"')

# (section number, brain anchor, anchor on the built site, why)
EXPECTED_ANCHORS: list[tuple[int, str, str, str]] = [
    (7, "motivation-1", "motivation",
     'kramdown numbers headings inside markdown="1" divs separately; braingen keeps one counter'),
]


@dataclass
class SectionReport:
    section: int
    files: list[FileReport] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(f.ok for f in self.files)


def alias_table(vault: Vault) -> dict[str, str]:
    """Legacy tag / alias / slug → the tag the brain emits for it."""
    table: dict[str, str] = {}
    for p in vault.by_type("keyword"):
        table[p.slug] = p.slug
    for p in vault.by_type("term"):
        table[p.slug] = p.slug
        for a in list(p.meta.get("aliases") or []) + list(p.meta.get("legacy-tags") or []):
            table[str(a)] = p.slug
    return table


def anchor_check(vault: Vault, site: Path, section: int) -> tuple[list[str], list[str]]:
    """(problems, notes) from comparing the brain's anchors with the built page."""
    page = vault.pages.get(f"section-{section}")
    built = site / "_site" / f"section-{section}" / "index.html"
    if page is None:
        return [], []
    if not built.exists():
        return [], [f"anchors not compared: _site/section-{section}/index.html not built (make site)"]
    ids = set(H_ID_RE.findall(built.read_text(encoding="utf-8")))
    problems: list[str] = []
    notes: list[str] = []
    for h in page.headings:
        if not h.anchor or h.anchor in ids:
            continue
        known = [x for x in EXPECTED_ANCHORS if x[0] == section and x[1] == h.anchor and x[2] in ids]
        if known:
            notes.append(f"expected difference: anchor {h.anchor} is {known[0][2]} on the site ({known[0][3]})")
        else:
            problems.append(f"anchor {h.anchor} ('{h.text}') not on the built page")
    return problems, notes


def not_ingested(vault: Vault, site: Path, section: int, generated: set[str]) -> list[str]:
    """Site files of this section (tips by posts-dir, examples by directive category) without a brain page."""
    sec = vault.pages.get(f"section-{section}")
    if sec is None:
        return []
    missing: list[str] = []
    for f in sorted((site / "_posts" / str(sec.meta["posts-dir"])).glob("*.md")):
        if f.relative_to(site).as_posix() not in generated:
            missing.append(f.relative_to(site).as_posix())
    cats = {d.arg for d in sec.directives if d.name == "examples" and d.arg}
    for f in sorted((site / "_examples").glob("*.md")):
        rel = f.relative_to(site).as_posix()
        if rel not in generated and frontmatter.load(f).get("category") in cats:
            missing.append(rel)
    return missing


def keyword_page_changes(site: Path, p: Plan) -> tuple[set[str], set[str]]:
    """(lost, gained) tags of the /keywords/ page if `p`'s posts replaced the site's."""
    generated = {o.rel: o.text for o in p.outputs if o.rel.startswith("_posts/")}
    before: set[str] = set()
    after: set[str] = set()
    for f in sorted((site / "_posts").glob("*/*.md")):
        tags = set(split_tags(frontmatter.load(f).get("tags")))
        before |= tags
        if f.relative_to(site).as_posix() not in generated:
            after |= tags
    for text in generated.values():
        after |= set(split_tags(frontmatter.loads(text).get("tags")))
    return before - after, after - before


def check_section(vault: Vault, site: Path, section: int, out_dir: Path) -> SectionReport:
    site = Path(site)
    rep = SectionReport(section)
    if f"section-{section}" not in vault.pages:
        rep.notes.append(f"section-{section} is not in the brain")
        return rep
    p = plan(vault, statuses=PARITY_STATUSES, section=section)
    target = Path(out_dir) / f"section-{section}"
    if target.exists():
        shutil.rmtree(target)
    aliases = alias_table(vault)
    for o in p.outputs:
        dst = target / o.rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(o.text, encoding="utf-8")
        orig = site / o.rel
        if orig.exists():
            rep.files.append(compare_file(o.rel, orig.read_text(encoding="utf-8"), o.text, section, aliases))
        else:
            rep.files.append(FileReport(o.rel, notes=["new: no original on the site"]))
    problems, notes = anchor_check(vault, site, section)
    if problems:
        rep.files.append(FileReport(f"_site/section-{section}/index.html", ok=False, problems=problems))
    rep.notes += notes
    missing = not_ingested(vault, site, section, {o.rel for o in p.outputs})
    if missing:
        rep.notes.append(f"not ingested: {len(missing)} site files of this section have no brain page")
    lost, gained = keyword_page_changes(site, p)
    if lost:
        rep.notes.append(f"keyword page loses tags: {sorted(lost)}")
    if gained:
        rep.notes.append(f"keyword page gains tags: {sorted(gained)}")
    return rep


def format_report(rep: SectionReport) -> str:
    lines = [f"section {rep.section}: {'PASS' if rep.ok else 'FAIL'} ({len(rep.files)} files compared)"]
    for f in rep.files:
        if f.problems or f.notes:
            lines.append(f"  {'ok  ' if f.ok else 'FAIL'} {f.rel}")
            lines += [f"       ! {x}" for x in f.problems]
            lines += [f"       - {x}" for x in f.notes]
    lines += [f"  - {x}" for x in rep.notes]
    return "\n".join(lines)
