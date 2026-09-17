---
id: ISS-010
type: issue
title: Term pages cannot leave draft because the lint forbids legacy-tags on reviewed pages
status: resolved
created: '2026-09-17'
updated: '2026-09-17'
sources: []
related:
- '[[architecture-decision]]'
- '[[adr]]'
- '[[decision-criteria]]'
- '[[stakeholder]]'
- '[[quality-requirement]]'
severity: minor
kind: contradiction
raised-by: agent
resolved: '2026-09-17'
---

**What's unresolved.** On imported pages `legacy-tags` is a work item: it must be emptied by
mapping every tag to a keyword or a term before the page leaves `draft`, and the lint enforces
that for every type. On a *term* page `legacy-tags` is the opposite — it is the permanent mapping
("old site tags that mean this term") that the ingest of the next section needs in order to map
`decision`, `adr`, `criteria`, `stakeholder` and `quality` without re-deciding. The two readings of
the same field collide: a term that carries its mapping can never reach `status: review`.

**Affects.** [[architecture-decision]], [[adr]], [[decision-criteria]], [[stakeholder]],
[[quality-requirement]].

**Evidence.** `_templates/term.md`: `legacy-tags: []   # old site tags that mean this term, e.g.
[scenario, quality-scenario]`. `braingen/lint.py`, `_schema`: `if p.status in {"review",
"published"} and p.meta.get("legacy-tags"): error "legacy-tags still present"` — no exception for
`type: term`. `CLAUDE.md` lists `legacy-tags` as a defining field of the term type.

**Options.**
1. Exempt `type: term` (and `keyword`) from the rule, by ADR plus a test — keeps the mapping and
   lets terms be reviewed and published.
2. Move the mapping to a different field, e.g. `legacy-aliases` — no lint change, but a schema
   change and a new field to teach the importer.
3. Empty `legacy-tags` on terms after the mapping is applied — satisfies the lint today and loses
   the mapping for the next eleven sections.

**Resolution.** Resolved 2026-09-17 with option 1: lint rule L13 (`legacy-tags` non-empty while
`status` is `review` or `published`) no longer applies to `type: term`. On an imported page the field
is a transient work item that must be mapped away before the page leaves draft; on a term page it is
the permanent list of old tag spellings that map here (spec 4.2), and ADR-0003's "a page may not
leave draft until that list is empty" concerns the pages the importer parks tags on — tip, example,
faq. The exemption is covered by `test_term_may_keep_legacy_tags_in_review`. The five terms of the
section 9 ingest keep their mapping and are now `status: review`.
