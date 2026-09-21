---
id: constraint
type: term
title: Constraint
status: review
created: '2026-09-20'
updated: '2026-09-21'
sources:
- '[[SRC-002-section-2-page]]'
- '[[SRC-014-section-2-content]]'
related:
- '[[quality-requirement]]'
- '[[architecture-decision]]'
- '[[stakeholder]]'
- '[[requirement]]'
term: Constraint
aliases:
- Architecture constraint
legacy-tags:
- constraint
- constraints
home: '[[section-2]]'
---

**Definition.** A requirement that limits the architect's freedom in design, implementation or
process decisions.

**In arc42.** Section 2 collects the constraints a system has to live with, because architects
should know exactly where they are free to decide and where they are not. Constraints often go
beyond a single system and hold for a whole organization or company. Section 2 distinguishes
technical constraints, organizational and political constraints, and conventions such as
programming, versioning, documentation or naming guidelines — [[tip-2-5]] asks for that split only
where it helps. A constraint must always be dealt with, but it is not always fixed: [[tip-2-2]]
asks for its consequences to be made explicit and for unreasonable ones to be renegotiated with
the [[stakeholder|stakeholders]] who imposed them.

**Distinguish from.** [[quality-requirement]] — a quality requirement says how well the system
must do something and leaves the how open; a constraint removes options outright.
[[architecture-decision]] — a decision picks one alternative from those the constraints left
standing, so constraints are the input to decisions, not a kind of decision.
