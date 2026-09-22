---
id: view
type: term
title: View
status: review
created: '2026-09-21'
updated: '2026-09-22'
sources:
- '[[SRC-016-section-4-content]]'
- '[[SRC-020-section-8-content]]'
- '[[SRC-021-section-7-content]]'
- '[[SRC-023-section-5-content]]'
related:
- '[[concept]]'
- '[[solution-strategy]]'
- '[[building-block]]'
- '[[deployment-view]]'
- '[[whitebox]]'
- '[[runtime-view]]'
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
notation is a separate question ([[notation]]). [[deployment-view]] is one of the three, with a
term of its own because the site tags it separately.

**Note on the tag.** The bare tag `view` sits on exactly one page, [[tip-4-4]], which is the tip
that talks about views in general. The site names the specific ones instead —
`deployment-view` on section 7, `runtime-view` on section 6 — and section 5 uses none of the
three, tagging its tips [[building-block]] rather than "building block view". So this term is the
umbrella that one page needs, not a tag that spans the view sections.
