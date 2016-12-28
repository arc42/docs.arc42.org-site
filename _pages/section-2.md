---
layout: arc42-doc-section
title: 2 - Constraints
permalink: /section-2/
order: 6
category: constraints
tags: _TBD constraints conventions
---

### 2. Architecture Constraints


<div class="arc42-help" markdown="1">

### Content

Any requirement that constrains software architects in their freedom of design and implementation decisions or decision about the development process. These constraints sometimes go beyond individual systems and are valid for whole organizations and companies.


### Motivation
Architects should know exactly where they are free in their design decisions and where they must adhere to constraints.
Constraints must always be dealt with; they may be negotiable, though.

### Form
Simple tables of constraints with explanations. If needed you can subdivide them into technical constraints, organizational and political constraints and conventions (e.g. programming or versioning guidelines, documentation or naming conventions)

</div>

#### _&lt;insert relevant constraints>_



## Examples and tips

<div id="search-results">
    <hr id="first-hr" class="with-no-margin"/>

    {% assign selected_posts = (site.posts | where: "category", "constraints") | reverse %}
    {% for post in selected_posts  %}
    <div class="article-wrapper">
        <article>
            {% include article-header.html page=post link=true share=false eye_catch=false %}
        </article>
    </div>
    <hr class="with-no-margin"/>
    {% endfor %}
</div>
