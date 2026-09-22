---
id: context
type: term
title: Context
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-022-section-3-content]]'
related:
- '[[external-interface]]'
- '[[business-context]]'
- '[[technical-context]]'
- '[[interface]]'
term: Context
aliases:
- System context
- Context and scope
- Scope
legacy-tags:
- context
home: '[[section-3]]'
---

**Definition.** Everything the system talks to but is not, together with the boundary that
decides which side each thing is on.

**In arc42.** Section 3 is where the boundary is drawn, and drawing it is the point:
[[tip-3-1]] asks for "what's inside" and what is outside to be stated explicitly, because that
is what fixes the system's responsibilities against its neighbours'. The context is the one
place in arc42 where completeness is demanded — [[tip-3-9]] makes the exception to the site's
usual advice and asks for *all* external neighbours — while [[tip-3-5]] forbids the detail that
completeness invites. The two hold together only through abstraction, which is why grouping
neighbours ([[tip-3-6]], [[tip-3-7]], [[tip-3-8]]) takes three tips of its own.

**On the tags.** [[tip-3-7]] also carried `cluster` and `criteria`, which say nothing about the
context that this term does not: on that page they mean "group the neighbours, and say by what
rule". Both names were already claimed by other terms for other meanings — `cluster` by
[[requirement]] since section 1, `criteria` by [[decision-criteria]] since section 9 — so under
the policy of [[ISS-034-the-site-tag-scenario-means-two-different-things|ISS-034]] they fold here
by meaning without being claimed here by name. Both reach zero at section 3's cut-over, finishing
a consolidation sections 1 and 9 began.

**Distinguish from.** [[external-interface]] — the context is the *set* of partners and the
boundary around them; an external interface is one crossing of that boundary. The distinction
matters because the context can be complete while the interfaces stay unspecified, which is
exactly the state section 3 asks for and section 5 later fills in. [[business-context]] and
[[technical-context]] are the same context told twice, in two vocabularies.
