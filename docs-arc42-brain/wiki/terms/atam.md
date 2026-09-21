---
id: atam
type: term
title: ATAM
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-017-section-10-content]]'
related:
- '[[quality-scenario]]'
- '[[quality-tree]]'
term: ATAM
aliases:
- Architecture Tradeoff Analysis Method
legacy-tags:
- atam
home: '[[section-10]]'
---

**Definition.** A scenario-based method from the Software Engineering Institute for evaluating an
architecture against its quality requirements.

**In arc42.** Not part of the template — arc42 borrows two of its ideas. The quality tree of
section 10.1 is what the SEI literature calls a *Quality Attribute Utility Tree* ([[tip-10-2]]),
and [[tip-10-8]] uses the quality scenarios of section 10.2 as the input to a qualitative
evaluation, in a table that pairs each scenario with its solution approach and the risk that
remains. Tip 11-3 applies the same move the other way round: a qualitative evaluation is also how
you find the problems and risks section 11 records. arc42 recommends the two ideas while noting
that the full method is widely considered "overly formal and slow" ([[tip-10-2]]).

**Distinguish from.** [[quality-model]] — a quality model is a catalogue of quality properties to
choose from; ATAM is a procedure for judging one system against the properties it has chosen.
