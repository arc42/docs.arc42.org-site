---
id: 5-9
type: tip
title: 'Tip 5-9: Use runtime views to explain or specify whiteboxes!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[tip-5-8]]'
section: '[[section-5]]'
keywords: []
terms:
- '[[building-block]]'
- '[[whitebox]]'
- '[[runtime-view]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/5-9/
---

In case you want to influence the internal structure of a whitebox,
but don't want to specify all details, you may apply techniques
from the runtime view:

Describe the required (runtime) behavior of the whitebox, for example
with:

* pseudo-code
* activity diagrams or flowcharts
* state diagrams or state-machines

Such information provides architects or developers with _some_ information
_how_ this whitebox should be constructed or build, but does not specify
all contained details.
