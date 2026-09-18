---
id: 9-5
type: tip
title: 'Tip 9-5: Document decisions as `Architecture Decision Record` (ADR)!'
status: published
created: '2026-09-17'
updated: '2026-09-18'
sources:
- '[[SRC-013-section-9-content]]'
related:
- '[[tip-9-2]]'
- '[[tip-9-4]]'
- '[[tip-9-8]]'
- '[[tip-9-9]]'
- '[[tip-9-10]]'
- '[[adr]]'
- '[[09-decision-example-adr]]'
section: '[[section-9#Background (on ADRs)]]'
keywords: []
terms:
- '[[architecture-decision]]'
- '[[adr]]'
- '[[decision-criteria]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/9-5/
---

<a target="_blank" rel="noopener noreferrer nofollow" href="https://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions">Michael Nygard</a> has written
a blogpost about documenting important architecture decisions in a _pattern_ form:

>We will use a format with just a few parts, so each document is easy to digest. The format has just a few parts.
>
>**Title** These documents have names that are short noun phrases. For example, "ADR 1: Deployment on Ruby on Rails 3.0.10" or "ADR 9: LDAP for Multitenant Integration"<br>
>**Context** This section describes the forces at play, including technological, political, social, and project local. These forces are probably in tension, and should be called out as such. The language in this section is value-neutral. It is simply describing facts.<br>
>**Decision** This section describes our response to these forces. It is stated in full sentences, with active voice. "We will ..."<br>
>**Status** A decision may be "proposed" if the project stakeholders haven't agreed with it yet, or "accepted" once it is agreed. If a later ADR changes or reverses a decision, it may be marked as "deprecated" or "superseded" with a reference to its replacement.<br>
>**Consequences** This section describes the resulting context, after applying the decision. All consequences should be listed here, not just the "positive" ones. A particular decision may have positive, negative, and neutral consequences, but all of them affect the team and project in the future.<br>
quoted from <a target="_blank" rel="noopener noreferrer nofollow" href="https://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions">Michael Nygard</a>

You could describe this ADR format as tables.

## (These) ADR are missing _criteria_

I (Gernot) am missing the decision criteria (see [tip 9-2 (document decision criteria)](/tips/9-2)) - but maybe
I'm overly peculiar in that aspect...
