---
layout: page
title: 5 - Building block view
permalink: /section-5/
order: 9
category: building-blocks
tags: _TBD building-block blackbox whitebox hierarchy
---

## Content

## Motivation

## Form


## Examples and tips

<div id="search-results">
    <hr id="first-hr" class="with-no-margin"/>

    {% assign selected_posts = (site.posts | where: "category", "building-blocks") | reverse %}
    {% for post in selected_posts  %}
    <div class="article-wrapper">
        <article>
            {% include article-header.html page=post link=true share=false eye_catch=false %}
        </article>
    </div>
    <hr class="with-no-margin"/>
    {% endfor %}
</div>
