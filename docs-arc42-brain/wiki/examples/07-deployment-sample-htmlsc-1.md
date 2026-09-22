---
id: 07-deployment-sample-htmlsc-1
type: example
title: 'Example Deployment View: HTML Sanity Checker'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-021-section-7-content]]'
related:
- '[[tip-7-7]]'
section: '[[section-7]]'
system: '[[htmlsc]]'
example-category: deployment
keywords:
- '[[example]]'
terms:
- '[[deployment-view]]'
legacy-tags: []
permalink: /examples/deployment-htmlsc-1/
---

<p></p>


## 7. Deployment View

![HTML Sanity Checker Deployment Overview](../assets/examples/htmlsc/7_1-deployment.png)


|Node / Artifact    | Description                                                |
|-------------------|------------------------------------------------------------|
|hsc plugin binary  |Compiled version of HtmlSC, including required dependencies.|
|-------------------|------------------------------------------------------------|
|hsc-development    |Development environment                                     |
|-------------------|------------------------------------------------------------|
|artifact repository|Global public _cloud_ repository for binary artifacts, similar to [mavenCentral](https://mvnrepository.com/) HtmlSC binaries are uploaded to this server.   |
|-------------------|------------------------------------------------------------|
|hsc user computer  |Where documentation is created and compiled to HTML.      |
|-------------------|------------------------------------------------------------|
|build.gradle       |Gradle build script configuring (among other things) the HtmlSC plugin. |
|-------------------|------------------------------------------------------------|

The three nodes (_computers_) shown in the diagram above are connected via Internet.

**Prerequisites**:

* HtmlSC developers need a Java development kit, Groovy, Gradle plus the JSoup
HTML parser.
* HtmlSC users need a Java runtime (> 1.6) plus a build file named `build.gradle`.
(within this documentation example we omitted the listing of the build script).
