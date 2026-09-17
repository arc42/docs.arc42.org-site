"""braingen command line: lint | raw | import."""
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
    return ap


def main(argv: list[str] | None = None) -> int:
    ap = build_parser()
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
