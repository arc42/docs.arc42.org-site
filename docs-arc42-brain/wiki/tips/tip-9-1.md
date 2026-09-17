---
id: 9-1
type: tip
title: 'Tip 9-1: Document only architecturally relevant decisions!'
status: review
created: '2026-09-17'
updated: '2026-09-17'
sources:
- '[[SRC-013-section-9-content]]'
related:
- '[[tip-9-2]]'
- '[[tip-9-3]]'
- '[[tip-9-7]]'
- '[[architecture-decision]]'
- '[[quality-requirement]]'
section: '[[section-9#Our proposal concerning decisions]]'
keywords:
- '[[lean]]'
terms:
- '[[architecture-decision]]'
- '[[stakeholder]]'
- '[[quality-requirement]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/9-1/
---

>(document) "architecturally significant" decisions: those that affect the structure, non-functional characteristics, dependencies, interfaces, or construction techniques.
>
>Quoted from <a target="_blank" rel="noopener noreferrer nofollow" href="https://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions">Michael Nygard</a>

Don't document every tiny development decision - but concentrate on the following:


* critical or important for the system
* influencing important quality attributes
* unconventional (“off the beaten track”)
* risky
* with expensive consequences
* with long-lasting effects
* affecting either
   * a large number of stakeholders
   * very special or important stakeholders
* that took a long time or much effort to decide
* astonishing
