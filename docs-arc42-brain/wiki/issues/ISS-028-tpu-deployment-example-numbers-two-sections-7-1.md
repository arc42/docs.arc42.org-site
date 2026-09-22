---
id: ISS-028
type: issue
title: The TPU deployment example has two sections numbered 7.1
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-021-section-7-content]]'
related:
- '[[07-deployment-example-tpu-1]]'
- '[[07-deployment-sample-tpu-2]]'
severity: minor
kind: contradiction
raised-by: agent
resolved: null
---

**What's unresolved.** [[07-deployment-example-tpu-1]] carries two H2 headings, seven lines apart,
both numbered 7.1: `## 7.1 Deployment View Level 1 (Traffic Pursuit Unit)` and
`## 7.1 Deployment Level 1`. The first introduces the rack photo, the second opens the list of
three nodes. A reader meets the same section number twice on one page, and the sibling example
[[07-deployment-sample-tpu-2]] then continues at 7.2, so the numbering is shared across pages and
visibly wrong on this one.

**Affects.** [[07-deployment-example-tpu-1]].

**Evidence.** Lines 27 and 34 of the body. The page's remaining headings are `### 1.
MeasuringUnit Node`, `### 2. PC-Board` and `### 3. Video Cards`, which are numbered on a different
scheme again — 1, 2, 3 rather than 7.1.1 and so on.

**Options.**
1. Renumber the second heading to 7.1.1, or drop its number and leave the text. The three node
   headings would then read naturally as its children.
2. Delete the second heading and let the node list follow the first.
3. Leave it.

**Resolution.** Open. Distinct from
[[ISS-009-examples-start-at-different-heading-levels|ISS-009]] (which level an example *starts*
at) and [[ISS-023-tpu-risk-example-uses-bold-text-as-headings|ISS-023]] (a page with no headings
at all): this is a page whose headings contradict each other. Three issues now describe the
heading structure of the examples, all three found in TPU or HtmlSC pages, which suggests one
pass over all 26 examples rather than three separate fixes.
