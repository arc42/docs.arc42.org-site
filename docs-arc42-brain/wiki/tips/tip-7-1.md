---
id: 7-1
type: tip
title: 'Tip 7-1: Document your technical infrastructure (hardware)!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-021-section-7-content]]'
related:
- '[[tip-7-3]]'
- '[[tip-7-8]]'
- '[[tip-7-10]]'
- '[[07-deployment-example-tpu-1]]'
section: '[[section-7]]'
keywords: []
terms:
- '[[deployment-view]]'
- '[[hardware]]'
- '[[infrastructure]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/7-1/
---

Describe the technical infrastructure (aka the underlying hardware) the
system is running in. That shall include:

* nodes, i.e. processors, server, cluster... and their
* relations (channels), i.e. bus, network or wireless connections,
* additional hardware elements, i.e. firewall, router, switches, storage etc.

You could either use UML deployment diagrams or free-form graphics, like shown below:

![free-form graphic to describe technical infrastructure](../assets/sections/07/infrastructure-with-symbols.png)
(diagram by <a target="_blank" rel="noopener noreferrer nofollow" href="https://www.uml-diagrams.org/examples/web-application-network-diagram-example.html?context=depl-examples">UML-diagrams.org</a>)

In case your stakeholder like such graphical icons or symbols: use a consistent
set of such symbols with a _defined_ semantic!

### Delegate hardware documentation

Try to delegate the hardware and infrastructure documentation to the appropriate
stakeholders.
