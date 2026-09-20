# Log

Append-only. One entry per operation, prefix exact so it stays greppable:
`grep '^## \[' _system/log.md | tail -5`.

<!-- Format:
## [YYYY-MM-DD] <bootstrap|ingest|audit|report|cutover|generate> | <subject>
- created: …
- updated: …
- issues: …
-->

## [2026-09-17] bootstrap | twelve section pages, keywords, systems
- created: section-1 … section-12 (draft, from raw/ingested/section-N-page), SRC-001 … SRC-012
- created: keywords lean, essential, thorough, example, tooling; systems htmlsc, tpu, mama, status
- notes: section 10 image path normalised from a hard-coded /assets/images path; all other bodies verbatim

## [2026-09-17] ingest | section 9 content
- created: tip-9-1 … tip-9-10 and the 3 decision examples (09-decision-example-adr, -htmlsc-1, -tpu-2), all `review`; terms architecture-decision, adr, decision-criteria, stakeholder, quality-requirement (all `draft`, see ISS-010); SRC-013-section-9-content
- updated: section-9 (`related: [[section-4]]`, the guidance itself says "Refer to section 4"); _system/index.md
- vocabulary: `decision` → term architecture-decision (all 13 pages); `adr` → term adr (9-5, 9-8, 9-9, 9-10, ADR example); `criteria` → term decision-criteria (9-2, 9-3, 9-5, 9-6, HtmlSC example); `stakeholder` → term stakeholder (9-1, 9-2, 9-4); `quality` → term quality-requirement (9-1, 9-4, doubt in ISS-001); `lean` (9-1, 9-7), `essential` (9-2, 9-3), `thorough` (9-6), `tooling` (9-10), `example` (3 examples) → existing keywords. All `legacy-tags` now empty on the thirteen imported pages; the term pages keep theirs as the permanent mapping (ISS-010). Tips 9-4, 9-5, 9-8 and 9-9 carry no keyword because the legacy post had no facet tag — nothing was invented.
- links: 70 related links (tips 44, examples 9, terms 17), plus 5 subsection links; 28 `terms:` references and 9 `keywords:` references across the 13 imported pages
- deviations from the brief's proposal, with reasons:
  - subsection links live in `section:`, not in `related:` — `_system/workflows/relations.md` forbids relating a page to its own section, and the tip template documents `section:` as the field that may carry a heading. Affected: 9-1 → `[[section-9#Our proposal concerning decisions]]`; 9-5, 9-8, 9-9, 9-10 → `[[section-9#Background (on ADRs)]]`.
  - examples did not get `related: [[section-9]]` for the same reason; they link the tips they demonstrate instead.
  - added beyond the proposal: 9-1 ↔ 9-7 (9-1 says document only the significant decisions, 9-7 says where the rest may go), 9-2 ↔ 9-5 (9-5's body links tip 9-2), 9-3 ↔ 9-6 (both are about the *why*), 9-4 ↔ 9-5 ("You could describe this ADR format as tables"), 9-2/9-6 ↔ HtmlSC example (it is the only page showing "Decision Criteria" and "Alternatives" per decision), 9-3 ↔ TPU example (free-form decisions with their reasons), 9-8/9-10 ↔ ADR example (it carries the timestamp of tip 9-8 and comes from the adr-tools of tip 9-10).
  - terms cite the source their definition comes from in addition to SRC-013: architecture-decision and adr also SRC-009, stakeholder also SRC-001, quality-requirement also SRC-010. The brief proposed SRC-013 alone, but the definitions of those four are taken from section pages that belong to other batches.
  - issue ids start at ISS-001 (the vault had no issues), not at ISS-013 as the template line suggested.
- issues: ISS-001 ambiguity — `quality` on tips 9-1/9-4 may mean the quality of the documentation, not the arc42 quality requirement; ISS-002 contradiction — section 9's Nygard table has neither the timestamp tip 9-8 demands nor the criteria tip 9-5 misses; ISS-003 risk — the Pugh matrix link of tip 9-2 redirects to an unrelated site (psychobegone.com); ISS-004 risk — thinkrelevance.com, joelparkerhenderson/… and wikipedia.org links answer only through redirects, and Nygard's article is cited under two domains within one section; ISS-005 gap — tip 9-2's second table uses `=` as separator row and does not render, plus "to"/"two"; ISS-006 gap — tips 9-3 and 9-5 reference tip 9-2 as `/tips/9-2` instead of a wikilink; ISS-007 gap — eight pages carry raw HTML anchors, `<br>` and an empty `<p></p>`; ISS-008 question — tip 9-8 duplicates one bullet of the quotation in tip 9-9; ISS-009 gap — the ADR example starts at H1, the other two at H2; ISS-010 contradiction — a term page cannot reach `review` while it carries the `legacy-tags` mapping the term type is supposed to hold.
- external links checked 2026-09-17 with `curl -sI`: 12 distinct URLs, 7 × 200 (cognitect.com, adr.github.io, adr.github.io/#tooling, npryce/adr-tools, npryce/adr-tools/tree/master/doc/adr, jsoup.org, rrice/java-string-similarity), 5 × 301 (thinkrelevance.com, decision-making-confidence.com, joelparkerhenderson/… twice, wikipedia.org → ISS-003, ISS-004). No 404, but the 301 of tip 9-2 lands on unrelated content.
- lint: 0 errors, 33 warnings. Every warning is "related [[x]] is not reciprocated" on an ISS page, and every one is deliberate: an issue's `related` records the pages it affects, and content pages must not link back — issues are not "see also" material for readers, and the back-links would push several tips past the limit of 8 related targets (relations.md). The tip/example/term graph itself is fully reciprocated and produces no warning.
- notes for the next ingest: (1) do not put subsection links into `related`; (2) `decision`, `adr`, `criteria`, `stakeholder` and `quality` are mapped — reuse the term pages instead of re-deciding; (3) expect the same raw-HTML anchors (ISS-007) and hard-coded `/tips/N-M` references (ISS-006) in every section, so ISS-006 and ISS-007 should be decided once, not per section; (4) near-duplicate that was left alone on purpose: section 9's Nygard table and the quotation in tip 9-5 say the same thing in guidance and in tip form, which is the intended division of labour (recorded as evidence in ISS-002); (5) `make brain-raw` and `make brain-import` handled this batch without a single hand-patch — no tooling bug found.
- update 2026-09-17: ISS-010 resolved by exempting terms from lint L13; the five terms are now review

## [2026-09-18] cutover | section 9
- published: section-9, tip-9-1 … tip-9-10, 09-decision-example-adr, -htmlsc-1, -tpu-2 (14 pages)
- generated: _pages/section-9.md, _posts/09-decisions/ (10), _examples/09-decision-example-* (3); hand-written originals deleted first, generated files now at the same paths
- parity: make generate-check PASS before (SECTION=9) and after (12 sections checked, 0 failed)
- tags: decision → architecture-decision (13 pages), criteria → decision-criteria (9-2), quality → quality-requirement (9-1, 9-4); adr added where the brain maps terms the legacy tags lacked (09-decision-example-adr, 9-5), decision-criteria likewise (09-decision-example-htmlsc-1, 9-3, 9-5, 9-6); keyword page gains architecture-decision, decision-criteria, quality-requirement, loses nothing
- site: related-links block on the 13 tips/examples; make check and make check-links green
- fix: marker moved into the front matter (YAML comment) — the body marker had replaced every generated page's meta description; section 9 regenerated

## [2026-09-18] report | dashboard (phase 3a)
- verified: `make dashboard-test` (97 passed), `make dashboard` in Docker against this repo — `/`, `/sections`, `/cutover`, `/lint`, `/graph.json` all 200; `/ping` as a fresh client shows `is_facilitator: true`; `/actions/preview` → 202, job polled to completion, `summary.sections` 12/12 PASS; `/actions/generate` → 202, job polled to completion, `exit_code: 0`, `summary.changed: 0` (section 9 already generated); `git status --short` showed exactly one change, this file's test-run line, reverted with `git checkout --`; `make brain-test` (120 passed), `make brain-lint` (0 errors, 33 warnings, unchanged baseline), `make brain-check-generated` (0 problems) all green afterwards
- docs: `docs-arc42-brain/README.md` and `CLAUDE.md` gain the dashboard commands; `_system/dashboard/README.md` created (run/test/architecture); dashboard spec status → implemented (phase 3a), with a Deviations section (module split beyond §6, `BRAINGEN` override instead of uv in the container, log line only after a successful generate, `braingen.lint.Finding.rule`, subprocess timeouts, detail-page grouped links, nav "More" menu)
- open item: port 4211 still needs registering in `../meta.arc42.org/raw/port-assignment.md` (separate repo, not touched here)

## [2026-09-19] report | permalink guard
- added: `braingen.permalinks` — `_system/published-permalinks.txt` (append-only, written by `make generate`) and `_system/retired-permalinks.txt` (URLs taken off on purpose, each with a reason); `make generate` stops before writing anything and `make brain-check-generated` / `make check` fail when a recorded URL is no longer planned; lint rule `permalink` flags two pages with the same URL
- bootstrapped: 14 URLs of section 9 recorded by `make generate` (0 files written)
- verified: setting tip-9-4 to draft (reverted) → `generate stopped: 1 published URLs would disappear`; `make brain-test` 129 passed, dashboard tests 123 passed, lint 0 errors, check-generated 0 problems

## [2026-09-20] ingest | section 2 content
- created: tip-2-1 … tip-2-5 and 02-constraint-example-1, all `review`; term constraint (`review`); SRC-014-section-2-content
- updated: terms stakeholder, quality-requirement, architecture-decision (each gains `related: [[constraint]]`); issues ISS-006 and ISS-007 widened from "section 9" to every section and given the section 2 evidence; _system/index.md
- vocabulary: `constraint` (all five tips) and `constraints` (the example) → new term constraint, whose `legacy-tags` now carries both spellings; `stakeholder` (2-2) → existing term stakeholder; `essential` (2-5) → existing keyword essential; `example` (the example) → existing keyword example. All `legacy-tags` empty on the six imported pages. Tips 2-1 … 2-4 carry no keyword because the legacy posts had no facet tag — nothing was invented.
- links: 16 related links (tips 12, example 4), 7 `terms:` and 2 `keywords:` references; `system: [[htmlsc]]` on the example. No subsection links: section 2's only headings are `Content`, `Motivation` and `Form`, which the schema forbids as link targets, and its H1 is the page itself.
- link rationale: 2-1 ↔ 2-3 (constraints found in other systems of the organization are the organizational ones), 2-2 ↔ 2-3 (both end in a negotiation with management/stakeholders), 2-3 ↔ 2-4 and 2-4 ↔ 2-5 (the bodies reference each other by hard-coded URL, see ISS-006), 2-3 ↔ 2-5 (2-5 names the categories 2-3 and 2-4 document), example ↔ 2-4 and ↔ 2-5 (its four bullets are technical constraints, unlabelled by category)
- parity: `make generate-check SECTION=2` PASS, 7 files compared; the one intended difference is the example's site tag `constraints` → `constraint` (term mapping), exactly the pattern of the section 9 cut-over
- issues: ISS-012 contradiction — section 2's *Form* asks for tables while its only example opens by recommending a plain enumeration; ISS-013 gap — "contraints"/"managements" in tip 2-4, "organisational" next to "organizational" inside single pages, and a stray leading space in tip 2-2, all live on the site since 2016 (deciding it sets the rule for the remaining sections: does an ingest fix typos, or does the brain stay byte-faithful until cut-over?); ISS-014 gap — three of five tips are about non-technical constraints and no example shows one
- ISS-007 gained a finding the section 9 ingest could not see: `<div class="arc42-example">` in the section 2 example carries authored text and the class that styles it, so "strip all raw HTML" is not a possible resolution — a normaliser needs one rule per construct
- lint: 0 errors, 43 warnings (baseline 33 + 10). Every new warning is an ISS page's `related` not being reciprocated, deliberate for the same reason as before; the tip/example/term graph produces none
- notes for the next ingest: (1) the term constraint's `legacy-tags` holds both `constraint` and `constraints` — reuse it; (2) a section page whose only headings are `Content`/`Motivation`/`Form` offers no subsection anchors, so tips link it bare; (3) `make brain-raw`/`make brain-import` again needed no hand-patch; (4) section 2 is ingested but **not** cut over — its six pages are `review`, the site still serves the hand-written originals
