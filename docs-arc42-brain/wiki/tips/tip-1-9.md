---
id: 1-9
type: tip
title: 'Tip 1-9: Use (semi) formal text to describe functional requirements!'
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-015-section-1-content]]'
related:
- '[[tip-1-6]]'
- '[[tip-1-8]]'
section: '[[section-1#1.1 Requirements Overview]]'
keywords:
- '[[notation]]'
- '[[tooling]]'
terms:
- '[[requirement]]'
- '[[functional-requirement]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/1-9/
---

It might be useful to document some important functions, processes or features
in a semi-formal notation.


Consider the open-source PlantUML (https://plantuml.com/) as an example.
Given the following activity description, it can create a graphical version:

```PlantUML
@startuml
start
  :authenticate;

  :select product;

  if (private customer?) then (yes)
    :add\nVAT;
  else (no)
    :request\nVAT_ID;
  endif

  :create invoice;
stop

@enduml
```

Activities are described between: and;, branches can be read as pseudo code and
that way you combine the benefits of plain text with graphical representation.

PlantUML renders the code above to the following diagram:

![](../assets/sections/01/simple-activity.png){:width="40%"}
