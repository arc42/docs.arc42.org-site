---
id: view
type: term
title: View
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-016-section-4-content]]'
- '[[SRC-020-section-8-content]]'
related:
- '[[concept]]'
- '[[solution-strategy]]'
- '[[building-block]]'
term: View
aliases:
- Architecture view
- Architectural view
legacy-tags:
- view
home: '[[section-5]]'
---

**Definition.** A description of the architecture that shows the system from one perspective only,
leaving out everything that perspective does not need.

**In arc42.** Three sections are views, and each answers a different question about the same
system: section 5, the building block view, shows the static structure — what the system is made
of; section 6, the runtime view, shows behaviour — how those parts work together over time;
section 7, the deployment view, shows the technical infrastructure the parts run on. The view is
the unit of "look it up here": [[tip-4-4]] asks the solution strategy to refer to a view rather
than repeat it, so that a fact about structure has exactly one place it is written down.

**Distinguish from.** [[concept]] — a concept crosses the views, because it holds for many
building blocks at once; a view is a complete projection of the whole system onto one concern.
A view is also not a diagram: a diagram is one possible form for a view, which is why the
notation is a separate question ([[notation]]).
