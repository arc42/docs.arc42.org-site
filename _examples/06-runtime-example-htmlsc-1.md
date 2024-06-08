---
layout: post
title: "Example Runtime View: HTML Sanity Checker"
tags: runtime example 
category: runtime
permalink: /examples/runtime-1/
---


<div class="arc42-example">
<br>
A simple diagram with a brief textual explanation.
</div>

## 6. Runtime View 

### 6.1 Execute all checks
A typical scenario within HtmlSC is the execution of _all_ available checking algorithms on a set of HTML pages.

![Main Loop]({{ site.imageurl}}/examples/htmlsc/6-main-loop.png)

**Explanation:**

0. User or build calls `htmlSanityCheck` build target.
1. Gradle (from within build) calls `sanityCheckHtml`
2. HSC configures input files and output directory
2. HSC creates an `AllChecksRunner` instance
3. gets all configured files into `allFiles`
4. (planned) get all available Checker classes based upon annotation
5. perform the checks, collecting the results


### 6.2 Report checking results

![Sequence diagram: Report results]({{ site.imageurl}}/examples/htmlsc/6-2-1-report-results.png)

Reporting is done in the natural hierarchy of results (see the corresponding concept in section 8.2.1 for an example report).

1. per "run" (`PerRunResults`): date/time of this run, files checked, some configuration info, summary of results
2. per "page" (`SinglePageResults`):
  1. create page result header with summary of page name and results
  2. for each check performed on this page create a section with `SingleCheckResults`
  3. per "single check on this page" report the results for this particular check
