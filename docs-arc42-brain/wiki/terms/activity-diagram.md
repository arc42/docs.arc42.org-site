---
id: activity-diagram
type: term
title: Activity diagram
status: review
created: '2026-09-21'
updated: '2026-09-22'
sources:
- '[[SRC-006-section-6-page]]'
- '[[SRC-015-section-1-content]]'
- '[[SRC-024-section-6-content]]'
related:
- '[[bpmn]]'
- '[[plantuml]]'
- '[[functional-requirement]]'
- '[[runtime-view]]'
- '[[runtime-scenario]]'
- '[[sequence-diagram]]'
term: Activity diagram
aliases: []
legacy-tags:
- activity-diagram
home: '[[section-6]]'
---

**Definition.** A UML diagram showing a flow of actions, with its branches, alternatives,
parallel paths and sequences.

**In arc42.** Two sections tag it, for two different jobs. Section 1 uses it for functional
requirements: [[tip-1-6]] recommends it for the visual overview it gives of activities and
special cases, and names the price — "the relatively high cost of creation and maintenance". The
alternatives arc42 offers against it there are [[bpmn]] when stakeholders find it too technical
([[tip-1-7]]), a numbered list when the process is simple ([[tip-1-8]]), and a text notation that
renders to the same diagram ([[plantuml]], [[tip-1-9]]); [[tip-1-8]] gives the rule for choosing,
namely that concurrent processes are what activity diagrams do better than a list. Section 6 uses
it for [[runtime-scenario|runtime scenarios]], and spends both its tips on the same question —
how to show which building block does what. [[tip-6-7]] answers with swimlanes, which group
activities by the actor performing them; [[tip-6-8]] answers with partitions, which modularise
the diagram itself. Swimlanes are what [[tip-6-1]] has in mind when it lists activity diagrams
among the notations that map activities to building blocks for you.

**Distinguish from.** [[bpmn]] — a different notation for the same job, addressed at business
rather than technical readers. [[plantuml]] — a tool that *produces* activity diagrams from
text, not a notation of its own. [[sequence-diagram]] — section 6's other tagged notation, which
orders by time along a lifeline instead of grouping by actor.
