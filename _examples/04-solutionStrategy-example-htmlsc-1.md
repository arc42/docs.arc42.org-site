---
layout: post
title: "Example Solution Strategy: HTML Sanity Checker"
tags: solution-strategy example 
category: solutionstrategy
permalink: /examples/solution-strategy-htmlsc-1/
---


<div class="arc42-example" markdown="1">
You need a brief summary and explanation of the fundamental solution ideas and strategies. 
These key ideas should be familiar to everyone involved in development and architecture.

Briefly explain how you achieve the most important quality requirements.
</div>

## 4. Solution Strategy

1. Implement HtmlSC mostly in the Groovy programming language and partially in Java
with minimal external dependencies.
2. We wrap this implementation into a Gradle plugin, so it can be used within
automated builds. Details are given in the
[Gradle userguide](https://docs.gradle.org/current/userguide/userguide.html).
(The Maven plugin is still under development).
3. Apply the [_template-method-pattern_](https://sourcemaking.com/design_patterns/template_method/)
to enable:
  * multiple checking algorithms
  * both HTML (file) and text (console) output
4. Rely on standard Gradle and Groovy conventions for configuration, having a single configuration file.
  * For the Maven plugin, this might lead to problems.

