"""Convert a raw/ batch (see raw.py) into draft wiki pages plus a source record.

Mechanical only: frontmatter mapping, callouts, directives, image paths. The
judgement work (mapping legacy tags to keywords/terms, related links, issues)
is the ingest session's, see _system/workflows/ingest.md.
"""
from __future__ import annotations

import hashlib
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import frontmatter
import yaml

HELP_OPEN = '<div class="arc42-help"'
HELP_CLOSE = "</div>"
EXAMPLE_INCLUDE_RE = re.compile(r'^\s*{%\s*include example\.md\s+category="([^"]+)"\s*%}\s*$')
EXAMPLES_LINK_RE = re.compile(r'^\s*{%\s*include examples-link\.html\s+variant="inline"\s*%}\s*$')
FURTHER_INFO_START = "{% include further-info.md"
TOPIC_RE = re.compile(r'topic="([^"]*)"')
TIP_FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-t-(\d+)-(\d+)\.md$")
SYSTEM_TOKENS = {"htmlsc": "htmlsc", "hsc": "htmlsc", "tpu": "tpu", "mama": "mama", "status": "status"}

IMAGE_REWRITES = [
    (re.compile(r"\{\{\s*site\.imageurl\s*\}\}/"), "../assets/sections/"),
    (re.compile(r"/assets/images/sections/"), "../assets/sections/"),
    (re.compile(r"\{\{\s*site\.exampleimages\s*\}\}/"), "../assets/examples/"),
    (re.compile(r"/assets/images/examples/"), "../assets/examples/"),
]


def rewrite_images(text: str) -> str:
    for rx, repl in IMAGE_REWRITES:
        text = rx.sub(repl, text)
    return text


def _common(id_: str, type_: str, title: str, today: str, source_slug: str) -> dict:
    return {
        "id": id_,
        "type": type_,
        "title": title,
        "status": "draft",
        "created": today,
        "updated": today,
        "sources": [f"[[{source_slug}]]"],
        "related": [],
    }


