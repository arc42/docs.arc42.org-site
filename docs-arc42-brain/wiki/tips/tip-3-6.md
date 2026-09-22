---
id: 3-6
type: tip
title: 'Tip 3-6: Simplify the context by categorization!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-022-section-3-content]]'
related:
- '[[tip-3-5]]'
- '[[tip-3-7]]'
section: '[[section-3]]'
keywords:
- '[[lean]]'
terms:
- '[[context]]'
- '[[external-interface]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/3-6/
---

Keep the context small and simple: categorize external interfaces, systems or
user roles that have strong similarities. Explicitly show that they are
categories or abstractions.

See the following example - where the context contains only a single "report" interface,
(a "category"), that is broken down into two different types of reports on level-1.

![context abstractions drawing](../assets/sections/03/context-abstractions.webp)

I've seen context diagrams with way more than 50 (!) external neighbours, in which
case categorization is an awesome way to reduce visual clutter and make diagrams
understandable again...
