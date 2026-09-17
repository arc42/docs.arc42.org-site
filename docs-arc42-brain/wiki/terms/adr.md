---
id: adr
type: term
title: Architecture Decision Record (ADR)
status: review
created: '2026-09-17'
updated: '2026-09-17'
sources:
- '[[SRC-009-section-9-page]]'
- '[[SRC-013-section-9-content]]'
related:
- '[[architecture-decision]]'
- '[[tip-9-5]]'
- '[[tip-9-8]]'
- '[[tip-9-9]]'
- '[[tip-9-10]]'
- '[[09-decision-example-adr]]'
term: Architecture Decision Record (ADR)
aliases:
- ADR
- Architecture Decision Record
legacy-tags:
- adr
home: '[[section-9#Background (on ADRs)]]'
---

**Definition.** An Architecture Decision Record is a short document that records a single
architecture decision in a fixed structure — title, context, decision, status and consequences —
so that the motivation behind the decision is not lost.

**In arc42.** Section 9 offers an ADR per important decision as the first of three possible forms
and reproduces the structure proposed by Michael Nygard: a proper noun-phrase *title*, the
*context* with its technical, political, social and project forces, the *decision* as a reply to
those forces, a *status* (proposed, accepted, deprecated, superseded) and all *consequences*,
positive, negative and neutral. Smaller documents are easier to read, create and maintain, which is
why arc42 recommends a few of them over one large decision chapter.

**Distinguish from.** [[architecture-decision]] — the decision is the choice that was made, the
ADR is the record of it.
