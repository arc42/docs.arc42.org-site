from dataclasses import dataclass, field

from model import Model
from relations import (group_links, issues_naming, link_graph, links_in, links_out, obsidian_url,
                       search, suggestions, term_graph)


def b(repo):
    return Model(repo).get()


def test_links_out_and_in(repo):
    br = b(repo)
    out = links_out(br, "tip-9-1")
    for pair in [("09-decision-example-x", "related"), ("section-9", "section"), ("adr", "terms"),
                 ("lean", "keywords"), ("SRC-001-test", "sources"), ("tip-9-2", "body")]:
        assert pair in out
    assert links_in(br, "tip-9-1") == [("09-decision-example-x", "related"), ("ISS-001", "related")]
    assert issues_naming(br, "tip-9-1") == ["ISS-001"]


def test_suggestions(repo):
    s = suggestions(b(repo))
    first = s["tip-9-1"][0]
    assert first["score"] == 3 and first["reasons"] == ["shared term adr (3)"]
    assert {x["target"] for x in s["tip-9-1"]} == {"tip-9-2", "tip-9-3"}
    assert s["tip-9-3"][0]["target"] in {"tip-9-1", "tip-9-2"}
    assert "09-decision-example-x" not in {x["target"] for x in s.get("tip-9-1", [])}


def test_graphs(repo):
    br = b(repo)
    g = link_graph(br)
    ids = {n["id"] for n in g["nodes"]}
    assert "tip-9-1" in ids and "ISS-001" not in ids and "SRC-001-test" not in ids
    rel = [e for e in g["edges"] if e["kind"] == "related"
           and {e["source"], e["target"]} == {"tip-9-1", "09-decision-example-x"}]
    assert len(rel) == 1
    t = term_graph(br)
    assert {n["id"] for n in t["nodes"]} == {"adr", "stakeholder"}
    assert t["edges"] == [{"source": "adr", "target": "stakeholder", "weight": 1}]


@dataclass
class _FPage:
    slug: str
    type: str
    meta: dict = field(default_factory=dict)


@dataclass
class _FVault:
    pages: dict


@dataclass
class _FBrain:
    vault: _FVault


def test_group_links_merges_vias_and_groups_by_type():
    pages = {
        "section-9": _FPage("section-9", "section", {"title": "Architecture Decisions"}),
        "tip-9-2": _FPage("tip-9-2", "tip", {}),
        "adr": _FPage("adr", "term", {"title": "ADR"}),
    }
    b = _FBrain(_FVault(pages))
    pairs = [("section-9", "related"), ("section-9", "section"), ("tip-9-2", "body"),
             ("adr", "terms"), ("missing-page", "related")]
    groups = group_links(b, pairs)
    assert [g["label"] for g in groups] == ["Sections", "Tips", "Terms", "Other"]
    assert groups[0]["rows"] == [
        {"slug": "section-9", "title": "Architecture Decisions", "vias": "related, section", "known": True}
    ]
    assert groups[1]["rows"] == [{"slug": "tip-9-2", "title": "tip-9-2", "vias": "body", "known": True}]
    assert groups[-1]["rows"] == [
        {"slug": "missing-page", "title": "missing-page", "vias": "related", "known": False}
    ]


def test_group_links_on_real_vault(repo):
    groups = {g["label"]: {r["slug"]: r for r in g["rows"]} for g in group_links(b(repo), links_out(b(repo), "tip-9-1"))}
    assert set(groups["Sections"]) == {"section-9"}
    assert set(groups["Examples"]) == {"09-decision-example-x"}
    assert set(groups["Sources"]) == {"SRC-001-test"}
    assert groups["Sections"]["section-9"]["title"] == "9 - Architecture Decisions"


def test_search_and_obsidian(repo):
    br = b(repo)
    assert [r["slug"] for r in search(br, "ADR.GITHUB")] == ["tip-9-1"]
    assert obsidian_url(br, br.vault.pages["tip-9-1"]) == \
        "obsidian://open?vault=docs-arc42-brain&file=wiki%2Ftips%2Ftip-9-1"
