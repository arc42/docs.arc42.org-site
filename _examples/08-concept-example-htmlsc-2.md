---
layout: post
title: "Example Concept: HTML Sanity Checker (Multiple Checking Algorithms)"
tags: concept example 
category: concepts
permalink: /examples/concept-htmlsc-2/
---

<p></p>


## 8. Crosscutting Concepts



### 8.3 Multiple Checking algorithms
HtmlSC uses the <a target="_blank" rel="noopener noreferrer nofollow" href="https://sourcemaking.com/design_patterns/template_method/">template-method-pattern</a>
to enable flexible checking algorithms:

> >"The Template Method defines a _skeleton of an algorithm_ in an operation, and defers some steps to subclasses".

We achieve that by defining the skeleton of the checking algorithm in one operation (`performCheck`), deferring the specific checking algorithm steps to subclasses. The invariant steps are implemented in the abstract base class, while the variant checking algorithms have to be provided by the subclasses.


~~~~
/**
  * Prerequisite: pageToCheck has been successfully parsed,
  * prior to constructing this Checker instance.
**/
public CheckingResultsCollector performCheck() {
    // assert prerequisite
    assert pageToCheck != null
    initResults()
    return check() // subclass executes the actual checking algorithm
}
~~~~

![Template Method (excerpt)]({{ site.imageurl }}/examples/htmlsc/8-3-template-method.png)

|Component         | Description |
|------|:------|
| Checker   | _abstract_ base class, containing the template method `check()` plus the public method `performCheck()` |
|------|------|
| `ImageFileExistChecker` | checks if referenced local image files exist |
|------|------|
| `InternalLinksChecker`    | checks if cross references (links referenced within the page) exist |
|------|------|
| `DuplicateIdChecker`        | checks if any id has multiple definitions |
|------|------|

