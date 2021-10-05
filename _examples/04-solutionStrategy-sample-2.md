---
layout: post
title: "Example Solution Strategy: MaMa"
tags: solution-strategy example 
category: solutionstrategy
permalink: /examples/solution-strategy-2/
---

<div class="arc42-example">
You need a brief summary and explanation of the fundamental solution ideas and strategies. 
These key ideas should be familiar to everyone involved in development and architecture.

Briefly explain how you achieve the most important quality requirements.
</div>

## 4. Solution Strategy 

Please note: 

* In _real life_ you would include links to detailed descriptions - that's omitted in this example.
* In this example, the approaches are centered around specific requirements. 
That is not necessary - certain stragic approaches in your system might be quite general and not related to specific requirements.

|Goal/Requirement    |Architectural Approach                  |Details        |
|--------------------|----------------------------------------|---------------|
|Flexible Data Structure |Database structure + persistence code is completely (100%) generated from UML-model | |
|Flexibility in Transmission Formats (CSV and fix-record-formats |Create domain-specific languages for CSV and fix-format import/export configurations. Build an ANTLR based parser for these languages plus the corresponding interpreters. | Section 8.2 |
|Flexibility (Configurable CSV/fix formats) |Implement customized editor for CSV/fix DSL as Eclipse plugin |Section 8.2 |
|Performance (import/process 250k images/24hrs) |Treat images as special case, store images in filesystem instead of database, create unique path/filename based upon cient-ID, include load-testing in automatic build, create test-data generator |Include special case for image persistence in code generator, Section 8.1 |
