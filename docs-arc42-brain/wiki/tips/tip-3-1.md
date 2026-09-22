---
id: 3-1
type: tip
title: 'Tip 3-1: Explicitly demarcate your system from its environment!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-022-section-3-content]]'
related:
- '[[tip-3-2]]'
- '[[tip-3-9]]'
section: '[[section-3]]'
keywords: []
terms:
- '[[context]]'
- '[[external-interface]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/3-1/
---

Define "what's inside" your system and what's outside.

You should demarcate your system from other IT systems in order to show how it
fits into the existing IT environment, which external interfaces are offered or consumed
and what users or roles are using the system.

That way you show the scope of your system: what are the responsibilities
of your system and what are the responsibilities of its neighbor systems.

You find an example in the diagram below: It shows the context of a webshop which delegates the payment handling to an external provider (removing this
responsibility from the scope of the webshop).

![](../assets/sections/03/simple-context.png){:width="70%"}
