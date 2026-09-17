---
id: decision-criteria
type: term
title: Decision criteria
status: review
created: '2026-09-17'
updated: '2026-09-17'
sources:
- '[[SRC-013-section-9-content]]'
related:
- '[[architecture-decision]]'
- '[[quality-requirement]]'
- '[[tip-9-2]]'
term: Decision criteria
aliases: []
legacy-tags:
- criteria
home: '[[section-9]]'
---

**Definition.** The criteria against which the alternatives of an architecture decision are
compared before one of them is selected; they are usually prioritized, either as a numerical
weight or in categories.

**In arc42.** Section 9 defines deciding as "selecting one alternative based on given criteria",
so the criteria are part of the decision. Tip 9-2 asks to ask the stakeholders for theirs: besides
purely technical criteria there may be organizational, formal, business-related or juristic (legal)
ones, and the same criterion may carry different priorities for different stakeholders. The
HtmlSanityChecker example shows criteria written down per decision.

**Distinguish from.** [[quality-requirement]] — a quality requirement is a property the system
must have and often becomes a criterion, but criteria also cover cost, licensing, skills and other
forces that are not properties of the system.
