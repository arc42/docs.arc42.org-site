---
layout: page
title: 6 - Runtime view
permalink: /section-6/
order: 10
category: runtime
tags: _TBD runtime scenario
---

## Content

## Motivation

## Form


## Examples and tips

<div id="search-results">
    <hr id="first-hr" class="with-no-margin"/>

    {% assign selected_posts = (site.posts | where: "category", "runtime") | reverse %}
    {% for post in selected_posts  %}
    <div class="article-wrapper">
        <article>
            {% include article-header.html page=post link=true share=false eye_catch=false %}
        </article>
    </div>
    <hr class="with-no-margin"/>
    {% endfor %}
</div>
