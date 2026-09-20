---
id: ISS-012
type: issue
title: Section 2 asks for tables of constraints while its only example is a plain bullet list
status: open
created: '2026-09-20'
updated: '2026-09-20'
sources:
- '[[SRC-002-section-2-page]]'
- '[[SRC-014-section-2-content]]'
related:
- '[[section-2]]'
- '[[02-constraint-example-1]]'
severity: minor
kind: contradiction
raised-by: agent
resolved: null
---

**What's unresolved.** The *Form* guidance of section 2 names one form, a table. The single
example that the section renders opens by recommending the opposite, a plain enumeration. A reader
who follows the guidance and a reader who copies the example produce different documents, and
neither page acknowledges the other form.

**Affects.** [[02-constraint-example-1]], [[section-2]].

**Evidence.** `wiki/sections/section-2.md`, *Form*: "Simple tables of constraints with
explanations. If needed you can subdivide them into technical constraints, organizational and
political constraints and conventions". `wiki/examples/02-constraint-example-1.md`, first line of
the body: "Key constraints can often be explained as simple enumeration in plain text.", followed
by a four-item bullet list. Compare [[tip-9-4]], where the alternative forms of a decision (table,
mind map) are offered explicitly as a tip.

**Options.**
1. Widen the *Form* guidance to "tables or a plain list, whichever carries the explanations" — one
   sentence, makes the example an illustration of the guidance instead of an exception.
2. Add a tip 2-6 in the shape of [[tip-9-4]] ("choose the form that fits the number of
   constraints") and leave both pages as they are.
3. Leave as is — the example's own sentence already reads as the exception, and arc42 guidance is
   deliberately not prescriptive.

**Resolution.** Open. This is content, not tooling: it needs the arc42 authors' word, since
changing *Form* changes the template text itself.
