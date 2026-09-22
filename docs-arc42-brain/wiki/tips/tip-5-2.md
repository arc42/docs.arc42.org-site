---
id: 5-2
type: tip
title: 'Tip 5-2: Organize the building block view hierarchically!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[tip-5-3]]'
- '[[tip-5-4]]'
- '[[tip-5-11]]'
- '[[tip-5-27]]'
- '[[05-buildingblock-example-hsc]]'
section: '[[section-5]]'
keywords:
- '[[hierarchy]]'
- '[[source-code]]'
- '[[essential]]'
terms:
- '[[building-block]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/5-2/
---

Explain the structure of your source code as a hierarchy of white- and blackboxes,
starting from the context view (arc42 section 3).

The context shows the complete system as a blackbox, which the building block
view level-1 refines as whitebox.

The diagram below schematically shows this hierarchy:

![hierarchical building block diagram](../assets/sections/05/building-block-hierarchy.webp)

* **Level 1** is the white box description of the overall system together with black box descriptions of all contained building blocks.
* **Level 2** zooms into some building blocks of level 1.
Thus it contains the white box description of selected building blocks of level 1, together with black box descriptions of their internal building blocks.
* **Level 3** zooms into selected building blocks of level 2, and so on.

> In the diagram above, each **rounded rectangle** represents a single whitebox,
which shall be documented by an instance of the whitebox template.
You will not have the hierarchy in a single diagram in your concrete documentation!
