---
layout: arc42-doc-section
title: 7 - Deployment view
permalink: /section-7/
order: 11
---

### 7. Deployment view

<div class="arc42-help" markdown="1">

### Content
The deployment view describes:

1. the technical infrastructure used to execute your system,
 with infrastructure elements like geographical locations, environments,
 computers, processors, channels and net topologies as well as other
 infrastructure elements and
2. the mapping of (software) building blocks to that infrastructure elements.

Often systems are executed in different environments, e.g. development environment, test environment, production environment. In such cases you should document all relevant environments.

Especially document the deployment view when your software is executed as
distributed system with more then one computer, processor, server or
container or when you design and construct your own hardware processors and
chips.

From a software perspective it is sufficient to capture those elements of the infrastructure that are needed to show the deployment of your building blocks.
Hardware architects can go beyond that and describe the infrastructure to any
level of detail they need to capture.

### Motivation
Software does not run without hardware.
This underlying infrastructure can and will influence your system and/or some
cross-cutting concepts. Therefore, you need to know the infrastructure.

### Form
Maybe the highest level deployment diagram is already contained in
section 3.2. as technical context with your own infrastructure as ONE black box. In this section you will zoom into this black box using additional deployment diagrams.

* UML offers deployment diagrams to express that view. Use it, probably with
nested diagrams, when your infrastructure is more complex.
* When your (hardware) stakeholders prefer other kinds of diagrams rather than UML
deployment diagram, let them use any kind that is able to show nodes and channels of the infrastructure.

</div>

#### 7.1 Infrastructure Level 1

<div class="arc42-help" markdown="1">
Describe (usually in a combination of diagrams, tables, and text):

* the distribution of your system to multiple locations, environments, computers, processors, .. as well as the physical connections between them
* important justification or motivation for this deployment structure
* Quality and/or performance features of the infrastructure
* the mapping of software artifacts (building blocks) to elements of the infrastructure

For multiple environments or alternative deployments please copy that section of arc42 for all relevant environments.
****
</div>

**&lt; insert infrastructure overview diagram >**


##### Motivation

_&lt; insert description of motivation or explanation in text form>_

##### (optional) Quality and/or Performance Features

_&lt; optionally insert description quality or performance features >_


##### Mapping

_&lt; insert description of mapping of building blocks >_



#### 7.2 Infrastructure Level 2

<div class="arc42-help" markdown="1">
Here you can include the internal structure of (some) infrastructure elements from
infrastructure level 1.

Please copy the structure from level 1 for each selected element.
</div>

##### 7.2.1 _&lt; Infrastructure element 1>_

_&lt; insert diagram + explanation >_

##### 7.2.2 _&lt; Infrastructure element 1>_

_&lt; insert diagram + explanation >_

##### ...

_&lt; insert diagram + explanation >_

##### 7.2.n _&lt; Infrastructure element 1>_
_&lt; insert diagram + explanation >_

{% include further-info.md
   category="deployment"
   topic="technical infrastructure, hardware, environments or deployment"
   faqlink="https://faq.arc42.org/category_c/#c-sec-7" %}
