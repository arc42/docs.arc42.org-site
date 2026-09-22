---
id: 3-7
type: tip
title: 'Tip 3-7:  If many external systems are involved, aggregate (cluster) them
  by explicit criteria!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-022-section-3-content]]'
related:
- '[[tip-3-6]]'
- '[[tip-3-8]]'
- '[[tip-3-9]]'
section: '[[section-3]]'
keywords: []
terms:
- '[[context]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/3-7/
---

If your system interacts with many external systems, you can combine several of
these external systems by explicit criteria. You should explicitly state these
criteria. Such criteria may include systems:

* share common or similar data
* communicate within the same use case or at the same time
* communicate using identical or similar technologies (e.g. categorized by ftp- and WebService)
* belong to the same or similar organization, such as: all systems of garages, insurances, glass manufacturing and tax advisors
* have similar domain or technical tasks to solve (all systems printing documents, dealing with chip cards, etc.)

## Examples: With and without
The following diagram (the detailed version) shows three specific neighbour
systems, all stereotyped with the category << logistics >>.


![extensive context diagram](../assets/sections/03/context-extensive.png)

The next diagram groups these neighbours into one single "Logistics" external system
on the left, stereotyped as << category >>.


![compact context diagram](../assets/sections/03/context-compact.png)
