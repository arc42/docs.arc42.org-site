---
id: quality-scenario
type: term
title: Quality scenario
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-001-section-1-page]]'
- '[[SRC-015-section-1-content]]'
- '[[SRC-017-section-10-content]]'
related:
- '[[quality-requirement]]'
- '[[quality-goal]]'
- '[[atam]]'
term: Quality scenario
aliases:
- Scenario
legacy-tags:
- scenario
- quality-scenario
home: '[[section-1#1.2 Quality Goals]]'
---

**Definition.** A short sentence describing how the system should react in a specific situation,
at a specific event, with a measurable outcome — the form that makes a quality requirement
concrete.

**In arc42.** Scenarios are the recommended form for quality goals in section 1.2 and for the
complete set in section 10. [[tip-1-12]] names three categories: usage scenarios (how the system
reacts in a certain kind of use), change scenarios (how it behaves when changed or extended) and
failure or downtime scenarios (how it behaves when something serious breaks). The examples that
tip gives are measurable on purpose — "within 1 second (up to 100 concurrent users)", "within at
most 60 person-hours" — because [[tip-1-16]] asks for brief explanations *with* scenarios rather
than keywords, and [[tip-1-11]] treats buzzwords as the failure mode scenarios prevent.

**Distinguish from.** [[quality-requirement]] — the requirement is the thing being stated, the
scenario is the form it is stated in. A quality requirement written as prose or a keyword is
still a quality requirement; it is simply not yet testable.
