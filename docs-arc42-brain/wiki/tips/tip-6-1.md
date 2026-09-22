---
id: 6-1
type: tip
title: 'Tip 6-1: Always map existing building blocks to the activities within runtime
  scenarios!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-024-section-6-content]]'
related:
- '[[tip-6-11]]'
- '[[tip-6-7]]'
- '[[tip-6-8]]'
- '[[tip-6-10]]'
- '[[06-runtime-example-tpu-1]]'
section: '[[section-6]]'
keywords:
- '[[essential]]'
terms:
- '[[runtime-view]]'
- '[[runtime-scenario]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/6-1/
---

Runtime scenarios show (document or specify) the interaction of building blocks
or their instances. You should always use elements from your
[building block view](/section-5)
(or their runtime counterparts, like instances of classes) within these
scenarios. They describe _how the system fulfills certain responsibilities_ or tasks,
what building blocks are involved.

Please contrast those runtime scenarios with _required functions_: Those
describe a required process or sequence of steps that the system somehow needs
to execute or perform (but regardless what element of the systems actually does it).

It's an important architecture task to map from the latter (requirements) to
the building blocks. In other words: You need to assign responsibilities to
your building blocks.

For this mapping you have several options:

* UML sequence diagrams, which immediately show the mapping of activities to
building blocks (see [tip (sequence diagrams)](/tips/6-11)).
* Activity diagrams or flowcharts with _swimlanes_ showing this mapping.
* Textual descriptions or numbered lists: There you have to manually care for the
mapping...
