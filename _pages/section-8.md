---
layout: arc42-doc-section
title: 8 - Concepts
permalink: /section-8/
order: 12
---

### 8. Crosscutting Concepts


<div class="arc42-help" markdown="1">

### Content
This section describes overall, principal regulations and solution ideas that are relevant in multiple parts (&rarr; cross-cutting) of your system.
Such concepts are often related to multiple building blocks. They include many different topics, such as

* domain models
* architectur patterns or design patterns
* rules for using specific technology
* principale, often technical decisions of overall decisions
* implementation rules

### Motivation
Concepts form the basis for _conceptual integrity_ (consistency, homogeneity) of the architecture. Thus, they are an important contribution to achieve inner qualities of your system.

Some of these concepts cannot be assigned to individual building blocks (e.g. security or safety). This is the place in the template that we provided for a cohesive specification of such concepts.

### Form
The form can be varied:

* concept papers with any kind of structure
* cross-cutting model excerpts or scenarios using notations of the architecture views
* example implementations,especially for technical concepts
* reference to typical usage of standard frameworks (e.g. using Hibernate for object/relational mapping)

### Structure of this Section
A potential (but not mandatory) structure for this section could be:

* Domain concepts
* User Experience concepts (UX)
* Safety and security concepts
* Architecture and design patterns
* "Under-the-hood" concepts
* Development concepts
* Operational concepts

Note: it might be difficult to assign individual concepts to one specific topic
on this list.

![]({{ site.imageurl }}/08-Crosscutting-Concepts-Structure.png)

<!-- collect all examples that are releated to this section of arc42 -->
{% include example.md category="concepts" %}

</div>

_&lt;describe concepts here >_


{% include further-info.md
   category="concepts"
   topic="crosscutting and/or technical concepts"
   faqlink="http://faq.arc42.org/category_c/#c-sec-8" %}
