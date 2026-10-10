import os
import subprocess
import threading
import time

import model as model_module
from model import (Model, contributors, examples_view, faq_view, gaps, ingest_state,
                   issues_touching_sections, issues_view, lint_view, list_rows, log_entries,
                   readiness, review_queue, section_numbers, sections_view, tags_view, tips_view)

from .kit import add_site_post, add_tip


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


def test_cache_reloads_on_generated_site_file_change(repo):
    """readiness()'s not_ingested check reads _pages/_posts/_examples (a
    `make generate` run from the host CLI touches those, not the vault),
    so stamp() must notice a change there too, not just under wiki/."""
    m = Model(repo)
    b1 = m.get(); assert m.get() is b1
    f = repo / "_pages" / "section-9.md"
    f.write_text("placeholder", encoding="utf-8")
    later = time.time() + 5
    os.utime(f, (later, later))
    assert m.get() is not b1


def test_sections_view(repo):
    v = sections_view(brain(repo), {"9": "PASS"})
    assert v["counts"] == {"draft": 1, "published": 1}
    rows = {r["number"]: r for r in v["rows"]}
    assert [r["number"] for r in v["rows"]] == [3, 9]
    assert (rows[9]["tips"], rows[9]["examples"], rows[9]["terms"], rows[9]["open_issues"]) == (3, 2, 1, 1)
    assert rows[9]["parity"] == "PASS" and rows[3]["parity"] is None
    assert rows[3]["open_issues"] == 1


def test_ingest_state_is_independent_of_the_section_pages_own_status(repo):
    """The distinction the Sections table's two columns exist for. The
    fixture starts with section 3 `draft` and empty, section 9 `published`
    with all three of its site posts ingested."""
    b = brain(repo)
    states = {int(s.meta["number"]): ingest_state(b, s) for s in b.vault.by_type("section")}
    assert states == {3: "not ingested", 9: "cut over"}

    # tip-3-1 covers the site's only section 3 post -> ingested, while the
    # section page itself stays `draft`.
    add_tip(repo, "3-1", "[[section-3]]", date="2016-01-01")
    b2 = Model(repo).get()
    sec3 = b2.vault.pages["section-3"]
    assert sec3.status == "draft" and ingest_state(b2, sec3) == "ingested"
    assert {r["number"]: r["ingest"] for r in sections_view(b2, {})["rows"]}[3] == "ingested"

    # One more site post with no brain page behind it -> partial.
    add_site_post(repo, "03-context", "2016-01-02-t-3-2.md")
    b3 = Model(repo).get()
    assert ingest_state(b3, b3.vault.pages["section-3"]) == "partial"


def test_issues_touching_sections_counts_distinct_issues_not_a_per_section_sum(repo):
    b = brain(repo)
    # Fixture: ISS-001 touches section 9 (via tip-9-1), ISS-003 touches
    # section 3 directly -- no overlap yet, so the distinct count and the
    # sum-over-sections agree; this alone wouldn't catch a double-count bug.
    assert issues_touching_sections(b) == 2

    # Make ISS-003 touch section 9 too (in addition to section 3): the
    # per-section sum would now be 3 (section 3: ISS-003, section 9:
    # ISS-001 + ISS-003), but the distinct count of open issues stays 2.
    p = repo / "docs-arc42-brain/wiki/issues/ISS-003.md"
    p.write_text(p.read_text().replace("- '[[section-3]]'", "- '[[section-3]]'\n- '[[tip-9-1]]'"),
                 encoding="utf-8")
    b2 = Model(repo).get()
    assert sum(r["open_issues"] for r in sections_view(b2, {})["rows"]) == 3
    assert issues_touching_sections(b2) == 2


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


def test_get_is_thread_safe(repo, monkeypatch):
    """Concurrent get() calls with an unchanged stamp must load the vault
    exactly once (gthread runs several requests in parallel)."""
    calls = []
    orig_load_vault = model_module.load_vault

    def counting_load_vault(root):
        calls.append(1)
        time.sleep(0.05)
        return orig_load_vault(root)

    monkeypatch.setattr(model_module, "load_vault", counting_load_vault)

    m = Model(repo)
    results = []

    def worker():
        results.append(m.get())

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(calls) == 1
    assert all(r is results[0] for r in results)


