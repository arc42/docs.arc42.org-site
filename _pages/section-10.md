---
layout: arc42-doc-section
title: 10 - Quality
permalink: /section-10/
order: 14
---

### 10. Quality Requirements

<div class="arc42-help" markdown="1">

### Content
This section contains all relevant quality requirements. 

The most important of these requirements have already been described in section 1.2. (quality goals), therefore they should only be referenced here.
In this section 10 you should also capture quality requirements with lesser importance, which will not create high risks when they are not fully achieved (but might be _nice-to-have_).

### Motivation
Since quality requirements will have a lot of influence on architectural decisions you should know  what qualities are really important for your stakeholders, in a specific and measurable way.


### Further Information

See the extensive [Q42 quality model on https://quality.arc42.org](https://quality.arc42.org).


<!-- collect all examples that are related to this section of arc42 -->
{% include example.md category="quality" %}

</div>


### 10.1 Quality Requirements Overview
<div class="arc42-help" markdown="1">

### Content

An overview or summary of quality requirements. 


### Motivation
Often we encounter dozens (or even hundreds) of detailed quality requirements. 
In this overview section you should try to summarize, e.g. by describing categories or topics (as suggested by [ISO 25010:2023](https://www.iso.org/obp/ui/#iso:std:iso-iec:25010:ed-2:v1:en) or [Q42](https://quality.arc42.org)

If these summary descriptions are already precise, specific enough and measurable, you may skip section 10.2.

### Form
Use a simple table in which each line contains a category or topic and a short description of the quality requirement.
Alternatively, you may use a mindmap to structure these quality requirements.

In literature, the idea of a _quality attribute tree_ has also been described, which puts the generic term "quality" as the root and uses a tree-like refinement of the term "quality". 
[Bass+21] introduced the term "Quality Attribute Utility Tree" for this purpose.


</div>

_&lt;Give an overview of quality requirements here >_

### 10.2 Quality Scenarios

<div class="arc42-help" markdown="1">

### Content
Quality scenarios make quality requirements concrete and allow to decide whether they are fulfilled (in the sense of acceptance criteria).
Ensure that your scenarios are specific and measurable.



Two kinds of scenarios are especially useful:

* _Usage scenarios_ (also called application scenarios or use case scenarios) describe the system’s runtime reaction to a certain stimulus. 
This also includes scenarios that describe the system’s efficiency or performance. 
Example: The system reacts to a user’s request within one second.
* _Change scenarios_ describe the desired effect of a modification or extension of the system or of its immediate environment. 
Example: Additional functionality is implemented or requirements for a quality attribute change, and the effort or duration of the change is measured.


### Form

Typical information for detailed scenarios include the following:

In short form (favoured in the Q42 model):

* **Context/Background**: What kind of system or component, what is the envirionment or situation?
* **Source/Stimulus**: Who or what initiates or triggers a behaviour, reaction or action.
* **Metric/Acceptance Criteria**: A response including a _measure_ or _metric_


The long form of scenarios (favoured by the SEI and [Bass+21]) is more detailed and includes the following information:

* **Scenario ID**: A unique identifier for the scenario.
* **Scenario Name**: A short, descriptive name for the scenario.
* **Source**: The entity (user, system, or event) that initiates the scenario.
* **Stimulus**: The triggering event or condition the system must address.
* **Environment**: The operational context or condition under which the system experiences the stimulus.
* **Artifact**: The building-blocks or other elements of the system affected by the stimulus.
* **Response**: The outcome or behavior the system exhibits in reaction to the stimulus.
* **Response Measure**: The criteria or metric by which the system’s response is evaluated.


### Examples
See [the Q42 quality model website](https://quality.arc42.org) for detailed examples of quality requirements.

### Further Information

* Len Bass, Paul Clements, Rick Kazman: "Software Architecture in Practice", 4th Edition, Addison-Wesley, 2021.

</div>

_&lt;describe quality scenarios here >_

## See also

Since January 2023, arc42 provides a <a target="_blank" rel="noopener noreferrer nofollow" href="https://quality.arc42.org">pragmatic quality model</a>, that proposes to _label_ quality requirements, with _hashtags_ or _labels_ like #flexible, #efficient, #usable, #operable, #testable, #secure, #safe" and #reliable.
0
![Q42, the arc42 quality model, with eight labels for system qualities](/images/10-quality/arc42-system-qualities-overview.svg)


{% include further-info.md
   category="quality"
   topic="quality requirements, quality-tree and/or quality scenarios"
   faqlink="https://faq.arc42.org/category_c/#c-sec-10" %}
