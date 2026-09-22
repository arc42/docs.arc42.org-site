---
id: port
type: term
title: Port
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-022-section-3-content]]'
related:
- '[[interface]]'
- '[[external-interface]]'
- '[[building-block]]'
term: Port
aliases:
- UML port
legacy-tags:
- port
home: '[[section-3]]'
---

**Definition.** A named connection point on the boundary of a building block, standing for a
whole group of interfaces rather than a single one.

**In arc42.** One tip uses it, and uses it for a specific job: [[tip-3-8]] offers ports as the
third way of taming a crowded context, after stereotyped categories ([[tip-3-7]]) and plain
abstraction ([[tip-3-6]]). Its argument is that a port does something the other two cannot —
"ports have the great advantage that they connect inside and outside", so the same symbol names
a cluster of neighbours and the internal blackbox that serves them, at the price of nothing but
a small square on the boundary.

**Distinguish from.** [[interface]] — an interface is one contract; a port is a place on the
boundary where any number of them are reached. [[external-interface]] — a port is not itself a
crossing of the system boundary, it is the labelled point where the crossings are grouped.
Because ports belong to a [[building-block]] and not only to the system as a whole, section 5
can use them at every level of decomposition, though the site does not yet do so.
