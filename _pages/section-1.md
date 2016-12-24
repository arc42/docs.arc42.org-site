---
layout: arc42-doc-section
title: 1 - Introduction and Goals
permalink: /section-1/
order: 5
tags: _TBD introduction goals stakeholder quality
---

## 1. Introduction and goals

### Content
Fassen Sie hier die wesentliche Anforderungen und treibenden Kräfte zusammen, die Softwarearchitekten und Entwicklungsteams berücksichtigen müssen. Dazu gehören:

* zugrunde liegenden Geschäftsziele, wesentliche Aufgabenstellung und essenzielle fachliche Anforderungen an das System,
* Qualitätsziele für die Architektur und
* relevante Stakeholder sowie deren Erwartungshaltung

## 1.1 Problem

### Content
Kurzbeschreibung der fachlichen Aufgabenstellung, treibenden Kräfte, Extrakt (oder Abstract) der Anforderungen.
Verweis auf (hoffentlich vorliegende) Anforderungsdokumente (mit Versionsbezeichnungen und Ablageorten).

### Motivation
Aus Sicht der späteren Nutzer ist die Unterstützung einer fachlichen Aufgabe oder Verbesserung der Qualität der eigentliche Beweggrund, ein neues System zu schaffen oder ein bestehendes zu modifizieren.

### Form
Kurze textuelle Beschreibung, eventuell in tabellarischer Use-Case Form.
Sofern vorhanden sollte die Aufgabenstellung Verweise auf die entsprechenden Anforderungsdokumente enthalten.

Halten Sie diese Auszüge so knapp wie möglich und wägen Sie Lesbarkeit und Redundanzfreiheit gegeneinander ab.

## 1.2 Quality goals

### Content
Die Top-3 bis Top-5 der Qualitätsziele für die Architektur, deren Erfüllung oder Einhaltung den maßgeblichen Stakeholdern besonders wichtig sind.
Gemeint sind hier wirklich Qualitätsziele, die nicht unbedingt mit den Zielen des Projekts übereinstimmen. Beachten Sie den Unterschied.


### Motivation
Sie müssen die für Ihre Stakeholder relevanten Qualitätsanforderungen an das System kennen, möglichst konkret und operationalisierbar. Wenn Sie als Architekt nicht wissen, woran Ihre Arbeit gemessen wird, ....

### Form
Einfache tabellarische Darstellung der Qualitätsziele mit möglichst konkreten Szenarien, geordnet nach Prioritäten.


## 1.3 Stakeholder
### Content
Expliziter Überblick über die Stakeholder des Systems, d.h. über alle Personen, Rollen oder Organisationen, die
* die Architektur kennen sollten oder
* von der Architektur überzeugt werden müssen,
* mit Architektur oder Code arbeiten (z.B. Schnittstellen nutzen),
* Dokumentation der Architektur für ihre eigene Arbeit benötigen,
* Entscheidungen über das System und dessen Entwicklung treffen.

### Motivation
Sie sollten die Projektbeteiligten und -betroffenen kennen, sonst erleben Sie später im Entwicklungsprozess Überraschungen. Diese Stakeholder bestimmen unter anderem Umfang und Detaillierungsgrad der von Ihnen zu leistenden Arbeit und Ergebnisse.

### Form
Einfache Tabelle mit Rollen- oder Personennamen, sowie deren Erwartungshaltung bezüglich der Architektur und deren Dokumentation.



## Examples and tips

<div id="search-results">
    <hr id="first-hr" class="with-no-margin"/>

    {% assign selected_posts = (site.posts | where: "category", "introduction") | reverse %}
    {% for post in selected_posts  %}
    <div class="article-wrapper">
        <article>
            {% include article-header.html page=post link=true share=false eye_catch=false %}
        </article>
    </div>
    <hr class="with-no-margin"/>
    {% endfor %}
</div>
