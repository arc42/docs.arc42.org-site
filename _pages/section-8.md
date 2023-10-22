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
* architectural patterns or design patterns
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

### Background
Some topics within systems often concern multiple building blocks, components or elements.
It might be easier to communicate or document such _cross-cutting_ topics at a central location, instead of repeating them in the description of the concerned elements.

Certain concepts might concern **all** elements of a system, others might only be relevant for a few.
In the diagram below, logging concerns all three components, whereas security is relevant only for two components.

![]({{ site.imageurl}}/concepts/crosscutting_concerns.drawio.png)

Some real-life examples:

* Within a system, a common format for log-messages shall be established, combined with a common convention of choosing the appropriate log-destination.
These decisions, along with implementation examples, could be described as "logging-concept".
* A system has numerous backend services, that communicate among each other based upon remote procedure calls or http-based REST.
Calling services ("consumers") always need to authenticate themselves to the called service ("provider").
For this authentication, a central common authorization service has to be used.
The technical and organizational details such authentication could be described as "backend authentication concept". 
* (taken from the HTML Sanity Checker, see below): 
All (7+) checker components within the system are structured according to the strategy pattern.



<!-- collect all examples that are related to this section of arc42 -->
<!-- ================================================================-->
{% include example.md category="concepts" %}

</div>

_&lt;describe concepts here >_


{% include further-info.md
   category="concepts"
   topic="crosscutting and/or technical concepts"
   faqlink="https://faq.arc42.org/category_c/#c-sec-8" %}
