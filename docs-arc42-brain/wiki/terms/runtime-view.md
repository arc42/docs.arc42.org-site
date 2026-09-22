---
id: runtime-view
type: term
title: Runtime view
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
- '[[SRC-024-section-6-content]]'
related:
- '[[view]]'
- '[[runtime-scenario]]'
- '[[deployment-view]]'
- '[[activity-diagram]]'
- '[[sequence-diagram]]'
term: Runtime view
aliases:
- Runtime
legacy-tags:
- runtime-view
- runtime
home: '[[section-6]]'
---

**Definition.** The view that shows behaviour over time — which building blocks interact, in what
order, to get something done.

**In arc42.** Section 6, and the shortest of the three view sections: eleven tips, of which nine
are about restraint. The section page asks for scenarios chosen by *architectural relevancy*, and
the tips spend their advice on how few to keep ([[tip-6-2]]: one to three in the documentation,
dozens during design), how coarse to draw them ([[tip-6-3]]), how much of one to show
([[tip-6-6]]) and how to mix sizes of participant to avoid drawing the rest ([[tip-6-10]]). Only
[[tip-6-4]] argues the other way, and hedges. Section 5 reaches into the view from outside:
[[tip-5-9]] offers its techniques — pseudo-code, activity diagrams, flowcharts, state machines —
as a way to say how a [[whitebox]] should behave without specifying the parts it is made of, so
behaviour becomes a constraint on a structure that is still open.

**On the tag.** The site spells this two ways. The eleven tips are tagged `runtime-view`; the
three examples are tagged `runtime`, the same short form the example category uses. The
unhyphenated spelling folds here and reaches zero at section 6's cut-over, exactly as
`deployment` folds into [[deployment-view]] and `buildingblock` into [[building-block]] — three
sections, one habit.

**Distinguish from.** [[view]] — the runtime view is one of the three, alongside the building
block view and the [[deployment-view]]. [[runtime-scenario]] — the view is the section; a
scenario is one concrete path through it. [[sequence-diagram]] and [[activity-diagram]] — the two
notations the section tags; the view is what is described, not how.
