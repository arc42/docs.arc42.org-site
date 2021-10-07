---
layout: post
title: "Example Building Block View Level-1: HTML Sanity Checker"
tags: buildingblock example 
category: building-block
permalink: /examples/buildingblock-1/
---


### 5.1 Whitebox HtmlSanityChecker

![Whitebox (HtmlSC)]({{ site.imageurl}}/examples/htmlsc/5-whitebox-hsc-level-1.png)


**Rationale:** We used _functional decomposition_ to separate responsibilities:

* `HSC Core` shall encapsulate checking logic and HTML parsing/processing.
* `Plugins` and `GraphicalUI` encapsulate all _usage_ aspects


**Contained Blackboxes:**


|Building block | Description    |
|-------|:------|
| `HSC Core`   |HTML parsing and sanity checking |
|-------|------|
| `HSC Gradle Plugin` |Exposes HtmlSC via a standard Gradle plugin, as described in the [Gradle user guide](https://docs.gradle.org/current/userguide/userguide.html). Source: Package `org.aim42.htmlsanitycheck`, classes: `HtmlSanityCheckPlugin` and `HtmlSanityCheckTask`
|-------|------|
| `NetUtil`    |package `org.aim42.inet`, checks for internet connectivity, configuration of http status codes     |
|-------|------|
| `FileUtil`  |package `org.aim42.filesystem`, file extensions etc. |
|-------|------|
| HSC Graphical UI   |(planned, not implemented)                      |
|-------|------|
