---
id: 5-5
type: tip
title: 'Tip 5-5: Describe the responsibility or purpose of every (important) blackbox!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[tip-5-1]]'
- '[[tip-5-6]]'
- '[[05-buildingblock-example-tpu-lev-1]]'
section: '[[section-5]]'
keywords:
- '[[essential]]'
terms:
- '[[building-block]]'
- '[[blackbox]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/5-5/
---

Apart from an expressive or meaningful name, a brief description of
its **responsibility** belongs to the really important aspects of the building block view.

* Names can become quite clear if they somehow refer to requirements fulfilled
by the corresponding blackbox.
* Describe "what" the blackbox does or performs, avoid describing the "how".
* Especially in lower levels of the building block hierarchy, single blackboxes
fulfill part of the responsibility of some higher-level building block.
* Keep this description brief and compact, one or two sentences at most. Having
too many "and" in such descriptions can be a sign of a missing abstraction.

>Naming things belongs to the <a target="_blank" rel="noopener noreferrer nofollow" href="https://martinfowler.com/bliki/TwoHardThings.html">two hardest things in Computer Science</a> - apart from cache invalidation and off-by-one-errors.
