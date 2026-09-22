---
id: technical-context
type: term
title: Technical context
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-022-section-3-content]]'
related:
- '[[context]]'
- '[[business-context]]'
- '[[infrastructure]]'
- '[[deployment-view]]'
term: Technical context
aliases:
- Technical context view
legacy-tags:
- technical-context
home: '[[section-3]]'
---

**Definition.** The context described in channels, protocols and transmission media, together
with the mapping that says which domain input or output uses which channel.

**In arc42.** Subsection 3.2, and the optional half: needed when hardware, buses or
transmission channels are central to the system, which for embedded systems is nearly always
([[tip-3-15]]) and for information systems rarely. Its distinguishing content is the mapping —
[[tip-3-18]] asks for domain interfaces and their technical realization to be related in a
table, which is the one thing neither half can state alone.

**Distinguish from.** [[business-context]] — the same partners in the other vocabulary.
[[deployment-view]] — the harder call, and [[tip-3-19]] makes it: a team focused on domain
topics can leave technology out of section 3 entirely and give it in section 7 instead. So a
technical context is not a small deployment view; it is the claim that the
[[infrastructure]] matters already at the system boundary.
