---
id: ISS-020
type: issue
title: Section 4 bodies carry editorial defects
status: open
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-016-section-4-content]]'
related:
- '[[tip-4-4]]'
- '[[04-solutionStrategy-example-mama-2]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Four defects survive in section 4's bodies, which the ingest keeps verbatim.
Three are typos; the fourth is an unclosed parenthesis inside a table cell, which is the only one
a reader can trip over.

**Affects.** [[tip-4-4]], [[04-solutionStrategy-example-mama-2]].

**Evidence.**

- [[tip-4-4]]: "such refered-documents" — one `r`, and the hyphen makes a compound of two words
  that are not one ("referred documents").
- [[tip-4-4]]: "you should document only briefly -" ends a line on a dangling hyphen where the
  sentence continues, so the rendered text reads "briefly - and refer (link) to".
- [[04-solutionStrategy-example-mama-2]]: "certain stragic approaches" — "strategic".
- [[04-solutionStrategy-example-mama-2]]: "create unique path/filename based upon cient-ID" —
  "client-ID"; and in the same table the first column of the second row opens a parenthesis it
  never closes: "Flexibility in Transmission Formats (CSV and fix-record-formats".

**Options.**
1. Fix them at cut-over, in the brain, as part of owning the content.
2. Fix them on the site now, before cut-over, and re-run `brain-raw` so the brain stays verbatim.
3. Leave them.

**Resolution.** Open, and deliberately the same shape as
[[ISS-013-section-2-tip-bodies-carry-editorial-defects|ISS-013]] and
[[ISS-015-section-1-tip-bodies-carry-editorial-defects|ISS-015]]: three sections now have one
typo issue each, none of them a cut-over blocker. Worth deciding once, for all sections, rather
than three times — the answer is probably option 1 plus a spell-check pass over the whole vault
after the last section is ingested.
