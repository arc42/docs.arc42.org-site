---
id: architecture-decision
type: term
title: Architecture decision
status: review
created: '2026-09-17'
updated: '2026-09-20'
sources:
- '[[SRC-009-section-9-page]]'
- '[[SRC-013-section-9-content]]'
related:
- '[[constraint]]'
- '[[adr]]'
- '[[decision-criteria]]'
- '[[tip-9-1]]'
term: Architecture decision
aliases: []
legacy-tags:
- decision
home: '[[section-9]]'
---

**Definition.** An architecture decision selects one alternative out of several, based on given
criteria, for a question that is architecturally significant.

**In arc42.** Section 9 defines a decision as "selecting one alternative based on given criteria"
and collects the important, expensive, large scale or risky ones together with their rationale.
A decision is *architecturally significant* when it affects the structure, quality characteristics,
important (especially external) dependencies and interfaces, or construction techniques of the
system. The most important decisions are already captured in section 4 (solution strategy); purely
local decisions may stay in the white box template of the building block they concern.

**Distinguish from.** [[adr]] — an ADR is one *format* for writing a decision down, not the
decision itself. [[decision-criteria]] — the yardstick a decision is measured against.
