---
id: 6-4
type: tip
title: 'Tip 6-4: Document detailed scenarios (with caution)!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-024-section-6-content]]'
related:
- '[[tip-6-2]]'
- '[[tip-6-3]]'
- '[[06-runtime-example-tpu-1]]'
section: '[[section-6]]'
keywords:
- '[[thorough]]'
terms:
- '[[runtime-view]]'
- '[[runtime-scenario]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/6-4/
---

This tip contrasts to [tip 6-3 (schematic scenarios)](/tips/6-3).

The original intention of UML sequence diagrams was showing interactions
between concrete _instances_ of classes, with method invocations and parameters,
- the lowest level of detail you can have. In this level, we talk about
the instance 'Homer Simpson' instead of the class `Person`.

The advantages of such details are **thoroughness and accuracy**: You visualize
single executions of source code.

**Please document details with caution - and only if relevant stakeholders really
need them!**

### Heavy disadvantages:

The disadvantage of these details are the immense creation and maintenance effort,
and the potentially low readability of very detailed runtime diagrams.
