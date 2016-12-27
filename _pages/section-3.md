---
layout: arc42-doc-section
title: 3 - Context and scope
permalink: /section-3/
order: 7
---
<p class="arc42-template-content">Reminder: Text marked with the small arc42 icon
and blue background is part of the arc42 template.</p>


<h2 class="arc42-template-content">3 Context and scope</h2>


#### Content

System scope and context - as the name suggests - delimits your system (i.e. your scope) from all its communication partners (neighboring systems and users, i.e. the context of your system). It thereby specifies the external interfaces.

If necessary, differentiate the business context (domain specific inputs and outputs) from the technical context (channels, protocols, hardware).

#### Motivation

The domain interfaces and technical interfaces to communication partners are among
your system's most critical aspects. Make sure that you completely understand them.


#### Form

* Various context diagrams
* Lists of communication partners and their interfaces.


<h2 class="arc42-template-content">3.1 Business context</h2>

#### Content

Specification of *all* communication partners (users, IT-systems, ...) with explanations of domain specific inputs and outputs or interfaces. Optinoally you can add domain specific formats or communication protocols.

#### Motivation
All stakeholders shoud understand which data are exchanged with the environment of the system.

#### Form
All kinds of diagrams that show the system as a black box and specify the domain interfaces to communiations partners.

Alternatively (or additionally) you can use a table. The title of the table is the name of your system, the three columns contain the name of the communication partner, the inputs, and the outputs.

<h4 class="arc42-template-content">Diagram or Table</h4>

<h4 class="arc42-template-content">(optionally:) Explanation of external domain interfaces</h4>

<h2 class="arc42-template-content">3.2 Technical context</h2>

#### Contents
Technical interfaces (channels and transmission media) linking your system to its environment. In addition a mapping of domain specific input/output to the channels, i.e. an explanation with I/O uses which channel.

#### Motivation
Many stakeholders make architectural decision based on the technical interfaces between the system and its context. Especially infrastructure or hardware designers decide these technical interfaces.

#### Form
E.g. UML deployment diagram describing channels to neighboring systems, together with a mapping table showing the relationships between channels and input/output.

<h4 class="arc42-template-content">Diagram or Table</h4>

<h4 class="arc42-template-content">(optionally:) Explanation of technical interfaces</h4>

<h4 class="arc42-template-content">Mapping of Input/Output to Channels</h4>


## Examples and Tips

<div id="search-results">
    <hr class="with-no-margin"/>
    {% assign selected_posts = (site.posts | where: "category", "context") | reverse %}
    {% for post in selected_posts  %}
    <div class="article-wrapper">
        <article>
            {% include article-header.html page=post link=true share=false eye_catch=false %}
        </article>
    </div>
    <hr class="with-no-margin"/>
    {% endfor %}
</div>
