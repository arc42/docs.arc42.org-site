---
id: 10-quality-scenario-example-htmlsc-2
type: example
title: 'Example Quality Scenarios: HTML Sanity Checker'
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-017-section-10-content]]'
related:
- '[[tip-10-5]]'
- '[[10-quality-scenario-example-tpu-1]]'
section: '[[section-10]]'
system: '[[htmlsc]]'
example-category: quality
keywords:
- '[[example]]'
terms:
- '[[quality-requirement]]'
legacy-tags: []
permalink: /examples/quality-htmlsc-2/
---

<p></p>


### 10.2 Quality Scenarios 

|ID     |Description                              |
|-------|-----------------------------------------|
|10.2.1 |Every broken internal link will be found. |  
|-------|-----------------------------------------|
|10.2.2 |Every missing (local) image will be found.|
|-------|-----------------------------------------|
|10.2.3 |Correctness of all checks is ensured by automated positive and negative tests. |
|-------|-----------------------------------------|
|10.2.4 |The results-report must contain _all_ results (aka findings) |
|-------|-----------------------------------------|
|10.2.5 |HtmlSC shall be extensible with new checking algorithms and new usage scenarios (i.e. from different build systems) |
|-------|-----------------------------------------|
|10.2.6 |HtmlSC leaves its source files completely intact: Content of files to be checked will _never_ be modified.|
|-------|-----------------------------------------|
|10.2.7 |HtmlSC performs all checks on a 100kByte HTML file in less than 10 seconds.|
|-------|-----------------------------------------|
