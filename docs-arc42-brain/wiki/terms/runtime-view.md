---
id: runtime-view
type: term
title: Runtime view
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[view]]'
- '[[runtime-scenario]]'
- '[[deployment-view]]'
term: Runtime view
aliases:
- Runtime
legacy-tags:
- runtime-view
home: '[[section-6]]'
---

**Definition.** The view that shows behaviour over time — which building blocks interact, in what
order, to get something done.

**In arc42.** Section 6, which is not yet in the brain; this term exists because section 5 reaches
into it. [[tip-5-9]] offers the runtime view's own techniques — pseudo-code, activity diagrams,
flowcharts, state machines — as a way to say how a [[whitebox]] should behave without specifying
the parts it is made of, so behaviour becomes a constraint on a structure that is still open.

**Distinguish from.** [[view]] — the runtime view is one of the three, alongside the building
block view and the [[deployment-view]]. [[runtime-scenario]] — the view is the section; a
scenario is one concrete path through it.
