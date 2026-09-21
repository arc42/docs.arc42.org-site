---
id: domain
type: term
title: Domain
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-020-section-8-content]]'
related:
- '[[concept]]'
- '[[glossary]]'
term: Domain
aliases:
- Domain model
- Business domain
- Business model
legacy-tags:
- domain
home: '[[section-8]]'
---

**Definition.** The subject matter the system is about — its things, activities and rules — and
the model that captures them.

**In arc42.** A crosscutting topic, and [[tip-8-5]] gives the reason plainly: business or domain
elements "will be referred-to from numerous building blocks", so describing them inside any one
building block would mean repeating them. Section 8 is therefore where the domain model belongs,
in graphical form for the overview. arc42 offers a ladder rather than one right answer: a full
Domain-Driven Design model with entities, aggregates, services and value objects if the team works
that way, or a plain logical data model ([[tip-8-7]]: "if you don't get at least your data right,
your system is likely to fail"), or process and activity models. [[tip-8-6]] splits the work with
section 12 — the relationships go in the concept, the definitions in the [[glossary]].

**Distinguish from.** [[glossary]] — the glossary defines each term for everyone; the domain model
shows how the terms relate, which is what makes it a concept rather than a list. DDD's *ubiquitous
language* is where the two meet, and [[tip-8-5]] and [[tip-12-2]] each name it from their own side.

**Note on the tag.** The site's tag is `domain` and the slug follows it, so the emitted tag keeps
that spelling; "Domain model" and "Business domain" are aliases.
