---
layout: arc42-doc-section
title: 9 - Architecture decisions
permalink: /section-9/
order: 13
---

### 9. Architecture Decisions

<div class="arc42-help" markdown="1">


### Content
Important, expensive, large scale or risky architecture decisions including rationales. With "decisions" we mean selecting one alternative based on given criteria.

Please use your judgement to decide whether an architectural decision should be documented here in this central section or whether you better document it locally (e.g. within the white box template of one building block). Avoid redundant texts. Refer to section 4, where you captured the most important decisions of your architecture already.

### Motivation
Stakeholders of your system should be able to comprehend and retrace your decisions.

### Form

* ADR ([architecture decision record](https://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions)) for every important decision
* list or table, ordered by importance and consequences or
* more detailed in form of separate sections per decision

### Background (on ADRs)
Smaller pieces of documentation are easier to read, create and maintain.
When it comes to architecture decisions, development teams will often:

*  _know_ about the decision, as it visible e.g. in source code, but
*  _miss_ the motivation behind that decision (see [Nygard 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions))

Therefore you should document a few important decisions together with their motivation, reasoning

#### Our proposal concerning decisions
Keep a collection of _architecturally significant_ decisions,
those decisions that affect the structure, quality characteristics, important (especially external) dependencies and interfaces, or construction techniques (thanx to Michael Nygard for [this proposal](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions))

You might follow the Nygard-structure, which works as follows:

| Section | Description |
| --------| ------------|
| Title   | Decisions should have a proper name.  For example, "ADR 42: Strategy-Pattern for multiple checking algorithms" or "ADR 9: Keycloak for secrets management" |
| Context | Describe the situation, including technical, political, social, and project aspects. These forces might be in tension. |
| Decision | What is our decision (_reply_ to the forces described in the context) |
| Status   | A decision may be "proposed" if the important stakeholders haven't agreed with it yet, or "accepted" once it is agreed. It could also be "deprecated" or "superseded", hopefully with a reference to its replacement. |
| Consequences |What will or can happen as consequences of this decision. All consequences should be listed here, not just the "positive" ones. A particular decision may have positive, negative, and neutral consequences, but all of them affect the team and project in the future. |

You can find additional structures of ADR in the [ADR Github collection](https://adr.github.io/)

<!-- collect all examples that are related to this section of arc42 -->
{% include example.md category="decisions" %}

</div>

_&lt;describe important architecture decisions here >_


{% include further-info.md
   category="decisions"
   topic="fundamental architecture and design decisions"
   faqlink="https://faq.arc42.org/category_c/#c-sec-9" %}
