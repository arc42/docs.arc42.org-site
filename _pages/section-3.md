---
layout: page
title: 3 - Context
permalink: /section-3/
order: 7
---


## Content

Die Kontextabgrenzung grenzt das System von allen Kommunikationspartner
(Nachbarsysteme und Benutzerrollen) ab. Sie legt damit die externen Schnittstellen fest.
Differenzieren Sie fachlichen Kontext (fachliche Ein- und Ausgaben) und
technischen Kontext (Kanäle, Protokolle, Hardware), falls nötig.



## Motivation

Die fachlichen und technischen Schnittstellen zu Kommunikationspartnern gehören zu den
kritischsten Aspekten eines Systems. Stellen Sie rechtzeitig sicher,
dass Sie diese komplett verstanden haben.


## Form

*  Diverse Kontextdiagramme
*  Listen von Kommunikationspartnern mit deren Schnittstellen.


## Examples and tips
 
<div id="search-results">
    <hr id="first-hr" class="with-no-margin"/>

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
