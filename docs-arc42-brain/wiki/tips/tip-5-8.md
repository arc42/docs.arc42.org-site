---
id: 5-8
type: tip
title: 'Tip 5-8: Justify every whitebox structure!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[tip-5-1]]'
- '[[tip-5-9]]'
section: '[[section-5]]'
keywords: []
terms:
- '[[building-block]]'
- '[[whitebox]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/5-8/
---

Every whitebox structure is the decomposition of a blackbox into smaller parts
(we call those _contained blackboxes_) plus their mutual dependencies or relationships.

In **every** whitebox you should briefly explain the reasons for the specific
decomposition or structure:

* Why does this whitebox consist of five blackboxes?
* Why does the contained blackbox A talk to B?

This information is sometimes called _design rationale_ for this specific whitebox.
