# Log

Append-only. One entry per operation, prefix exact so it stays greppable:
`grep '^## \[' _system/log.md | tail -5`.

<!-- Format:
## [YYYY-MM-DD] <bootstrap|ingest|audit|report> | <subject>
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
