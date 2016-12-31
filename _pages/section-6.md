---
layout: arc42-doc-section
title: 6 - Runtime view
permalink: /section-6/
order: 10
---

<div class="arc42-help" markdown="1">

### Content
This view describes concrete behavior and interactions of the system’s building blocks in form of scenarios from the following areas:

* important use cases or features: how do building blocks execute them?
* interactions at critical external interfaces: how do building blocks cooperate with users and neighbouring systems?
* operation and administration: launch, start-up, stop
* error and exception scenarios

Remark: The main criterion for the choice of possible scenarios (sequences, workflows) is their *architectural relevancy*. It is *not* important to describe a large number of scenarios. You should rather document a representative selection.

### Motivation
You should understand how (instances of) building blocks of your system perform their job and communicate at runtime.
You will mainly capture scenarios in your documentation to communicate your architecture to stakholders that are less willing or able to read and understand the static models (building block view, deployment view).

### Form
There are many notations for describing scenarios, e.g.

* numbered list of steps (in natural language)
* activity diagrams or flow charts
* sequence diagrams
* BPMN or EPCs (event process chains)
* state machines
* ...

</div>

#### 6.1 _&lt;Runtime Scenario 1>_

<div class="arc42-help" markdown="1">

* insert runtime diagram or textual description of the scenario
* insert description of the notable aspects of the interactions between the
building block instances depicted in this diagram.
</div>

##### _&lt;insert diagram for scenario 1>_

##### _&lt;describe notable aspects of interactions >_


#### 6.2 _&lt;Runtime Scenario 2>_

#### ...

#### 6.n _&lt;Runtime Scenario n>_


{% include further-info.md
   category="runtime"
   topic="runtime scenarios"
   faqlink="http://faq.arc42.org/category_c/#c-sec-6" %}
