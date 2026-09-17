---
id: ISS-010
type: issue
title: Term pages cannot leave draft because the lint forbids legacy-tags on reviewed pages
status: open
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
resolved: null
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

**Resolution.** Open. The five terms of this ingest stay at `status: draft` so that nothing is
lost; option 1 is the ingest's recommendation and needs an ADR.
