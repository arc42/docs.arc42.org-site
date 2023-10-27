---
layout: post
title: "Example Building Block View: HTML Sanity Checker"
tags: buildingblock example 
category: building-block
permalink: /examples/buildingblock-hsc/
---


<div class="arc42-example" markdown="1">
This example contains several levels of the building block view - ranging from the overview level-1 down to very specific and low-level-3.
</div>


### 5.1 Whitebox HtmlSanityChecker

![Whitebox (HtmlSC)]({{ site.imageurl}}/examples/htmlsc/5-whitebox-hsc-level-1.png)


**Rationale:** We used _functional decomposition_ to separate responsibilities:

* `HSC Core` shall encapsulate checking logic and HTML parsing/processing.
* `Plugins` and `GraphicalUI` encapsulate all _usage_ aspects


**Contained Blackboxes:**


|Building block | Description    |
|-------|:------|
| [`HSC Core`](#521-hsc-core-whitebox)   |HTML parsing and sanity checking |
|-------|------|
| `HSC Gradle Plugin` |Exposes HtmlSC via a standard Gradle plugin, as described in the [Gradle user guide](https://docs.gradle.org/current/userguide/userguide.html). Source: Package `org.aim42.htmlsanitycheck`, classes: `HtmlSanityCheckPlugin` and `HtmlSanityCheckTask`
|-------|------|
| `NetUtil`    |package `org.aim42.inet`, checks for internet connectivity, configuration of http status codes     |
|-------|------|
| `FileUtil`  |package `org.aim42.filesystem`, file extensions etc. |
|-------|------|
| HSC Graphical UI   |(planned, not implemented)                      |
|-------|------|


### 5.2 Building Blocks - Level 2



#### 5.2.1 HSC Core (Whitebox)


![HSC-Core (Whitebox)]({{ site.imageurl}}/examples/htmlsc/5-2-1-hsc-core.png)


**Rationale:**
The internal structure of `HSC Core` follows a functional decomposition:
  * configuration,
  * parsing and handling HTML input,
  * checking,
  * creating suggestions and
  * collecting checking results


**Contained Blackboxes:**


|Building block  |Description                                           |
|---------|:--------|
|`Checker`        |Contains the pure checking functionality.  See its [blackbox description](#checker-blackbox) below.  |
|---------|--------|
|`AllChecksRunner`  |Facade to the Checkers. Provides a (configurable) interface. Source: `org.aim42.htmlsanitycheck.AllChecksRunner`. Called by `HSC GradlePlugin` |
|---------|--------|
|`Configuration`| Handles configuration of input and output location, timeouts, status-code behavior and types of checks to be performed.  |
|---------|--------|
|`Reporter`       |Reports checking results to either console or file.   |
|---------|--------|
|`Suggester`      |In case of checking issues, suggests alternatives (_did you mean xyz?_). Suggestions are included in  results.   |       
|---------|--------|



##### 5.2.1.1 Checker (Blackbox)

The abstract class `Checker` provides the uniform interface (`public void check()`) to different checking algorithms.

Based upon polymorphism, the actual checking is handled by subclasses of the abstract `Checker`class, uses the template-method pattern. It uses the
[concept of extensible checking algorithms](#section-ii-8-checking-algorithm).

##### 5.2.1.2 Suggester (Blackbox)
For a given input (_target_), `Suggester` searches within a set of possible values (_options_) to find the n most similar values. For example:

*	Target = "McDown"
*	Options = {"McUp", "McDon", "Mickey"}
* The resulting suggestion would be "McDon", because it has the greatest similarity to the target "McDown".

The implementation is based upon the <a target="_blank" rel="noopener noreferrer nofollow" href="https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance">Jaro-Winkler distance</a>, one of the algorithms to calculate similarity between strings.


`Suggester` is used in the following cases:

* Broken image links: Compares the name of the missing image with all available image file names to find the closest match.
* Missing cross references (broken internal links): Compares the broken link with all available link targets (anchors).

Source: `package org.aim42.htmlsanitycheck.suggest.Suggester`


### 5.3 Building Blocks - Level 3

#### 5.3.1 ResultsCollector (Whitebox)


![Results Collector (Whitebox)]({{ site.imageurl}}/examples/htmlsc/5-3-results-collector.png)

**Rationale:** This structures follows the hierarchy of checks, managing results for:

1. a number of pages/documents (`PerRunResults`),
2. a single HTML page (`SinglePageResults`) and finally
3. the results of a single check, e.g. the `MissingImagesChecker` (`SingleCheckResults`).


**Contained Blackboxes:**


|Building block   |Description                                           |
|---------|:--------|
|`Per-Run Results`|Aggregated results for potentially many HTML pages/documents.    |
|---------|--------|
|`SinglePageResults`|Aggregated results for a single HTML page|
|---------|--------|
|`SingleCheckResults`|Results for a single type of check (e.g. missing-images check or broken-internal-link check) |
|---------|--------|
|`Finding`        |A single finding, (e.g. "image 'logo.png' missing"). Can contain suggestions. |
|---------|--------|
