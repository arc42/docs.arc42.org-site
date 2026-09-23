---
id: 6-3
type: tip
title: 'Tip 6-3: Document ''schematic'' (instead of detailed) scenarios!'
status: published
created: '2026-09-22'
updated: '2026-09-23'
sources:
- '[[SRC-024-section-6-content]]'
related:
- '[[tip-6-2]]'
- '[[tip-6-4]]'
- '[[tip-6-10]]'
section: '[[section-6]]'
keywords:
- '[[lean]]'
terms:
- '[[runtime-view]]'
- '[[runtime-scenario]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/6-3/
---

A 'schematic' overview of a certain process, activity or function is often
sufficient to understand the interaction between different building blocks
of the system.

Especially developers tend to look for details in source code anyhow, so
they don't need very detailed diagrams.

In 'schematic' scenarios you refer to higher levels of abstraction, to
building blocks from higher levels (e.g. level-1) of the building block view.

In the following scenario only building-blocks from level-1 of the
corresponding building block view interact.

![schematic sequence diagram](../assets/sections/07/schematic-sequence.png)

#### Building Block Level-1 for the Example:

![level 1 for schematic sequence diagram ](../assets/sections/07/level-1-for-schematic-sequence.png)
