"""Published URLs must not silently disappear (docs.arc42.org is cited from outside).

`make generate` records every permalink it publishes in REGISTRY, append-only.
Before it writes anything, and in `check-generated`, every recorded URL must
still be planned, or be listed in RETIRED with a reason. Unpublishing a page or
changing its permalink therefore stops generate instead of turning a cited URL
into a 404. The site has no redirect plugin, so retiring a URL is a deliberate,
recorded decision, not a side effect.
"""
from __future__ import annotations

from .generate import Plan
from .parse import Vault

REGISTRY = "_system/published-permalinks.txt"   # vault-relative
RETIRED = "_system/retired-permalinks.txt"      # vault-relative

REGISTRY_HEADER = (
    "# Every URL `make generate` has published: permalink<TAB>page id. Append-only, written by generate.\n"
    f"# To take a URL off the site on purpose, list it in {RETIRED.split('/')[-1]} with a reason.\n"
)


def _rows(vault: Vault, rel: str) -> list[tuple[str, str]]:
    f = vault.root / rel
    if not f.exists():
        return []
    rows = []
    for line in f.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        url, _, rest = line.partition("\t")
        rows.append((url.strip(), rest.strip()))
    return rows


def read_registry(vault: Vault) -> dict[str, str]:
    """permalink -> id of the page that published it."""
    return dict(_rows(vault, REGISTRY))


def read_retired(vault: Vault) -> dict[str, str]:
    """permalink -> reason ("" when the line has none)."""
    return dict(_rows(vault, RETIRED))


def check(vault: Vault, p: Plan) -> list[str]:
    """Recorded URLs that `p` would no longer serve and nobody retired."""
    planned = {o.permalink for o in p.outputs}
    retired = read_retired(vault)
    problems = [f"{url}: listed in {RETIRED} with no reason" for url, why in sorted(retired.items()) if not why]
    for url, page_id in sorted(read_registry(vault).items()):
        if url in planned or retired.get(url):
            continue
        problems.append(f"{url} (was {page_id}) would no longer be served; keep the page published and the "
                        f"permalink unchanged, or list the URL in {RETIRED} with a reason")
    return problems


def record(vault: Vault, p: Plan) -> int:
    """Add the permalinks of `p` to the registry. Returns how many were new."""
    known = read_registry(vault)
    new = {o.permalink: o.page_id for o in p.outputs if o.permalink and o.permalink not in known}
    if not new:
        return 0
    rows = {**known, **new}
    f = vault.root / REGISTRY
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(REGISTRY_HEADER + "".join(f"{url}\t{pid}\n" for url, pid in sorted(rows.items())), encoding="utf-8")
    return len(new)
