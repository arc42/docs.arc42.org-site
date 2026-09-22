---
id: 5-1
type: tip
title: 'Tip 5-1: Use common structures for sections of the building block view!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[tip-5-5]]'
- '[[tip-5-7]]'
- '[[tip-5-8]]'
section: '[[section-5]]'
keywords: []
terms:
- '[[building-block]]'
- '[[blackbox]]'
- '[[whitebox]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/5-1/
---

TODO: insert links to specific tips for black-/whitebox

Regardless on the level-of-detail or abstraction level you're currently
documenting or specifying: Use uniform:

* **whitebox** representations to (graphically) explain structures
and inner workings
* **blackbox** representation to explain responsibiliy and interfaces
of single building blocks


#### Whitebox descriptions

Every whitebox explains the internal structure and internal interfaces
of a "higher-level blackbox", usually by a diagram and some textual explanation.

You might use UML or any box/arrow kind of diagram.

#### Blackbox descriptions

Blackbox descriptions:

* explain responsibilities and interfaces of a building block,
* respect the information-hiding principle, thus avoiding disclosure of internal details
* can be either tabular or graphical


Other [tips in this section](/section-5/) refer to both black- and whiteboxes.
