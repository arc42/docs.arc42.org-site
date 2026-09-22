---
id: 3-8
type: tip
title: 'Tip 3-8: Aggregate (cluster) similar neighbour systems with ports!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-022-section-3-content]]'
related:
- '[[tip-3-2]]'
- '[[tip-3-7]]'
- '[[tip-3-9]]'
section: '[[section-3]]'
keywords: []
terms:
- '[[context]]'
- '[[port]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/3-8/
---

If your system interacts with many external systems, you could use UML port symbols
at to denote categories (or clusters) of such neighbours,
instead of showing all external systems as separate symbols.

That looks similar to [tip 3-7 (categories of external systems)](/tips/3-7),
but doesn't require the use of stereotypes and might save some drawing effort.

Ports have the great advantage that they connect inside and outside:
You can depict which internal blackbox communicates with which of the external
neighbours.

See the examples below: First you see a context with ports, below you find the more extensive version with ports and explicit neighbour systems.

![](../assets/sections/03/context-with-ports.png)

![](../assets/sections/03/big-context.png)
