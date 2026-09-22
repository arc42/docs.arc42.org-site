---
id: business-context
type: term
title: Business context
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-022-section-3-content]]'
related:
- '[[context]]'
- '[[technical-context]]'
- '[[domain]]'
term: Business context
aliases:
- Domain context
legacy-tags:
- business-context
home: '[[section-3]]'
---

**Definition.** The context described in domain terms only: which partner gives the system what
information, and what it gets back — with no statement about how any of it travels.

**In arc42.** Subsection 3.1. It is the half of section 3 that every system needs, and for
information systems often the only half ([[tip-3-10]]). Because its audience is the stakeholders
who will never read a deployment diagram, [[tip-3-11]] goes as far as breaking UML on purpose
here: arrows are reversed to read as data flows, since "intuitively, many people understand an
arrow between software systems as data flow". That is the clearest statement in the whole site
that this diagram is a communication tool before it is a model.

**Distinguish from.** [[technical-context]] — same partners, different vocabulary. Keeping them
apart is the default ([[tip-3-10]]); [[tip-3-17]] allows merging them to save effort, and says
plainly that this is a trade, not an improvement. The domain language the business context
speaks is the [[domain]] model of section 8, which is where its terms should be defined rather
than re-explained in the context ([[tip-3-3]]).
