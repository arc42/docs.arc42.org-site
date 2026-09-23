"""braingen command line: lint | raw | import | generate | generate-check | check-generated | approve-edit | pending-edits."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .lint import lint
from .parse import load_vault


def cmd_lint(args: argparse.Namespace) -> int:
    findings = lint(load_vault(args.vault))
    for x in findings:
        print(x)
    errors = sum(1 for x in findings if x.level == "error")
    print(f"{len(findings)} findings, {errors} errors, {len(findings) - errors} warnings")
    return 1 if errors else 0


def cmd_raw(args: argparse.Namespace) -> int:
    from .raw import make_raw

    batch = make_raw(args.site, args.vault, args.section, args.what)
    print(f"raw batch written: {batch}")
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    from datetime import date

    from .importer import import_batch

    report = import_batch(args.vault, args.batch, args.today or date.today().isoformat())
    for p in report.written:
        print(f"wrote {p.relative_to(args.vault)}")
    print(f"source record: {report.source_slug}")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    from .generate import apply, plan

    vault = load_vault(args.vault)
    errors = [x for x in lint(vault) if x.level == "error"]
    if errors:
        for x in errors:
            print(x)
        print(f"generate stopped: {len(errors)} lint errors")
        return 1
    from .permalinks import check as check_permalinks, record

    p = plan(vault)
    lost = check_permalinks(vault, p)
    if lost:
        for x in lost:
            print(x)
        print(f"generate stopped: {len(lost)} published URLs would disappear")
        return 1
    try:
        res = apply(vault, args.site, p)
    except FileExistsError as e:
        print(e)
        return 1
    new = record(vault, p)
    if new:
        print(f"recorded {new} new permalinks in _system/published-permalinks.txt")
    for rel in res.written:
        print(f"wrote   {rel}")
    for rel in res.deleted:
        print(f"deleted {rel}")
    print(f"{len(res.written)} written, {len(res.deleted)} deleted, {len(res.unchanged)} unchanged")
    return 0


def cmd_generate_check(args: argparse.Namespace) -> int:
    from .parity import check_section, format_report

    vault = load_vault(args.vault)
    if args.section is not None:
        sections = [args.section]
    else:
        sections = sorted(int(p.meta["number"]) for p in vault.by_type("section"))
    failed = 0
    for n in sections:
        rep = check_section(vault, args.site, n, args.out)
        print(format_report(rep))
        failed += 0 if rep.ok else 1
    print(f"{len(sections)} sections checked, {failed} failed; generated files under {args.out}")
    return 1 if failed else 0


def cmd_check_generated(args: argparse.Namespace) -> int:
    from .generate import check, plan
    from .permalinks import check as check_permalinks

    vault = load_vault(args.vault)
    p = plan(vault)
    problems = check(vault, args.site, p) + check_permalinks(vault, p)
    for x in problems:
        print(x)
    print(f"generated files: {len(problems)} problems")
    return 1 if problems else 0


def cmd_approve_edit(args: argparse.Namespace) -> int:
    """Show what an edit does to a published body, and record it only on --yes.

    Corrections to published text are the point of the brain owning the
    content, but the raw-parity guard cannot tell a correction from an emitter
    regression. So a correction is approved by a human who has seen the diff,
    and the approval covers exactly the body it was shown (ADR-0006).
    """
    from datetime import date

    from .approvals import Approval, append, body_diff, original_from_raw
    from .generate import plan
    from .parity import PARITY_STATUSES

    vault = load_vault(args.vault)
    outputs = {}
    for page in vault.by_type("section"):
        n = int(page.meta["number"])
        for o in plan(vault, statuses=PARITY_STATUSES, section=n).outputs:
            outputs[o.rel] = (o.text, n)
    if args.rel not in outputs:
        print(f"{args.rel}: not a file this vault generates")
        return 1
    original = original_from_raw(args.vault, args.rel)
    if original is None:
        print(f"{args.rel}: no hand-written original in raw/ingested/ — nothing to approve against")
        return 1

    text, section = outputs[args.rel]
    diff, fp = body_diff(original, text, section)
    if not diff:
        print(f"{args.rel}: body is unchanged from the original — no approval needed")
        return 0
    print(diff)
    print(f"\n{args.rel}\nfingerprint {fp}\nissue {args.issue}\nreason {args.reason}")
    if not args.yes:
        print("\nnot recorded — this is the preview. Re-run the same command with --yes "
              "(make: YES=1) to approve exactly this body.")
        return 0
    path = append(args.vault, Approval(args.rel, fp, args.issue, args.today or date.today().isoformat(),
                                       args.reason))
    print(f"\nrecorded in {path.relative_to(args.vault)}")
    return 0


def cmd_pending_edits(args: argparse.Namespace) -> int:
    """List published bodies that differ from the copy captured at ingest.

    The queue the dashboard shows and `approve-edit` works through: each entry
    is one page whose text the brain has changed, with the diff and whether it
    has already been approved (ADR-0006).
    """
    import json

    from .approvals import pending
    from .generate import plan
    from .parity import PARITY_STATUSES

    vault = load_vault(args.vault)
    outputs = {}
    for page in vault.by_type("section"):
        n = int(page.meta["number"])
        for o in plan(vault, statuses=PARITY_STATUSES, section=n).outputs:
            outputs[o.rel] = (o.text, n)
    items = pending(args.vault, outputs)
    if args.json:
        print(json.dumps([p.as_dict() for p in items], indent=2))
        return 0
    for p in items:
        state = (f"approved {p.approved.issue} {p.approved.date}: {p.approved.reason}"
                 if p.approved else "NOT APPROVED")
        print(f"{p.rel}  [{state}]")
    print(f"{len(items)} changed bodies, {sum(1 for p in items if not p.approved)} not approved")
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="braingen", description="docs-arc42-brain tooling")
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("lint", help="validate the vault")
    l.add_argument("vault", type=Path)
    l.set_defaults(func=cmd_lint)
    r = sub.add_parser("raw", help="copy a section's site files into a raw/ batch")
    r.add_argument("--site", type=Path, required=True)
    r.add_argument("--vault", type=Path, required=True)
    r.add_argument("--section", type=int, required=True)
    r.add_argument("--what", choices=["all", "page", "content"], default="all")
    r.set_defaults(func=cmd_raw)
    i = sub.add_parser("import", help="convert a raw batch into draft wiki pages")
    i.add_argument("--vault", type=Path, required=True)
    i.add_argument("--batch", required=True, help="batch folder name under raw/, e.g. section-9-all")
    i.add_argument("--today", default=None, help="override the date written into created/updated")
    i.set_defaults(func=cmd_import)
    g = sub.add_parser("generate", help="write the Jekyll files of every published page")
    g.add_argument("--vault", type=Path, required=True)
    g.add_argument("--site", type=Path, required=True)
    g.set_defaults(func=cmd_generate)
    pc = sub.add_parser("generate-check", help="parity check: generate into --out and compare with the site")
    pc.add_argument("--vault", type=Path, required=True)
    pc.add_argument("--site", type=Path, required=True)
    pc.add_argument("--section", type=int, default=None, help="one section; default: every section in the brain")
    pc.add_argument("--out", type=Path, required=True, help="scratch folder, e.g. docs-arc42-brain/build/parity")
    pc.set_defaults(func=cmd_generate_check)
    ae = sub.add_parser("approve-edit", help="show an edit to a published body and record it on --yes")
    ae.add_argument("--vault", type=Path, required=True)
    ae.add_argument("--rel", required=True, help="site path, e.g. _pages/section-9.md")
    ae.add_argument("--issue", required=True, help="the issue that decided it, e.g. ISS-002")
    ae.add_argument("--reason", required=True, help="one line, what the edit does and why")
    ae.add_argument("--today", default=None)
    ae.add_argument("--yes", action="store_true", help="record it; without this the diff is only shown")
    ae.set_defaults(func=cmd_approve_edit)
    pe = sub.add_parser("pending-edits", help="list published bodies that differ from the ingested original")
    pe.add_argument("--vault", type=Path, required=True)
    pe.add_argument("--json", action="store_true")
    pe.set_defaults(func=cmd_pending_edits)
    cg = sub.add_parser("check-generated", help="fail if a generated file differs from a fresh generate")
    cg.add_argument("--vault", type=Path, required=True)
    cg.add_argument("--site", type=Path, required=True)
    cg.set_defaults(func=cmd_check_generated)
    return ap


def main(argv: list[str] | None = None) -> int:
    ap = build_parser()
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
