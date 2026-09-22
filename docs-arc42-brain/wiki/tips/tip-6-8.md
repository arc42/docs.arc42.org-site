---
id: 6-8
type: tip
title: 'Tip 6-8: Use activity diagrams with partitions to describe or specify runtime
  scenarios!'
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-024-section-6-content]]'
related:
- '[[tip-6-1]]'
- '[[tip-6-7]]'
section: '[[section-6]]'
keywords: []
terms:
- '[[runtime-view]]'
- '[[runtime-scenario]]'
- '[[activity-diagram]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/6-8/
---

Take a look at the following example - which shows the _modularization_ or _partitioning_
of an activity diagram.

![activity diagram with partitions](../assets/sections/06/activity-with-partition.png){:width="40%"}

The diagram above was rendered by PlantUML with the following code:

```PlantUML
@startuml
partition Checker {
  (*)  -> "check input"
    -->If "verbose?" then
  }

  partition Verbalizer {
     -> [Yes] "turn on\n verbosity"
  }

  partition Runner 
   --> "run\n command"


   else
     ->  [no] "run\n command"
     -> "finalize"
   Endif
     ->(*)

@enduml
```
