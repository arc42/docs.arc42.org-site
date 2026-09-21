---
id: requirement
type: term
title: Requirement
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-001-section-1-page]]'
- '[[SRC-015-section-1-content]]'
related:
- '[[functional-requirement]]'
- '[[business-goal]]'
- '[[constraint]]'
term: Requirement
aliases: []
legacy-tags:
- requirement
- overview
- cluster
home: '[[section-1#1.1 Requirements Overview]]'
---

**Definition.** A statement of what the system must do or how well it must do it, against which
the finished system can be judged.

**In arc42.** Section 1.1 does not restate the requirements — it gives a short overview of the
functional ones and the driving forces, and refers to the requirements documents where they
exist. The tips of section 1.1 are about keeping that overview short (less than a page,
[[tip-1-1]]), about grouping requirements into clusters instead of listing them
([[tip-1-4]]), and about being able to cite an individual requirement by a stable id when a
design decision has to be justified ([[tip-1-5]]).

**Distinguish from.** [[functional-requirement]] and [[quality-requirement]] — the two kinds
arc42 keeps in different places, the first in section 1.1, the second in sections 1.2 and 10.
[[constraint]] — a constraint also binds the architect, but it is not something the system does or
achieves; it removes options.

**Note on the legacy tag.** On the site, `requirement` tags every post of section 1, including the
ones about quality goals and stakeholders, where it means "section 1" rather than the concept. The
brain references this term only on the tips that really are about requirements in general; the
rest carry `section:` plus their specific term. See
[[ISS-017-blanket-requirement-tag-on-every-section-1-post|ISS-017]].
