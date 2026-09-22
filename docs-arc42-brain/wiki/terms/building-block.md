---
id: building-block
type: term
title: Building block
status: review
created: '2026-09-21'
updated: '2026-09-22'
sources:
- '[[SRC-020-section-8-content]]'
- '[[SRC-021-section-7-content]]'
- '[[SRC-022-section-3-content]]'
- '[[SRC-023-section-5-content]]'
related:
- '[[concept]]'
- '[[view]]'
- '[[interface]]'
- '[[deployment-view]]'
- '[[port]]'
- '[[blackbox]]'
- '[[whitebox]]'
- '[[cohesion]]'
term: Building block
aliases:
- Building-block
legacy-tags:
- building-block
- buildingblock
home: '[[section-5]]'
---

**Definition.** A static part of the system at any level of decomposition — a subsystem,
component, class or package — described by what it does and what it offers, not by how it works
inside.

**In arc42.** Section 5, the building block view, is the hierarchy of them: each level opens one
black box into a white box of smaller ones. Building blocks are also what makes a [[concept]]
crosscutting — a concept is "not the property of any single building block, but a decision that
several of them share" ([[tip-8-1]]). [[tip-8-11]] closes the loop in the other direction: give
each important concept a name and stamp it on the building blocks that apply it, as the
stereotype «X-service» does in its diagram, so a reader of section 5 can see which concepts a part
of the system follows.

**On the tag.** The site spells it two ways: the 28 section 5 tips are tagged `building-block`,
its four examples `buildingblock`. The unhyphenated spelling is folded here and reaches zero at
section 5's cut-over, so the tips and the worked examples finally answer to one tag.

**Distinguish from.** [[blackbox]] and [[whitebox]] — not other kinds of building block but the
two ways of writing about one, with its insides withheld or shown. [[view]] — a view is a whole
projection of the system; a building block is one element inside the building block view. [[interface]] — the interface is the part of a
building block others depend on, which is why a black box can be understood without opening it.
