---
id: 8-9
type: tip
title: 'Tip 8-9: Document decisions instead of concepts!'
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-020-section-8-content]]'
related:
- '[[tip-8-3]]'
section: '[[section-8]]'
keywords:
- '[[lean]]'
terms:
- '[[concept]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/8-9/
---

You can interpret concepts as special cases of architecture and/or design decisions
(see [arc42 section 9](/section-9/)).

```
if (extensive-explanation-required)
   then concept
   else decision
```

Even from a decision (in arc42 section 9) you can refer (or hyperlink) to
the corresponding source code (or even better, appropriate unit tests!). That's
sometimes sufficient for developers...
