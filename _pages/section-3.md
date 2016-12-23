---
layout: page
title: 3 - Context and scope
permalink: /section-3/
order: 7
---

<h2 class="tag-box inline">Context and scope</h2>


#### Content

Die Kontextabgrenzung grenzt das System von allen Kommunikationspartner
(Nachbarsysteme und Benutzerrollen) ab. Sie legt damit die externen Schnittstellen fest.
Differenzieren Sie fachlichen Kontext (fachliche Ein- und Ausgaben) und
technischen Kontext (Kanäle, Protokolle, Hardware), falls nötig.

#### Motivation

Die fachlichen und technischen Schnittstellen zu Kommunikationspartnern gehören zu den
kritischsten Aspekten eines Systems. Stellen Sie rechtzeitig sicher,
dass Sie diese komplett verstanden haben.


#### Form

*  Diverse Kontextdiagramme
*  Listen von Kommunikationspartnern mit deren Schnittstellen.

<h2 class="tag-box inline">3.1 Business context</h2>

<h2 class="tag-box inline">3.2 Technical context</h2>


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
