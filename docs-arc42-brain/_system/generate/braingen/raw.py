"""Copy one arc42 section's current site files into a raw/ batch for ingest.

A batch is a folder raw/section-<N>-<what>/ with a manifest.yaml. Nothing in
the site is modified; the batch is the immutable provenance the importer
reads. `what` is "page" (the section page only), "content" (its tips and
examples) or "all".
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

import frontmatter
import yaml

WHAT = ("all", "page", "content")
EXAMPLE_INCLUDE_RE = re.compile(r'{%\s*include example\.md\s+category="([^"]+)"\s*%}')
SECTION_IMAGE_RE = re.compile(r"(?:\{\{\s*site\.imageurl\s*\}\}|/assets/images/sections)/([^)\s\"']+)")
EXAMPLE_IMAGE_RE = re.compile(r"(?:\{\{\s*site\.exampleimages\s*\}\}|/assets/images/examples)/([^)\s\"']+)")


def _section_meta(site: Path, section: int) -> dict:
    entries = yaml.safe_load((site / "_data" / "sections.yml").read_text(encoding="utf-8"))
    for e in entries:
        if int(e["number"]) == section:
            return e
    raise ValueError(f"section {section} not in _data/sections.yml")


def _posts_dir(site: Path, section: int) -> str:
    prefix = f"{section:02d}-"
    for d in sorted((site / "_posts").iterdir()):
        if d.is_dir() and d.name.startswith(prefix):
            return d.name
    raise ValueError(f"no _posts/{prefix}* directory for section {section}")


def _copy(src: Path, dst: Path, files: list[str], batch: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    files.append(str(dst.relative_to(batch)))


def make_raw(site: Path, vault: Path, section: int, what: str = "all") -> Path:
    if what not in WHAT:
        raise ValueError(f"what must be one of {WHAT}, got {what!r}")
    site, vault = Path(site), Path(vault)
    meta = _section_meta(site, section)
    batch = vault / "raw" / f"section-{section}-{what}"
    if batch.exists():
        raise FileExistsError(f"{batch} exists; archive it under raw/ingested/ or remove it first")

    page_path = site / "_pages" / f"section-{section}.md"
    page = frontmatter.load(page_path)
    example_categories = EXAMPLE_INCLUDE_RE.findall(page.content)
    files: list[str] = []
    texts: list[str] = []

    if what in ("all", "page"):
        _copy(page_path, batch / "pages" / page_path.name, files, batch)
        texts.append(page_path.read_text(encoding="utf-8"))

    posts_dir = _posts_dir(site, section)
    if what in ("all", "content"):
        for p in sorted((site / "_posts" / posts_dir).glob("*.md")):
            _copy(p, batch / "posts" / p.name, files, batch)
            texts.append(p.read_text(encoding="utf-8"))
        for e in sorted((site / "_examples").glob("*.md")):
            cat = frontmatter.load(e).get("category")
            if cat in example_categories:
                _copy(e, batch / "examples" / e.name, files, batch)
                texts.append(e.read_text(encoding="utf-8"))

    joined = "\n".join(texts)
    for rel in sorted(set(SECTION_IMAGE_RE.findall(joined))):
        _copy(site / "assets/images/sections" / rel, batch / "assets/sections" / rel, files, batch)
    for rel in sorted(set(EXAMPLE_IMAGE_RE.findall(joined))):
        _copy(site / "assets/images/examples" / rel, batch / "assets/examples" / rel, files, batch)

    manifest = {
        "section": section,
        "what": what,
        "name": meta["name"],
        "category": meta["category"],
        "permalink": meta["permalink"],
        "posts_dir": posts_dir,
        "order": page.get("order"),
        "title": page.get("title"),
        "example_categories": example_categories,
        "files": files,
    }
    batch.mkdir(parents=True, exist_ok=True)
    (batch / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return batch
