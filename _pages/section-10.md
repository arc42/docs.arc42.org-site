---
layout: arc42-doc-section
title: 10 - Quality
permalink: /section-10/
order: 14
category: quality
tags: _TBD quality cross-cutting
---

## Content

## Motivation

## Form


## Examples and tips

<div id="search-results">
    <hr id="first-hr" class="with-no-margin"/>

    {% assign selected_posts = (site.posts | where: "category", "quality") | reverse %}
    {% for post in selected_posts  %}
    <div class="article-wrapper">
        <article>
            {% include article-header.html page=post link=true share=false eye_catch=false %}
        </article>
    </div>
    <hr class="with-no-margin"/>
    {% endfor %}
</div>
