---
id: glossary
type: term
title: Glossary
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-019-section-12-content]]'
related:
- '[[concept]]'
- '[[i18n]]'
term: Glossary
aliases: []
legacy-tags:
- glossary
home: '[[section-12]]'
---

**Definition.** The agreed definitions of the important business and technical terms used about a
system, in one place.

**In arc42.** Section 12, and the last section for a reason: it serves all the others. Its purpose
is that everyone involved shares one understanding of the terminology — [[tip-12-1]] calls it "one
manifestation of the general rule of 'better explicit than implicit'". arc42 asks for an
alphabetical table ([[tip-12-2]]), optionally a diagram of how the terms relate ([[tip-12-3]]) and
a column per language where stakeholders do not share one ([[tip-12-4]]). The advice that gives it
its character is the limit: 10 to 30 terms, specific to this system's problem and solution space,
because "you don't want to write another encyclopedia" ([[tip-12-5]]). Neither UML nor Java
belongs in it.

**Distinguish from.** [[concept]] — [[tip-12-2]] notes the glossary may be the same thing as
Domain-Driven Design's *ubiquitous language*, which would make it a crosscutting concept and put
it in section 8 as well; the difference is purpose, not content. A glossary defines terms, a
concept decides how something is done across the system.
