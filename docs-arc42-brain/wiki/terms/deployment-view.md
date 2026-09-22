---
id: deployment-view
type: term
title: Deployment view
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-021-section-7-content]]'
related:
- '[[view]]'
- '[[infrastructure]]'
- '[[hardware]]'
- '[[building-block]]'
term: Deployment view
aliases:
- Deployment
legacy-tags:
- deployment-view
- deployment
home: '[[section-7]]'
---

**Definition.** The view that shows the technical infrastructure a system runs on, and which parts
of the software run where.

**In arc42.** Section 7, the third of the three views. It answers two questions that only make
sense together: what the [[infrastructure]] looks like — nodes, channels, environments
([[tip-7-1]], [[tip-7-3]]) — and how the [[building-block|building blocks]] are mapped onto it.
[[tip-7-5]] is precise about what is mapped: not the building blocks themselves but the
*artifacts* compiled from them, often m:n, which is why one system can have several deployment
variants worth explaining. The mapping can be drawn as a UML deployment diagram ([[tip-7-6]]) or
written as a table ([[tip-7-7]]), and like the building block view it may be organised in levels
([[tip-7-4]]).

**Distinguish from.** [[view]] — the general idea; the deployment view is one of the three
concrete ones arc42 asks for. [[infrastructure]] — the infrastructure is the subject, the
deployment view is the description of it plus the mapping.

**Note on the tag.** The site tags the ten section 7 tips `deployment-view` and the three examples
`deployment`; both names map here, so the shorter one disappears from the keyword page at
cut-over.
