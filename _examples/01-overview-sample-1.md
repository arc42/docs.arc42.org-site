---
layout: post
title: "Overview Example: HTML Sanity Checker"
tags: overview example 
category: overview
permalink: /examples/overview-example-1/
---

## 1. (example) Introduction 


HtmlSanityCheck (HtmlSC) checks HTML for semantic errors, like broken links and missing images. 
It has been created to support authors who create HTML as output format.

Main goal is to support authors in avoiding errors within their (generated) HTML.


### 1.1 (example) Overview for HTML Sanity Checker

<div class="arc42-example" markdown="1">

You like to briefly explain important goals and requirements, use-cases or features of the system. 
If available, refer to existing requirements documentation.

Most important: Readers can understand the central tasks of the system, before they encounter the architecture of the system (starting with arc42-section 3).
</div>

1. Authors write in formats like [AsciiDoc](https://asciidoctor.org/docs/what-is-asciidoc/), [Markdown](https://www.daringfireball.net/projects/markdown/syntax) or other formats, which are transformed to HTML by corresponding generators.
2. HtmlSC checks the generated HTML for broken links, missing images and other semantic issues.
3. HtmlSC creates a test report, similar to the well-known unit test report (see below).

![HtmlSC goal: Semantic checking of HTML pages]({{ site.imageurl}}/examples/htmlsc/1-1-overview.png)

The overall goal of HtmlSC is to create neat and clear reports, showing errors within HTML files. Below you find a example report.

![example Report]({{ site.exampleimages }}/htmlsc/1-1-example-report.jpg)

HtmlSanityCheck (HtmlSC) checks HTML for semantic errors, like broken links and missing images. 
It has been created to support authors who create HTML as output format.
