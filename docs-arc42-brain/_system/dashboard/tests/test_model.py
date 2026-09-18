import os
import time

from model import (Model, examples_view, faq_view, gaps, issues_view, lint_view, log_entries,
                   readiness, review_queue, sections_view, tags_view, tips_view)


def brain(repo):
    return Model(repo).get()


def test_cache_reloads_on_change(repo):
    m = Model(repo)
    b1 = m.get(); assert m.get() is b1
    f = repo / "docs-arc42-brain/wiki/tips/tip-9-3.md"
    later = time.time() + 5
    os.utime(f, (later, later))
    assert m.get() is not b1
    m.clear(); assert m.get() is not None


def test_sections_view(repo):
    v = sections_view(brain(repo), {"9": "PASS"})
    assert v["counts"] == {"draft": 1, "published": 1}
    rows = {r["number"]: r for r in v["rows"]}
    assert [r["number"] for r in v["rows"]] == [3, 9]
    assert (rows[9]["tips"], rows[9]["examples"], rows[9]["terms"], rows[9]["open_issues"]) == (3, 2, 1, 1)
    assert rows[9]["parity"] == "PASS" and rows[3]["parity"] is None
    assert rows[3]["open_issues"] == 1


def test_tips_examples_faq(repo):
    b = brain(repo)
    t = tips_view(b)
    assert t["counts"] == {"draft": 1, "review": 1, "published": 1}
    assert t["without_related"] == ["tip-9-2", "tip-9-3"] and t["legacy"] == ["tip-9-2"]
    e = examples_view(b)
    assert e["by_system"] == {"(none)": 1, "HTML Sanity Checker": 1}
    assert e["orphan_categories"] == ["orphans"]
    f = faq_view(b)
    assert f["count"] == 0 and "136" in f["note"]


def test_tags_view(repo):
    v = tags_view(brain(repo))
    assert v["terms"] == [("adr", 3), ("stakeholder", 1)]
    assert v["keywords"] == [("lean", 1)]
    assert v["incomplete_terms"] == ["stakeholder"]
    assert v["legacy"] == [("ADRs", "adr")]


def test_issues_and_lint(repo):
    b = brain(repo)
    i = issues_view(b)
    assert [p.slug for p in i["open"]] == ["ISS-001", "ISS-003"]
    assert i["by_severity"] == {"major": 1, "minor": 1} and i["by_kind"] == {"gap": 1, "risk": 1}
    l = lint_view(b)
    assert list(l["errors"]) == ["example-category"] and len(l["warnings"]["reciprocity"]) == 2


def test_log_entries_newest_first(repo):
    e = log_entries(brain(repo))
    assert [x["subject"] for x in e] == ["six", "five", "four", "three", "two"]
    assert e[0] == {"date": "2026-09-15", "kind": "generate", "subject": "six"}


def test_review_queue(repo):
    q = review_queue(brain(repo))
    assert [p.slug for p in q["pages"]] == ["adr", "tip-9-3"]
    assert [label for label, _ in q["checklist"]] == ["Read", "Vocabulary", "Links", "Issues", "Status"]


def test_readiness(repo):
    r = readiness(brain(repo), {"9": "PASS", "3": "PASS"})
    rows = {x["number"]: x for x in r["rows"]}
    assert rows[9]["cut_over"] is True and rows[9]["ingested"] is True
    assert rows[9]["lint_clean"] is False and rows[9]["related"] is False
    assert rows[3]["ingested"] is False and rows[3]["lint_clean"] is True and rows[3]["related"] is True
    assert r["next"] is None


def test_readiness_next_when_ready(repo):
    (repo / "_posts/03-context/2016-01-01-t-3-1.md").unlink()
    r = readiness(brain(repo), {"3": "PASS"})
    assert r["next"] == 3


def test_gaps(repo):
    g = gaps(brain(repo))
    assert g["tips_without_example"] == ["tip-9-2", "tip-9-3"]
    assert g["examples_without_tip"] == ["09-decision-example-y"]
    assert g["unlinked_subsections"] == [("section-3", "Business Context")]
    assert g["sections_without_related"] == ["section-3", "section-9"]
