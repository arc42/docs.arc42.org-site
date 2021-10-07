---
layout: post
title: "Quality Requirements Example: HTML Sanity Checker"
tags: quality-requirements example 
category: quality-goals
permalink: /examples/quality-requirements-1/
---

<div class="arc42-example">
This example has been created with Enterprise Architect(TM) as a data flow diagram.
</div>


### 1.2 (example) Quality Requirements for HTML Sanity Checker


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