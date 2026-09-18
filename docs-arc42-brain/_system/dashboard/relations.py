"""Relations over the loaded vault: links in/out, issues naming a page,
`related:` suggestions, link and term graphs, search, and the obsidian://
deep link.

Reads the model only through `model.Brain` / braingen `Page` (D21); reuses
`model.issue_targets` rather than re-deriving it.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from urllib.parse import quote

from model import Brain, issue_targets

# Order also fixes the "via" for links_out when a target is reachable
# through more than one field (each (target, via) pair is still distinct).
LINK_KEYS = ("related", "section", "sources", "home", "system", "terms", "keywords", "ingested-pages")

# _system/workflows/relations.md
WEIGHTS = {"term": 3, "subsection": 2, "keyword": 1, "system": 2}

# Group order and labels for the detail page's "Links in"/"Links out"
# (brief: grouped by type, Sections first through Sources last).
GROUP_TYPES = ("section", "tip", "example", "term", "keyword", "system", "issue", "source")
GROUP_LABELS = {
    "section": "Sections", "tip": "Tips", "example": "Examples", "term": "Terms",
    "keyword": "Keywords", "system": "Systems", "issue": "Issues", "source": "Sources",
}


def _targets(page, key: str) -> set[str]:
    return {l.target for l in page.links_in(key)}


def links_out(b: Brain, slug: str) -> list[tuple[str, str]]:
    """(target_slug, via) for every wikilink out of `slug`; via is a
    LINK_KEYS field name or "body". Unique, in order of first appearance."""
    page = b.vault.pages[slug]
    seen: set[tuple[str, str]] = set()
    out: list[tuple[str, str]] = []
    for key in LINK_KEYS:
        for link in page.links_in(key):
            pair = (link.target, key)
            if pair not in seen:
                seen.add(pair)
                out.append(pair)
    for link in page.body_links:
        pair = (link.target, "body")
        if pair not in seen:
            seen.add(pair)
            out.append(pair)
    return out


def links_in(b: Brain, slug: str) -> list[tuple[str, str]]:
    """(source_slug, via) for every page that links to `slug`, sorted."""
    result = []
    for p in b.vault.pages.values():
        for target, via in links_out(b, p.slug):
            if target == slug:
                result.append((p.slug, via))
    return sorted(result)


def group_links(b: Brain, pairs: list[tuple[str, str]]) -> list[dict]:
    """`links_out`/`links_in` pairs -> one row per target, with every `via`
    merged ("via body, related"), grouped by the target page's type in
    GROUP_TYPES order (a group appears only if it has rows). A target whose
    type isn't in GROUP_TYPES (or that names no known page — a broken link)
    falls into a trailing "Other" group; `known` marks it for the template."""
    vias: dict[str, list[str]] = {}
    order: list[str] = []
    for target, via in pairs:
        if target not in vias:
            vias[target] = []
            order.append(target)
        if via not in vias[target]:
            vias[target].append(via)

    buckets: dict[str, list[dict]] = defaultdict(list)
    for target in order:
        page = b.vault.pages.get(target)
        ptype = page.type if page is not None and page.type in GROUP_TYPES else "other"
        title = str(page.meta.get("title") or target) if page is not None else target
        buckets[ptype].append({
            "slug": target, "title": title, "vias": ", ".join(vias[target]), "known": page is not None,
        })

    groups = []
    for ptype in GROUP_TYPES:
        if buckets.get(ptype):
            groups.append({"label": GROUP_LABELS[ptype], "rows": sorted(buckets[ptype], key=lambda r: r["slug"])})
    if buckets.get("other"):
        groups.append({"label": "Other", "rows": sorted(buckets["other"], key=lambda r: r["slug"])})
    return groups


def issues_naming(b: Brain, slug: str) -> list[str]:
    """Issue slugs whose related/body links name `slug`, sorted."""
    return sorted(
        i.slug for i in b.vault.by_type("issue")
        if slug in issue_targets(b, i)
    )


def _related_either_way(a, bp) -> bool:
    return bp.slug in _targets(a, "related") or a.slug in _targets(bp, "related")


def _pair_score(a, bp) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    shared_terms = sorted(_targets(a, "terms") & _targets(bp, "terms"))
    for t in shared_terms:
        score += WEIGHTS["term"]
        reasons.append(f"shared term {t} ({WEIGHTS['term']})")

    sa = a.links_in("section")
    sb = bp.links_in("section")
    if sa and sb and sa[0].heading and sa[0].heading == sb[0].heading and sa[0].target == sb[0].target:
        score += WEIGHTS["subsection"]
        reasons.append(f"same subsection {sa[0].heading} ({WEIGHTS['subsection']})")

    shared_keywords = sorted(_targets(a, "keywords") & _targets(bp, "keywords"))
    for k in shared_keywords:
        score += WEIGHTS["keyword"]
        reasons.append(f"shared keyword {k} ({WEIGHTS['keyword']})")

    if a.type == "example" and bp.type == "example":
        shared_systems = sorted(_targets(a, "system") & _targets(bp, "system"))
        if shared_systems:
            sys_slug = shared_systems[0]
            score += WEIGHTS["system"]
            reasons.append(f"same system {sys_slug} ({WEIGHTS['system']})")

    return score, reasons


def suggestions(b: Brain) -> dict[str, list[dict]]:
    """slug -> [{"target", "score", "reasons"}], score desc then target asc.

    Candidates are unordered pairs of non-retired tips and examples, minus
    pairs already related in either direction; score > 0 lists the pair
    under both pages.
    """
    candidates = sorted(
        (p for p in b.vault.by_type("tip") + b.vault.by_type("example") if p.status != "retired"),
        key=lambda p: p.slug,
    )
    result: dict[str, list[dict]] = defaultdict(list)
    for i, a in enumerate(candidates):
        for bp in candidates[i + 1:]:
            if _related_either_way(a, bp):
                continue
            score, reasons = _pair_score(a, bp)
            if score <= 0:
                continue
            result[a.slug].append({"target": bp.slug, "score": score, "reasons": reasons})
            result[bp.slug].append({"target": a.slug, "score": score, "reasons": reasons})
    for slug, items in result.items():
        items.sort(key=lambda x: (-x["score"], x["target"]))
    return dict(result)


def link_graph(b: Brain) -> dict:
    """Nodes: every page except type issue and source. Edges: `related`
    (kind "related") and `section` (kind "section") between those nodes,
    deduplicated as unordered pairs per kind."""
    nodes = sorted(
        (p for p in b.vault.pages.values() if p.type not in ("issue", "source")),
        key=lambda p: p.slug,
    )
    node_ids = {p.slug for p in nodes}
    out_nodes = [
        {"id": p.slug, "title": str(p.meta.get("title") or p.slug), "type": p.type, "status": p.status}
        for p in nodes
    ]
    edges = []
    seen: dict[str, set[frozenset]] = {"related": set(), "section": set()}
    for p in nodes:
        for key in ("related", "section"):
            for link in p.links_in(key):
                if link.target not in node_ids or link.target == p.slug:
                    continue
                pair = frozenset((p.slug, link.target))
                if pair in seen[key]:
                    continue
                seen[key].add(pair)
                edges.append({"source": p.slug, "target": link.target, "kind": key})
    return {"nodes": out_nodes, "edges": edges}


def term_graph(b: Brain) -> dict:
    """Nodes: terms. Edges: {"source", "target", "weight"} = the number of
    pages whose `terms:` carries both."""
    terms = sorted(b.vault.by_type("term"), key=lambda p: p.slug)
    nodes = [
        {"id": t.slug, "title": str(t.meta.get("title") or t.slug), "type": t.type, "status": t.status}
        for t in terms
    ]
    weights: Counter[frozenset] = Counter()
    for p in b.vault.pages.values():
        page_terms = sorted(_targets(p, "terms"))
        for i, ti in enumerate(page_terms):
            for tj in page_terms[i + 1:]:
                weights[frozenset((ti, tj))] += 1
    edges = []
    for pair, weight in weights.items():
        source, target = sorted(pair)
        edges.append({"source": source, "target": target, "weight": weight})
    edges.sort(key=lambda e: (e["source"], e["target"]))
    return {"nodes": nodes, "edges": edges}


def _snippet(title: str, body: str, ql: str, width: int = 160) -> str:
    collapsed = " ".join(f"{title}\n\n{body}".split())
    low = collapsed.lower()
    idx = low.find(ql)
    if idx == -1:
        return collapsed[:width]
    start = max(0, idx - width // 2)
    end = min(len(collapsed), start + width)
    start = max(0, end - width)
    return collapsed[start:end]


def search(b: Brain, q: str, limit: int = 50) -> list[dict]:
    """{"slug", "type", "title", "snippet"} for pages whose title or body
    contain `q`, case-insensitive; snippet is <=160 chars around the first
    match, newlines collapsed."""
    ql = q.lower()
    results = []
    for p in sorted(b.vault.pages.values(), key=lambda p: p.slug):
        title = str(p.meta.get("title") or p.slug)
        if ql not in title.lower() and ql not in p.body.lower():
            continue
        results.append({
            "slug": p.slug, "type": p.type, "title": title,
            "snippet": _snippet(title, p.body, ql),
        })
        if len(results) >= limit:
            break
    return results


def obsidian_url(b: Brain, page) -> str:
    """obsidian://open deep link for `page`, vault name `docs-arc42-brain`."""
    rel = b.vault.rel(page.path)
    if rel.endswith(".md"):
        rel = rel[:-3]
    return f"obsidian://open?vault=docs-arc42-brain&file={quote(rel, safe='')}"
