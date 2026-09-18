"""braingen command line: lint | raw | import | generate | generate-check | check-generated."""
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
    try:
        res = apply(vault, args.site, plan(vault))
    except FileExistsError as e:
        print(e)
        return 1
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

    vault = load_vault(args.vault)
    problems = check(vault, args.site, plan(vault))
    for x in problems:
        print(x)
    print(f"generated files: {len(problems)} problems")
    return 1 if problems else 0


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
