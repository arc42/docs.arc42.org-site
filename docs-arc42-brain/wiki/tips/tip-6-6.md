---
id: 6-6
type: tip
title: 'Tip 6-6: Describe excerpts of scenarios (partial scenarios)!'
status: published
created: '2026-09-22'
updated: '2026-09-23'
sources:
- '[[SRC-024-section-6-content]]'
related:
- '[[tip-6-5]]'
- '[[tip-6-11]]'
- '[[06-runtime-example-mama-2]]'
section: '[[section-6]]'
keywords: []
terms:
- '[[runtime-view]]'
- '[[runtime-scenario]]'
- '[[sequence-diagram]]'
legacy-tags: []
date: '2016-03-01'
permalink: /tips/6-6/
---

We have seen too many sequence diagrams resembling the one below: Scenarios that
just propagate date over several participants - usually non-interesting stuff.


![boring sequence diagram](../assets/sections/06/long-and-mostly-boring.png){:width="40%"}


## More effective: Partial scenarios

Describe only excerpts or parts of such scenarios.

* Focus on risky, difficult, complicated or interesting parts.
* Don't hesitate to start right in the middle of a longer (overall) process
* Cut out boring, standard, simple of straightforward stuff

Compare the (compact) diagram below with the (boring and much longer) version above.


![(partial) sequence diagram](../assets/sections/06/short-and-interesting.png){:width="30%"}


Btw: both diagrams were generated from a PlantUML textual description, the code for
the latter is given below:

```PlantUML
@startuml
note right of F: before start, a1-a5 have completed
F -> G : start
G -> G : init
G -> H : create()
G <--H : X
G -> I : authorize( X )
I -> L : check(X)
I <--H : ok
G -> I : foo(X, H)
I --> G : completed
note right of G: G return result to A

@enduml
```
