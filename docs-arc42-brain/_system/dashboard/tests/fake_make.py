"""A fake `make` for actions.py tests: records every invocation and emits
braingen-shaped output for `brain-lint`, `generate` and `generate-check`
without running real Docker/braingen."""
from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

_SCRIPT = '''#!__PYTHON__
import json
import os
import sys

with open("__RECORD__", "a", encoding="utf-8") as f:
    f.write(json.dumps(sys.argv[1:]) + "\\n")

target = sys.argv[3]

if target == "brain-lint":
    exit_code = int(os.environ.get("FAKE_LINT_EXIT", 0))
    if exit_code != 0:
        print("ERROR   x: boom")
    print("0 findings")
    sys.exit(exit_code)

if target == "generate":
    n = int(os.environ.get("FAKE_GEN_LINES", 1))
    for i in range(n):
        print("wrote   f" + str(i) + ".md")
    print("2 written, 1 deleted, 5 unchanged")
    sys.exit(int(os.environ.get("FAKE_GEN_EXIT", 0)))

if target == "generate-check":
    print("section 3: PASS (0 files compared)")
    print("section 9: FAIL (6 files compared)")
    sys.exit(1)

print("fake make: unknown target " + target, file=sys.stderr)
sys.exit(9)
'''


def install(tmp_path: Path, monkeypatch) -> Path:
    """Install a fake `make` on PATH; return the file it records calls to."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    record = tmp_path / "make-calls.jsonl"
    record.touch()

    script_path = bin_dir / "make"
    script_path.write_text(
        _SCRIPT.replace("__PYTHON__", sys.executable).replace("__RECORD__", str(record)),
        encoding="utf-8",
    )
    mode = script_path.stat().st_mode
    script_path.chmod(mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    monkeypatch.setenv("PATH", str(bin_dir) + os.pathsep + os.environ.get("PATH", ""))
    return record
