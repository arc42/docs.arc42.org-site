---
id: cohesion
type: term
title: Cohesion
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[building-block]]'
- '[[concept]]'
term: Cohesion
aliases: []
legacy-tags:
- cohesion
home: '[[section-5]]'
---

**Definition.** The degree to which the elements inside one building block belong together.

**In arc42.** One tip carries the tag and it does not hedge: [[tip-5-17]] calls cohesion "one of
the most fundamental and classical software engineering design principles" and then concedes that
what *belongs* together depends on the viewpoint and differs between stakeholders, so the rule it
actually gives is to have consistent rules — similar business function, similar data, similar
users, similar technology, similar deployment, same maintainers. It is the principle the section
reasons from rather than a thing to document: [[tip-5-16]] invokes it as the reason to break its
own rule that a building block should be a package, when what sits in the package is not
cohesive.

**Distinguish from.** [[building-block]] — cohesion is the property by which a good one is
recognised, not a kind of one. [[concept]] — a crosscutting concept deliberately spans building
blocks, so it is the thing cohesion does *not* measure.