def test_list_rows_unfiltered(repo):
    b = brain(repo)
    rows = list_rows(b, "tip")
    assert [r["slug"] for r in rows] == ["tip-9-1", "tip-9-2", "tip-9-3"]
    assert rows[0] == {
        "slug": "tip-9-1", "title": "Tip 9-1: Do it!", "status": "published",
        "section": 9, "system": None, "updated": "2026-09-18",
    }
    assert rows[2]["updated"] == "2026-09-05"


def test_list_rows_filters_by_status_and_section(repo):
    b = brain(repo)
    assert [r["slug"] for r in list_rows(b, "tip", status="draft")] == ["tip-9-2"]
    assert [r["slug"] for r in list_rows(b, "tip", sections={9})] == ["tip-9-1", "tip-9-2", "tip-9-3"]
    assert list_rows(b, "tip", sections={3}) == []


def test_list_rows_several_sections_are_or_ed_and_empty_means_no_filter(repo):
    b = brain(repo)
    everything = [r["slug"] for r in list_rows(b, "tip")]
    assert [r["slug"] for r in list_rows(b, "tip", sections={3, 9})] == everything
    assert [r["slug"] for r in list_rows(b, "tip", sections=set())] == everything


def test_section_numbers_come_from_the_section_pages(repo):
    assert section_numbers(brain(repo)) == [3, 9]


def _commit(repo, name, email, date, msg):
    env = {**os.environ, "GIT_AUTHOR_NAME": name, "GIT_AUTHOR_EMAIL": email,
           "GIT_COMMITTER_NAME": name, "GIT_COMMITTER_EMAIL": email,
           "GIT_AUTHOR_DATE": f"{date}T12:00:00", "GIT_COMMITTER_DATE": f"{date}T12:00:00"}
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "--allow-empty", "-m", msg],
                   env=env, check=True)


def test_contributors_fold_identities_via_mailmap(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".mailmap").write_text("Real Name <real@example.org> <old@example.org>\n")
    _commit(tmp_path, "Real Name", "real@example.org", "2026-01-01", "one")
    _commit(tmp_path, "host@laptop", "old@example.org", "2026-02-01", "two")
    _commit(tmp_path, "host@laptop", "old@example.org", "2026-03-01", "three")
    _commit(tmp_path, "Other Person", "other@example.org", "2026-02-15", "four")
    _commit(tmp_path, "dependabot[bot]", "1+dependabot[bot]@users.noreply.github.com", "2026-04-01", "bump")
    assert contributors(tmp_path) == [
        {"name": "Real Name", "email": "real@example.org", "commits": 3,
         "first": "2026-01-01", "last": "2026-03-01", "aliases": ["host@laptop"], "bot": False},
        {"name": "Other Person", "email": "other@example.org", "commits": 1,
         "first": "2026-02-15", "last": "2026-02-15", "aliases": [], "bot": False},
        {"name": "dependabot[bot]", "email": "1+dependabot[bot]@users.noreply.github.com",
         "commits": 1, "first": "2026-04-01", "last": "2026-04-01", "aliases": [], "bot": True},
    ]


def test_contributors_is_empty_outside_a_git_repo(tmp_path):
    assert contributors(tmp_path) == []


def test_list_rows_system_name_and_filter(repo):
    b = brain(repo)
    rows = {r["slug"]: r for r in list_rows(b, "example")}
    assert rows["09-decision-example-x"]["system"] == "HTML Sanity Checker"
    assert rows["09-decision-example-y"]["system"] is None
    filtered = list_rows(b, "example", system="htmlsc")
    assert [r["slug"] for r in filtered] == ["09-decision-example-x"]


def test_gaps(repo):
    g = gaps(brain(repo))
    assert g["tips_without_example"] == ["tip-9-2", "tip-9-3"]
    assert g["examples_without_tip"] == ["09-decision-example-y"]
    assert g["unlinked_subsections"] == [("section-3", "Business Context")]
    assert g["sections_without_related"] == ["section-3", "section-9"]
