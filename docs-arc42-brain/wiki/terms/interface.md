---
id: interface
type: term
title: Interface
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-018-section-11-content]]'
- '[[SRC-020-section-8-content]]'
related:
- '[[external-interface]]'
- '[[building-block]]'
term: Interface
aliases: []
legacy-tags:
- interface
home: '[[section-5]]'
---

**Definition.** The boundary at which a building block offers its services to others, described by
what crosses it rather than by what is behind it.

**In arc42.** Interfaces are what makes the building block view of section 5 useful: a black box
is only a black box because its interface says everything a caller needs. The context of section 3
is the special case where the partner on the other side is outside the system
([[external-interface]]). [[tip-11-2]] is why the term matters to section 11 — an interface is a
place where two parties' assumptions meet, which makes it a reliable source of problems and
[[risk|risks]] for availability, robustness and security.

**Distinguish from.** [[external-interface]] — an external interface is an interface to a
communication partner outside the system; section 3 specifies those, section 5 the internal ones
between building blocks.
