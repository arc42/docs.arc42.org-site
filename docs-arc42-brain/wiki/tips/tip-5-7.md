---
id: 5-7
type: tip
title: 'Tip 5-7: Use tables to efficiently document/specify blackboxes!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[tip-5-1]]'
- '[[tip-5-6]]'
- '[[tip-5-24]]'
- '[[05-buildingblock-example-hsc]]'
section: '[[section-5]]'
keywords:
- '[[table]]'
terms:
- '[[building-block]]'
- '[[blackbox]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/5-7/
---

A simple and efficient way to document or specify blackboxes
are tables, like shown in the following sections.

### Minimal Blackbox Template

|Purpose/Responsibility | &lt;short description of purpose> |
|Interface(s)           | &lt;short description of interface(s)> |

### Full Blackbox Template


|Purpose/Responsibility | &lt;short description of purpose> |
|Interface(s)           | &lt;short description of interface(s)> |
|(optional) Quality-/performance characteristics | &lt;short description or links to quality requirements> |
|(optional) directory/file location | where to find the source code of this blackbox. |
|(optional) Fulfilled requirements| &lt;short description or links to requirements documentation>|
|(optional) Open issues | &lt;list of known problems/risks, links to arc42-section 11>

### Remarks

* Interfaces: describe those only when they are **not** extracted as separate paragraphs.
Interfaces may include qualities and performance characteristics.

* Quality-/performance characteristics might be topics like availability, run time behavior,
flexibility or similar.
* Directory/file location: This might be a single file/directory, or a list of sources making up this blackbox.
* Add fulfilled requirements only if you **really** need traceability. It's expensive and creates huge effort... Think twice.
