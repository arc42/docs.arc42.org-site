---
id: 7-3
type: tip
title: 'Tip 7-3: Document the various environments!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-021-section-7-content]]'
related:
- '[[tip-7-1]]'
- '[[tip-7-4]]'
- '[[tip-7-9]]'
section: '[[section-7]]'
keywords: []
terms:
- '[[deployment-view]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/7-3/
---

In case the system is developed, tested and operated in different hardware
environments (i.e. DEV for development, CI for build/integration,
  TEST for system and manual tests and PROD for production), you should
  document these environments plus possible differences between them.

The stereotype &laquo;executionEnvironment&raquo; symbolizes such environments.
The little "infinity" symbol in the lower right corner (i.e. in Development)
means there is a refined diagram available (that "infinity" symbol is a speciality
of Sparx EnterpriseArchitect&reg;).

![deployment overview](../assets/sections/07/deployment-overview.png)
