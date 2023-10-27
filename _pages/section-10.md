---
layout: arc42-doc-section
title: 10 - Quality
permalink: /section-10/
order: 14
---

### 10. Quality Requirements

<div class="arc42-help" markdown="1">

### Content
This section contains all quality requirements as quality tree with scenarios.
The most important ones have already been described in section 1.2. (quality goals)

Here you can also capture quality requirements with lesser priority,
which will not create high risks when they are not fully achieved.

### Motivation
Since quality requirements will have a lot of influence on architectural
decisions you should know for every stakeholder what is really important to them,
concrete and measurable.

<!-- collect all examples that are related to this section of arc42 -->
{% include example.md category="quality" %}

</div>


### 10.1 Quality Requirements
<div class="arc42-help" markdown="1">

### Content
The table or tree (as defined in ATAM – Architecture Tradeoff Analysis Method) of quality requirements, with quality/evaluation scenarios as leaves.

### Motivation
The table or tree structure with priorities provides an overview for a sometimes large number of quality requirements.

### Form
The quality tree is a high-level overview of the quality goals and requirements:

* a table, containing specific quality requirements
* tree-like refinement of the term "quality". Use "quality" or "usefulness" as a root
* a mind map with quality categories as main branches

In any case the tree should include links to the scenarios of the following section.

</div>

_&lt;describe quality tree here >_

### 10.2 Quality Scenarios

<div class="arc42-help" markdown="1">

### Content
Concretization of (sometimes vague or implicit) quality requirements using (quality) scenarios.

These scenarios describe what should happen when a stimulus arrives at the system.

For architects, two kinds of scenarios are important:

* Usage scenarios (also called application scenarios or use case scenarios) describe the system’s runtime reaction to a certain stimulus. This also includes scenarios that describe the system’s efficiency or performance. Example: The system reacts to a user’s request within one second.
* Change scenarios describe a modification of the system or of its immediate environment. Example: Additional functionality is implemented or requirements for a quality attribute change.

### Motivation
Scenarios make quality requirements concrete and allow to more easily measure or decide whether they are fulfilled.

Especially when you want to assess your architecture using methods like ATAM you need to describe your quality goals (from section 1.2) more precisely down to a level of scenarios that can be discussed and evaluated.

### Form
Tabular or free form text.

</div>

_&lt;describe quality scenarios here >_

## See also

Since January 2023, arc42 provides a <a target="_blank" rel="noopener noreferrer nofollow" href="https://quality.arc42.org">pragmatic quality model</a>, that does not require a strict hierarchy of quality requirements, but proposes to _label_ them, with labels "flexible, efficient, usable, operable, testable, secure, safe" and "reliable".
0
![Q42, the arc42 quality model, with eight labels for system qualities](/images/10-quality/arc42-system-qualities-overview.svg)


{% include further-info.md
   category="quality"
   topic="quality requirements, quality-tree and/or quality scenarios"
   faqlink="https://faq.arc42.org/category_c/#c-sec-10" %}
