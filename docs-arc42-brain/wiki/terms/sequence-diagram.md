---
id: sequence-diagram
type: term
title: Sequence diagram
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-024-section-6-content]]'
related:
- '[[activity-diagram]]'
- '[[plantuml]]'
- '[[runtime-view]]'
- '[[runtime-scenario]]'
term: Sequence diagram
aliases:
- UML sequence diagram
legacy-tags:
- sequence-diagram
home: '[[section-6]]'
---

**Definition.** A UML diagram that puts each participant on its own vertical lifeline and draws
the messages between them as arrows, so that time runs down the page and responsibility runs
across it.

**In arc42.** The notation section 6 leans on hardest. [[tip-6-11]] recommends it for runtime
scenarios because it "clearly denote[s] the responsibility of all participating building blocks",
and [[tip-6-1]] gives the reason in the form of a property no other notation on its list has: a
sequence diagram shows the mapping of activities onto [[building-block|building blocks]]
*immediately*, without the reader having to do the assignment themselves. All three section 6
examples use one. The section's advice is then almost entirely about how much to draw:
[[tip-6-3]] keeps the lifelines at level 1, [[tip-6-4]] warns that the notation's original
purpose — concrete instances, method calls, parameters — buys accuracy at a maintenance price
few teams should pay, [[tip-6-6]] cuts the boring middle out, and [[tip-6-10]] mixes participants
of different sizes on one diagram. [[tip-6-9]] and [[plantuml]] answer the cost objection by
generating the diagram from text.

**Distinguish from.** [[activity-diagram]] — the other notation section 6 tags, which groups by
actor through swimlanes rather than by lifeline, and which section 1 also uses for requirements;
a sequence diagram is tagged only in section 6. [[runtime-scenario]] — the scenario is what is
being described; the sequence diagram is one of several forms it can take, and section 6's
*Form* list names five.