def _split_tags(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [t for t in value.replace(",", " ").split() if t]
    return [str(t).strip() for t in value if str(t).strip()]


def convert_section(text: str, manifest: dict, today: str, source_slug: str) -> tuple[dict, str]:
    post = frontmatter.loads(text)
    out: list[str] = []
    in_help = False
    faq_topic = ""
    lines = post.content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith(HELP_OPEN):
            in_help = True
            out.append("> [!arc42-help]")
            i += 1
            continue
        if in_help and stripped == HELP_CLOSE:
            in_help = False
            i += 1
            continue
        if stripped.startswith(FURTHER_INFO_START):
            block = line
            while "%}" not in block and i + 1 < len(lines):
                i += 1
                block += "\n" + lines[i]
            m = TOPIC_RE.search(block)
            faq_topic = m.group(1) if m else ""
            i += 1
            continue
        m = EXAMPLE_INCLUDE_RE.match(line)
        if m:
            line = f"%% examples: {m.group(1)} %%"
        elif EXAMPLES_LINK_RE.match(line):
            line = "%% examples-link %%"
        line = rewrite_images(line)
        if in_help:
            line = f"> {line}" if line.strip() else ">"
        out.append(line)
        i += 1
    body = "\n".join(out).rstrip("\n") + "\n"
    n = int(manifest["section"])
    meta = _common(f"section-{n}", "section", str(post.get("title", manifest.get("title"))), today, source_slug)
    meta.update({
        "number": n,
        "name": manifest["name"],
        "category": manifest["category"],
        "posts-dir": manifest["posts_dir"],
        "permalink": manifest["permalink"],
        "order": manifest.get("order"),
        "faq-topic": faq_topic,
    })
    return meta, body


def convert_tip(filename: str, text: str, manifest: dict, today: str, source_slug: str) -> tuple[dict, str]:
    m = TIP_FILENAME_RE.match(filename)
    if not m:
        raise ValueError(f"tip filename {filename!r} does not match YYYY-MM-DD-t-N-M.md")
    date, n, k = m.group(1), m.group(2), m.group(3)
    post = frontmatter.loads(text)
    meta = _common(f"{n}-{k}", "tip", str(post.get("title", "")), today, source_slug)
    meta.update({
        "section": f"[[section-{int(manifest['section'])}]]",
        "keywords": [],
        "terms": [],
        "legacy-tags": _split_tags(post.get("tags")),
        "date": date,
        "permalink": str(post.get("permalink", f"/tips/{n}-{k}/")),
    })
    return meta, rewrite_images(post.content).rstrip("\n") + "\n"


def _system_for(stem: str) -> str:
    for token in stem.split("-"):
        if token in SYSTEM_TOKENS:
            return f"[[{SYSTEM_TOKENS[token]}]]"
    return ""


def convert_example(filename: str, text: str, manifest: dict, today: str, source_slug: str) -> tuple[dict, str]:
    stem = filename[:-3] if filename.endswith(".md") else filename
    post = frontmatter.loads(text)
    meta = _common(stem, "example", str(post.get("title", "")), today, source_slug)
    meta.update({
        "section": f"[[section-{int(manifest['section'])}]]",
        "system": _system_for(stem),
        "example-category": str(post.get("category", "")),
        "keywords": [],
        "terms": [],
        "legacy-tags": _split_tags(post.get("tags")),
        "permalink": str(post.get("permalink", "")),
    })
    return meta, rewrite_images(post.content).rstrip("\n") + "\n"


def write_page(path: Path, meta: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fm = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, default_flow_style=False)
    path.write_text(f"---\n{fm}---\n\n{body}", encoding="utf-8")


def next_source_id(vault: Path) -> int:
    best = 0
    for p in (Path(vault) / "raw" / "sources").glob("SRC-*.md"):
        m = re.match(r"SRC-(\d+)", p.name)
        if m:
            best = max(best, int(m.group(1)))
    return best + 1


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class ImportReport:
    source_slug: str
    written: list[Path] = field(default_factory=list)


def import_batch(vault: Path, batch_name: str, today: str) -> ImportReport:
    vault = Path(vault)
    batch = vault / "raw" / batch_name
    manifest = yaml.safe_load((batch / "manifest.yaml").read_text(encoding="utf-8"))
    source_slug = f"SRC-{next_source_id(vault):03d}-{batch_name}"
    report = ImportReport(source_slug)

    planned: list[tuple[Path, dict, str]] = []
    page_file = batch / "pages" / f"section-{manifest['section']}.md"
    if page_file.exists():
        meta, body = convert_section(page_file.read_text(encoding="utf-8"), manifest, today, source_slug)
        planned.append((vault / "wiki/sections" / f"{meta['id']}.md", meta, body))
    for p in sorted((batch / "posts").glob("*.md")) if (batch / "posts").is_dir() else []:
        meta, body = convert_tip(p.name, p.read_text(encoding="utf-8"), manifest, today, source_slug)
        planned.append((vault / "wiki/tips" / f"tip-{meta['id']}.md", meta, body))
    for p in sorted((batch / "examples").glob("*.md")) if (batch / "examples").is_dir() else []:
        meta, body = convert_example(p.name, p.read_text(encoding="utf-8"), manifest, today, source_slug)
        planned.append((vault / "wiki/examples" / f"{meta['id']}.md", meta, body))

    for path, _, _ in planned:
        if path.exists():
            raise FileExistsError(f"{path.relative_to(vault)} already exists; the vault owns it now")

    for path, meta, body in planned:
        write_page(path, meta, body)
        report.written.append(path)

    assets = batch / "assets"
    if assets.is_dir():
        for src in sorted(assets.rglob("*")):
            if src.is_file():
                dst = vault / "wiki/assets" / src.relative_to(assets)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

    files = [
        {"path": rel, "sha256": _sha256(batch / rel)}
        for rel in manifest.get("files", [])
        if (batch / rel).is_file()
    ]
    src_meta = {
        "id": source_slug.split("-section-")[0] if "-section-" in source_slug else source_slug[:7],
        "type": "source",
        "title": f"Site files of section {manifest['section']} ({manifest['what']})",
        "status": "ingested",
        "created": today,
        "updated": today,
        "source-type": "repository",
        "origin": f"raw/{batch_name}/",
        "captured": today,
        "files": files,
        "ingested-pages": [f"[[{p.stem}]]" for p in report.written],
    }
    src_path = vault / "raw/sources" / f"{source_slug}.md"
    write_page(src_path, src_meta, f"Copied from docs.arc42.org-site on {today} by `braingen raw`; converted by `braingen import`.\n")
    report.written.append(src_path)
    return report
