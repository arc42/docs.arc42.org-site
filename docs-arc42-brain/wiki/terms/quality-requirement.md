---
id: quality-requirement
type: term
title: Quality requirement
status: review
created: '2026-09-17'
updated: '2026-09-21'
sources:
- '[[SRC-010-section-10-page]]'
- '[[SRC-013-section-9-content]]'
- '[[SRC-015-section-1-content]]'
related:
- '[[constraint]]'
- '[[decision-criteria]]'
- '[[stakeholder]]'
- '[[tip-9-1]]'
- '[[quality-goal]]'
- '[[quality-scenario]]'
- '[[quality-tree]]'
- '[[quality-model]]'
term: Quality requirement
aliases: []
legacy-tags:
- quality
- quality-requirements
home: '[[section-10]]'
---

**Definition.** A required quality property of the system, stated in a specific and measurable
way.

**In arc42.** Section 10 contains all relevant quality requirements: the most important ones are
already described as quality goals in section 1.2 and are only referenced, while section 10 also
captures the ones of lesser importance that create no high risk when they are not fully achieved.
Their relevance for section 9 is stated in section 10's motivation: quality requirements have a
lot of influence on architectural decisions, which is why tip 9-1 counts "influencing important
quality attributes" among the reasons to document a decision.

**Distinguish from.** [[decision-criteria]] — a quality requirement is a property of the system;
a decision criterion is a yardstick for comparing alternatives, which may or may not be a quality
requirement.
