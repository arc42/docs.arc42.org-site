---
layout: arc42-doc-section
title: 11 - Risks and technical debt
permalink: /section-11/
order: 15
category: risks
tags: _TBD risk technical-debt
---

## Content

## Motivation

## Form


## Examples and tips

<div id="search-results">
    <hr id="first-hr" class="with-no-margin"/>

    {% assign selected_posts = (site.posts | where: "category", "risks") | reverse %}
    {% for post in selected_posts  %}
    <div class="article-wrapper">
        <article>
            {% include article-header.html page=post link=true share=false eye_catch=false %}
        </article>
    </div>
    <hr class="with-no-margin"/>
    {% endfor %}
</div>
