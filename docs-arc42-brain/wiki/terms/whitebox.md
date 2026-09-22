---
id: whitebox
type: term
title: Whitebox
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[blackbox]]'
- '[[building-block]]'
- '[[view]]'
term: Whitebox
aliases:
- White box
- White-box
legacy-tags:
- whitebox
home: '[[section-5]]'
---

**Definition.** One building block opened up: the blackboxes it decomposes into, the
relationships between them, and the reason it was cut that way.

**In arc42.** The unit of the building block view — [[tip-5-2]] describes the whole view as a
tree of whiteboxes, each rounded rectangle in its figure being "a single whitebox, which shall be
documented by an instance of the whitebox template", and warns that the tree is never drawn in
one diagram. The rationale is not optional: [[tip-5-8]] asks every whitebox to answer why it has
these five parts and why A talks to B, and calls that the design rationale. [[tip-5-4]] binds the
first one to the world outside — level 1 has to stay consistent with the context's external
interfaces — and [[tip-5-9]] offers a way to constrain a whitebox without decomposing it at all,
by describing its required behaviour with the techniques of the [[runtime-view]].

**Distinguish from.** [[blackbox]] — the same building block with its insides withheld.
[[view]] — the building block view is the whole tree; a whitebox is one node of it. Note that
the site's tags do not use the word *view* for this section at all: its pages are tagged
[[building-block]].
