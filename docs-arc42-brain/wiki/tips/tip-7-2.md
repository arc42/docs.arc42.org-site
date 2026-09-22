---
id: 7-2
type: tip
title: 'Tip 7-2: Explain hardware and infrastructure decisions!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-021-section-7-content]]'
related:
- '[[tip-7-8]]'
section: '[[section-7]]'
keywords: []
terms:
- '[[deployment-view]]'
- '[[hardware]]'
- '[[architecture-decision]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/7-2/
---

Deployment- or infrastructure diagrams support overall understanding of the underlying hardware.

In addition to this overview it is useful to understand the reasoning behind the hardware
decisions, the selection of specific machines, processors or other devices.

If hardware plays an important role in the architecture, you can even use a node-template
for that purpose, similar to the following table:

#### Node &lt;node-name>

|Responsibility| what is the role of this hardware element, what's it doing? |
|(technical) characteristics| i.e. nr of cpus/cores, memory, throughput, nr-of-ports, vendor, model... |
|associated building blocks | what part of the software is running on this hardware? |
|reason for selection | why was this particular hardware selected? |
