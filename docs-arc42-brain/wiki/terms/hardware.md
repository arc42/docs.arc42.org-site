---
id: hardware
type: term
title: Hardware
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-021-section-7-content]]'
related:
- '[[infrastructure]]'
- '[[deployment-view]]'
term: Hardware
aliases: []
legacy-tags:
- hardware
home: '[[section-7]]'
---

**Definition.** The physical elements a system runs on — processors, servers, boards, devices and
the machines between them.

**In arc42.** arc42 treats hardware as part of the architecture wherever it constrains or explains
it, and as somebody else's document wherever it does not. [[tip-7-2]] wants the *reasoning* behind
the hardware written down, not just the diagram, and offers a node template whose last row is
"reason for selection". [[tip-7-8]] asks for the few nodes that carry special meaning to be
explained rather than merely drawn. [[tip-7-10]] draws the boundary from the other side: where
other people own the infrastructure, include only what is needed to understand the architecture
decisions — and [[tip-7-1]] says the same in one line, "try to delegate the hardware and
infrastructure documentation to the appropriate stakeholders".

**Distinguish from.** [[infrastructure]] — the wider term, which also covers environments,
networks and middleware. The site tags both on [[tip-7-1]], which is the tip that names them
together: "the technical infrastructure (aka the underlying hardware)".
