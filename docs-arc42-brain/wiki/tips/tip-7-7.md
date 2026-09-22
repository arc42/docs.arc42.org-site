---
id: 7-7
type: tip
title: 'Tip 7-7: Use tables to document software/hardware mapping!!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-021-section-7-content]]'
related:
- '[[tip-7-5]]'
- '[[tip-7-6]]'
- '[[07-deployment-sample-htmlsc-1]]'
section: '[[section-7]]'
keywords:
- '[[lean]]'
terms:
- '[[deployment-view]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/7-7/
---

As a (simple) alternative to graphical mapping with deployment
diagrams (see [tip 7-6 (deployment diagrams)](/tips/7-6)), you could
use tables to document or specify deployment of software on hardware.

|Server| Artifact |Remark|
|------|-----------|-----|
|OneServer| |A docker container, requiring at least Docker V 12.1 |
| |DomainServices |auto-deployed by Gradle build script|
| | | |
|OtherServer | |Dell(c) Server, Quad-Core i7 CPU, 64GB RAM, running RH Enterprise Linux |
| |Articles |Unix executable, build by make, executed via cron |
| |FooBar |Java jar, build, deployed and executed via Gradle build script  |
| |CassandraDB |Open source database, started via cron |

Please find the corresponding diagram below:


![deployment diagram](../assets/sections/07/deployment-diagram.png){:width="60%"}
