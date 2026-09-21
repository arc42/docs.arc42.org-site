---
id: activity-diagram
type: term
title: Activity diagram
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-006-section-6-page]]'
- '[[SRC-015-section-1-content]]'
related:
- '[[bpmn]]'
- '[[plantuml]]'
- '[[functional-requirement]]'
term: Activity diagram
aliases: []
legacy-tags:
- activity-diagram
home: '[[section-6]]'
---

**Definition.** A UML diagram showing a flow of actions, with its branches, alternatives,
parallel paths and sequences.

**In arc42.** Section 6's *Form* lists "activity diagrams or flow charts" among the notations for
runtime scenarios, and section 1 uses the same notation for functional requirements:
[[tip-1-6]] recommends it for the visual overview it gives of activities and special cases, and
names the price — "the relatively high cost of creation and maintenance". The alternatives arc42
offers against it are [[bpmn]] when stakeholders find it too technical ([[tip-1-7]]), a numbered
list when the process is simple ([[tip-1-8]]), and a text notation that renders to the same
diagram ([[plantuml]], [[tip-1-9]]). [[tip-1-8]] gives the rule for choosing: concurrent
processes are what activity diagrams do better than a list.

**Distinguish from.** [[bpmn]] — a different notation for the same job, addressed at business
rather than technical readers. [[plantuml]] — a tool that *produces* activity diagrams from
text, not a notation of its own.
