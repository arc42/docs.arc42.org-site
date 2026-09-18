"""Generate the Jekyll content files from the vault, idempotently.

`make generate` owns exactly the files that carry the marker line (see
emit_body.MARKER_PREFIX) plus the assets listed in the asset manifest; everything
else in the site is never written or deleted.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .emit import Output, emit_example, emit_section, emit_tip, section_of, tags_for
from .emit_body import is_generated
from .parse import Page, Vault

OWNED_GLOBS = ["_pages/section-*.md", "_posts/*/*.md", "_examples/*.md"]
ASSET_MANIFEST = "_system/generated-assets.txt"   # vault-relative
ASSET_TARGETS = {"sections": "assets/images/sections", "examples": "assets/images/examples"}


@dataclass(frozen=True)
class AssetOutput:
    rel: str      # site-relative destination, e.g. "assets/images/sections/10/q42.svg"
    src: Path     # absolute source under wiki/assets/


@dataclass
class Plan:
    outputs: list[Output] = field(default_factory=list)
    assets: list[AssetOutput] = field(default_factory=list)


@dataclass
class Result:
    written: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)


def _selected(page: Page, statuses: set[str], section: int | None, vault: Vault) -> bool:
    if page.status not in statuses:
        return False
    if section is None:
        return True
    sec = page if page.type == "section" else section_of(vault, page)
    return int(sec.meta["number"]) == section


def plan(vault: Vault, statuses: set[str] = frozenset({"published"}), section: int | None = None) -> Plan:
    """Everything one run writes. `statuses`/`section` exist for the parity check."""
    sections = [p for p in vault.by_type("section") if _selected(p, statuses, section, vault)]
    tips = [p for p in vault.by_type("tip") if _selected(p, statuses, section, vault)]
    examples = [p for p in vault.by_type("example") if _selected(p, statuses, section, vault)]
    emitted = {p.slug for p in tips + examples}
    site_tags = {t for p in tips for t in tags_for(vault, p)}
    out = Plan()
    out.outputs += [emit_section(vault, p) for p in sections]
    out.outputs += [emit_tip(vault, p, emitted, site_tags) for p in tips]
    out.outputs += [emit_example(vault, p, emitted, site_tags) for p in examples]
    out.outputs.sort(key=lambda o: o.rel)
    out.assets = _assets(vault, sections + tips + examples)
    return out


def _assets(vault: Vault, pages: list[Page]) -> list[AssetOutput]:
    seen: dict[str, AssetOutput] = {}
    for p in pages:
        for img in p.images:
            src = (p.path.parent / img).resolve()
            try:
                rel = src.relative_to((vault.root / "wiki/assets").resolve())
            except ValueError:
                continue
            kind, rest = rel.parts[0], Path(*rel.parts[1:])
            if kind in ASSET_TARGETS:
                dst = f"{ASSET_TARGETS[kind]}/{rest.as_posix()}"
                seen[dst] = AssetOutput(dst, src)
    return [seen[k] for k in sorted(seen)]


def owned_files(site: Path) -> list[str]:
    """Site-relative paths of every content file that carries the marker."""
    found: list[str] = []
    for pattern in OWNED_GLOBS:
        for f in sorted(site.glob(pattern)):
            if is_generated(f.read_text(encoding="utf-8")):
                found.append(f.relative_to(site).as_posix())
    return found


def read_asset_manifest(vault: Vault) -> list[str]:
    f = vault.root / ASSET_MANIFEST
    if not f.exists():
        return []
    return [l.strip() for l in f.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]


def write_asset_manifest(vault: Vault, rels: list[str]) -> None:
    header = "# assets written by `make generate`; it deletes these, and only these, when stale\n"
    f = vault.root / ASSET_MANIFEST
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(header + "".join(f"{r}\n" for r in sorted(rels)), encoding="utf-8")


def conflicts(vault: Vault, site: Path, p: Plan) -> list[str]:
    """Hand-made files a run would overwrite. `apply` writes nothing while any exist."""
    site = Path(site)
    found: list[str] = []
    for o in p.outputs:
        f = site / o.rel
        if f.exists():
            current = f.read_text(encoding="utf-8")
            if current != o.text and not is_generated(current):
                found.append(f"{o.rel}: hand-written file; delete the original first (cut-over)")
    owned_assets = set(read_asset_manifest(vault))
    for a in p.assets:
        f = site / a.rel
        if f.exists() and a.rel not in owned_assets and f.read_bytes() != a.src.read_bytes():
            found.append(f"{a.rel}: hand-made asset with different content")
    return found


def apply(vault: Vault, site: Path, p: Plan) -> Result:
    """Write `p` into `site` and delete the stale files it owns. Idempotent."""
    site = Path(site)
    found = conflicts(vault, site, p)
    if found:
        raise FileExistsError("refusing to overwrite:\n  " + "\n  ".join(found))
    res = Result()
    for o in p.outputs:
        f = site / o.rel
        if f.exists() and f.read_text(encoding="utf-8") == o.text:
            res.unchanged.append(o.rel)
            continue
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(o.text, encoding="utf-8")
        res.written.append(o.rel)
    targets = {o.rel for o in p.outputs}
    for rel in owned_files(site):
        if rel not in targets:
            (site / rel).unlink()
            res.deleted.append(rel)

    old_assets = set(read_asset_manifest(vault))
    new_assets = {a.rel for a in p.assets}
    for a in p.assets:
        f = site / a.rel
        data = a.src.read_bytes()
        if f.exists() and f.read_bytes() == data:
            res.unchanged.append(a.rel)
            continue
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(data)
        res.written.append(a.rel)
    for rel in sorted(old_assets - new_assets):
        f = site / rel
        if f.exists():
            f.unlink()
            res.deleted.append(rel)
    if old_assets != new_assets:
        write_asset_manifest(vault, sorted(new_assets))
    return res


def check(vault: Vault, site: Path, p: Plan) -> list[str]:
    """Problems that make the committed generated files differ from a fresh generate."""
    site = Path(site)
    problems: list[str] = []
    targets = {o.rel: o for o in p.outputs}
    for o in p.outputs:
        f = site / o.rel
        if not f.exists():
            problems.append(f"{o.rel}: missing, run make generate")
        elif f.read_text(encoding="utf-8") != o.text:
            current = f.read_text(encoding="utf-8")
            what = "hand-edited or stale" if is_generated(current) else "hand-written file where a generated one belongs"
            problems.append(f"{o.rel}: {what}, run make generate (edit {o.source} instead)")
    for rel in owned_files(site):
        if rel not in targets:
            problems.append(f"{rel}: generated file without a published brain page, run make generate")
    listed = set(read_asset_manifest(vault))
    for a in p.assets:
        f = site / a.rel
        if not f.exists() or f.read_bytes() != a.src.read_bytes():
            problems.append(f"{a.rel}: differs from {a.src.name} in wiki/assets, run make generate")
        elif a.rel not in listed:
            problems.append(f"{a.rel}: not in {ASSET_MANIFEST}, run make generate")
    return problems
