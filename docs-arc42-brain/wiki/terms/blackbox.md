---
id: blackbox
type: term
title: Blackbox
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[whitebox]]'
- '[[building-block]]'
- '[[interface]]'
term: Blackbox
aliases:
- Black box
- Black-box
legacy-tags:
- blackbox
home: '[[section-5]]'
---

**Definition.** A building block described only by what it is responsible for and what crosses
its boundary — its insides deliberately left out.

**In arc42.** Half of the section's method, and the half that saves the effort:
[[tip-5-6]] spells out what the omission buys, namely that the insides can change without any
client adapting, that the whitebox need never be written at all, and that fewer stakeholders have
to hold fewer details. [[tip-5-5]] says what must then be said instead — a responsibility in one
or two sentences, with "too many 'and'" read as a sign of a missing abstraction — and
[[tip-5-7]] turns that into a table with two required rows and five optional ones.

The theory does not quite survive contact: [[tip-5-6]] admits that responsibility and interface
are sometimes not enough, and walks through a square-root function whose precision,
authorization, parallelism, cost and speed all matter to a caller. Those are quality
requirements attached to a [[building-block]], which is why the full template has a row for
them.

**Distinguish from.** [[whitebox]] — the same building block with its decomposition shown.
Every whitebox contains blackboxes and every blackbox may be opened into a whitebox, so the two
are not two kinds of thing but two ways of writing about one thing, chosen level by level.
[[interface]] — what a blackbox description must name, not what it is.
