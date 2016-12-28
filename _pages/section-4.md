---
layout: arc42-doc-section
title: 4 - Solution strategy
permalink: /section-4/
order: 8
category: solution-strategy
tags: _TBD solution-strategy concepts
---

<div class="arc42-help" markdown="1">

### Content

### Motivation

### Form

</div>

## Examples and tips

<div id="search-results">
    <hr id="first-hr" class="with-no-margin"/>

    {% assign selected_posts = (site.posts | where: "category", "solution-strategy") | reverse %}
    {% for post in selected_posts  %}
    <div class="article-wrapper">
        <article>
            {% include article-header.html page=post link=true share=false eye_catch=false %}
        </article>
    </div>
    <hr class="with-no-margin"/>
    {% endfor %}
</div>
