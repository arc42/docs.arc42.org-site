---
layout: post
title: "Sample Business Context (HTML Sanity Checker)"
tags: context sample 
category: context
permalink: /samples/business-context-1/
---

## 3. Context View

<div class="arc42-help" markdown="1">
Specification of *all* communication partners (users, IT-systems, ...) with explanations of domain specific inputs and outputs or interfaces. 
Optionally you can add domain specific formats or communication protocols.

* **Business Context**: 
Specification of *all* communication partners (users, IT-systems, ...) with explanations of domain specific inputs and outputs or interfaces. 
Optionally you can add domain specific formats or communication protocols.
* **Technical Context** (aka Deployment Context): 
Technical interfaces (channels and transmission media) linking your system to its environment. 
In addition a mapping of domain specific input/output to the channels, i.e. an explanation with I/O uses which channel.

</div>

### 3.1 Sample Business Context 

![Business context]({{ site.imageurl}}/samples/htmlsc/3-hsc-business-context.png)


|Neighbor  |Description |
|------|:-----|
|user         |documents software with toolchain that generates html. Wants to ensure that links within this HTML are valid.     |
|-----|---------|
|build system      |mostly [Gradle](https://gradle.org)                         |
|------|---------|
|local HTML files  |HtmlSC reads and parses local HTML files and performs sanity checks within those.                                |
|------|---------|
|local image files |HtmlSC checks if linked images exist as (local) files.     |
|------|---------|
|external web resources |HtmlSC can be configured to optionally check for the existence of external web resources. 
**Risk**: Due to the nature of web systems and the involved remote network operations, this check might need significant time and might yield invalid results due to network and latency issues.  |