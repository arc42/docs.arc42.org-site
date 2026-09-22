---
id: ISS-029
type: issue
title: Section 7 bodies carry editorial defects
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-021-section-7-content]]'
related:
- '[[tip-7-8]]'
- '[[tip-7-9]]'
- '[[tip-7-10]]'
- '[[07-deployment-example-tpu-1]]'
- '[[07-deployment-sample-tpu-2]]'
- '[[ISS-044-one-editorial-pass-owns-the-decision-ten-issues-ask-for]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Eight defects, including one word that is now misspelled the same way in
two different sections and one unclosed parenthesis.

**Affects.** [[tip-7-8]], [[tip-7-9]], [[tip-7-10]], [[07-deployment-example-tpu-1]],
[[07-deployment-sample-tpu-2]].

**Evidence.**

- [[tip-7-10]]: "only such information … that's neccessary" — the same misspelling as
  [[tip-8-3]]'s "absolutely relevant or neccessary", recorded in
  [[ISS-027-section-8-bodies-carry-editorial-defects|ISS-027]]. Two sections, one typo.
- [[tip-7-9]]: "propably" for "probably", and "you should instead _thorougly_ document" for
  "thoroughly".
- [[tip-7-8]]: "explain those nodes, what there properties are" — "their".
- [[07-deployment-example-tpu-1]]: "is the central processoror of the TPU".
- [[07-deployment-sample-tpu-2]]: "the refinement of one processors"; "The video cards consists of
  two PCBs"; and a parenthesis that never closes — "(UserInserter Node and LegalInserter Node, cf.
  figure 7.5 and the other one contains the Codec."

**Options.**
1. Fix them at cut-over, in the brain, as part of owning the content.
2. Fix them on the site now, before cut-over, and re-run `brain-raw` so the brain stays verbatim.
3. Leave them.

**Resolution.** Open, the seventh section with a typo issue of its own. The `neccessary` pair is
the second case of a defect that spans sections — after `ubiqitous` vs `ubiquitous` — and neither
would be found by reading one section at a time, which is the argument for one pass over the whole
vault once section 5 is in.

**The decision this issue asks for lives in [[ISS-044-one-editorial-pass-owns-the-decision-ten-issues-ask-for|ISS-044]]** (2026-09-22). Ten per-section issues each asked the same question — correct in the brain, or stay byte-faithful until cut-over? — and none of them owned the answer. This one keeps its own defect list, which is what the eventual pass works from.
