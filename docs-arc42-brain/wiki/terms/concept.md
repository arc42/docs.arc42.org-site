---
id: concept
type: term
title: Concept
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-016-section-4-content]]'
- '[[SRC-019-section-12-content]]'
- '[[SRC-020-section-8-content]]'
related:
- '[[view]]'
- '[[solution-strategy]]'
- '[[glossary]]'
- '[[i18n]]'
- '[[domain]]'
- '[[building-block]]'
term: Concept
aliases:
- Crosscutting concept
- Cross-cutting concept
legacy-tags:
- concept
home: '[[section-8]]'
---

**Definition.** A solution idea, rule or regulation that holds for several building blocks at
once, so it cannot be written down inside any single one of them.

**In arc42.** Section 8 collects them — persistence, logging, error handling, security,
internationalization, build and test — which is why arc42 calls them *crosscutting* concepts: they
cut across the structure that section 5 describes. A concept is where the detail belongs:
[[tip-4-1]] keeps the solution strategy to a list of keywords and sends the reader to section 8
for the explanation, and [[tip-4-4]] names concepts, views and code as the three places the
strategy should refer to instead of repeating.

**Distinguish from.** [[solution-strategy]] — the strategy is the short summary of the few
decisions that shape the architecture; a concept is one of those decisions worked out in full.
[[view]] — a view is a projection of the whole system onto one concern, a concept is a rule
applying across the parts a view shows.
