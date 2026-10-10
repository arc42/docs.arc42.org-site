"""Query-string helpers for the list pages' filters.

Pure functions of the request args, so the section toggles' links can be
tested without Flask: every chip is a plain link to the current filter with
its own section switched on or off (no JS, bookmarkable, back button works).
"""
from __future__ import annotations

from urllib.parse import urlencode


def sections_arg(values: list[str]) -> set[int]:
    """The `section` query values as ints; anything not a number is dropped,
    matching "missing is no filter"."""
    out = set()
    for v in values:
        try:
            out.add(int(v))
        except ValueError:
            pass
    return out


def filter_href(path: str, status: str, system: str, sections: set[int]) -> str:
    params = [("status", status)] if status else []
    if system:
        params.append(("system", system))
    params += [("section", str(n)) for n in sorted(sections)]
    return path + ("?" + urlencode(params) if params else "")


def section_chips(path: str, numbers: list[int], selected: set[int],
                  status: str = "", system: str = "") -> list[dict]:
    """[{label, on, href}]: "All" (on when nothing is selected, clears the
    selection), then one chip per section whose href toggles it."""
    chips = [{"label": "All", "on": not selected, "href": filter_href(path, status, system, set())}]
    for n in numbers:
        chips.append({"label": str(n), "on": n in selected,
                      "href": filter_href(path, status, system, selected ^ {n})})
    return chips
