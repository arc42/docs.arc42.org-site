---
id: solution-strategy
type: term
title: Solution strategy
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-004-section-4-page]]'
- '[[SRC-015-section-1-content]]'
- '[[SRC-016-section-4-content]]'
related:
- '[[architecture-decision]]'
- '[[quality-goal]]'
- '[[view]]'
- '[[concept]]'
term: Solution strategy
aliases: []
legacy-tags:
- solution-strategy
home: '[[section-4]]'
---

**Definition.** The short summary of the fundamental decisions and solution approaches that shape
the architecture.

**In arc42.** Section 4 holds it, and it is where the most important architecture decisions are
already captured. [[tip-1-17]] uses it as the place for the table that pairs a quality goal with
the decision it drove, so that section 1.2 needs only a reference; the same tip points at tip 4-2
for the table's shape.

Section 4's own tips are almost entirely about keeping it short. Two forms are offered and both
are deliberately thin: a list of keywords ([[tip-4-1]]) or a table whose columns are quality goal,
scenario, approach and a link to the details ([[tip-4-2]], with [[tip-4-3]] for systems whose
quality requirements are the driving force). The detail belongs elsewhere — [[tip-4-4]] sends the
reader to a [[concept]], a [[view]] or the code — the strategy may grow with the system rather
than being decided up front ([[tip-4-5]]), and whatever it contains has to say *why*
([[tip-4-6]]).

**Distinguish from.** [[architecture-decision]] — the strategy is the small set of shaping
decisions taken together and summarised; section 9 records individual decisions with their
rationale.
