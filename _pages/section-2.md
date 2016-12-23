---
layout: page
title: 2 - Constraints
permalink: /section-2/
order: 6
category: constraints
tags: _TBD constraints conventions
---

## Content
Fesseln und Vorgaben, die ihre Freiheiten bezüglich Entwurf, Implementierung oder Ihres Entwicklungsprozesses einschränken. Diese Randbedingungen gelten manchmal organisations- oder firmenweit über die Grenzen einzelner Systeme hinweg.

## Motivation
Als Architekt sollten Sie explizit wissen, wo Ihre Freiheitsgrade bezüglich Entwurfsentscheidungen liegen und wo Sie Randbedingungen beachten müssen.
Sie können Randbedingungen vielleicht noch verhandeln, zunächst sind sie aber da.

## Form
Einfache Tabellen der Randbedingungen mit Erläuterungen. Bei Bedarf unterscheiden Sie technische, organisatorische und politische Randbedingungen oder übergreifende Konventionen (beispielsweise Programmier- oder Versionierungsrichtlinien, Dokumentation- oder Namenskonvention)


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
