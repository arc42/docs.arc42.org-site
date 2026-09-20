---
id: ISS-014
type: issue
title: Section 2 has no example of organizational or political constraints
status: open
created: '2026-09-20'
updated: '2026-09-20'
sources:
- '[[SRC-002-section-2-page]]'
- '[[SRC-014-section-2-content]]'
related:
- '[[tip-2-3]]'
- '[[tip-2-5]]'
- '[[02-constraint-example-1]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Three of the five tips of section 2 are about constraints that are *not*
technical — organizational ones such as time, budget, process, contracting and legal concerns
([[tip-2-3]]), the category split itself ([[tip-2-5]]), and the negotiation of consequences with
stakeholders ([[tip-2-2]]). The section renders exactly one example, and every constraint in it is
technical. A reader looking for what a documented budget or process constraint is supposed to look
like finds nothing.

**Affects.** [[tip-2-3]], [[tip-2-5]], [[02-constraint-example-1]], [[section-2]].

**Evidence.** `%% examples: constraints %%` in `wiki/sections/section-2.md` resolves to a single
page, [[02-constraint-example-1]]; its four bullets are platform independence, Gradle
integration, command-line operation and an open-source licence. The licence bullet is arguably
legal rather than technical, but it is not labelled as a category. By comparison section 9 renders
three examples from three systems ([[09-decision-example-adr]], [[09-decision-example-htmlsc-1]],
[[09-decision-example-tpu-2]]).

**Options.**
1. Add a second constraints example from one of the other documented systems ([[tpu]], [[mama]],
   [[status]]) that shows organizational and political constraints, ideally as the table the
   section's *Form* asks for — which would also answer [[ISS-012-section-2-asks-for-tables-but-the-example-is-a-list|ISS-012]].
2. Extend the existing example with a second, categorized block.
3. Leave as is — one worked example per section is the site's norm outside section 9.

**Resolution.** Open. Needs the arc42 authors: writing a new example is authoring, not curation.
