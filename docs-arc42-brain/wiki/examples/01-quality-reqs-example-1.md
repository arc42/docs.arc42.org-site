---
id: 01-quality-reqs-example-1
type: example
title: 'Quality Requirements Example: HTML Sanity Checker'
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-015-section-1-content]]'
related:
- '[[tip-1-12]]'
- '[[tip-1-18]]'
section: '[[section-1#1.2 Quality Goals]]'
system: '[[htmlsc]]'
example-category: qualitygoals
keywords:
- '[[example]]'
terms:
- '[[quality-requirement]]'
- '[[quality-goal]]'
- '[[quality-scenario]]'
legacy-tags: []
permalink: /examples/quality-requirements-1/
---

Some (simple) quality requirements (as scenarios), organized by priority in a table.

## 1.2 (example) Quality Requirements for HTML Sanity Checker


| Priority | Quality Goal |Scenario                                               |
|---|:---|:---|
| 1        | Correctness  |Every broken internal link (cross reference) is found. |
|---|---|---|
| 1        | Correctness  |Every potential semantic error is found and reported. In case of doubt[^doubt], report and let the user decide.  |
|---|---|---|
| 1        | Safety       |Content of the files to be checked is _never_ altered. |
|---|---|---|
| 2        | Flexibility  |Multiple checking algorithms, report formats and clients. At least Gradle and command-line have to be supported.|
|---|---|---|
| 2        | Correctness  |Correctness of every checker is automatically tested for positive AND negative cases.|
|---|---|---|
| 3        | Performance  |Check of 100kB html file performed under 10 secs (excluding Gradle startup)|
|---|---|---|

[^doubt]: Especially when checking external links, the correctness of links depends on external factors, like network availability, latency or server configuration, where HtmlSC cannot always identify the root cause of potential problems.
