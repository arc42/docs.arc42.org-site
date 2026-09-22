---
id: ISS-043
type: issue
title: Section 6 publishes claims that were dated when written and never revisited
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-024-section-6-content]]'
related:
- '[[tip-6-7]]'
- '[[06-runtime-example-htmlsc-1]]'
severity: minor
kind: risk
raised-by: agent
resolved: null
---

**What's unresolved.** Two places in section 6 make a claim that was true at a stated moment and
has not been checked since. Both stamp their own date, so a reader can see they are old; neither
has been revisited in the nine years since.

**Affects.** [[tip-6-7]], [[06-runtime-example-htmlsc-1]].

**Evidence.**

1. [[tip-6-7]] closes with a note on tooling: "PlantUML (as of February 2017) can only render
   vertical swimlanes. Depending on your needs, horizontal swimlanes might be better to
   understand - in wich case you need different tools." The claim is about a third-party tool
   that the same section recommends four times, and it is the only capability limit section 6
   asserts about it. Whether it still holds needs checking against PlantUML rather than guessing.
2. [[06-runtime-example-htmlsc-1]] lists as step 5 of its main loop: "(planned) get all available
   Checker classes based upon annotation". The figure beside it — `6-main-loop.png` — already
   draws that step as `allCeckers = CheckerFactory.getAllCheckersByAnnotation`, with no marking
   that it is planned. So the prose and the figure disagree about whether the step exists, and
   HTML Sanity Checker is a live project whose actual answer is a lookup away. (The figure also
   spells the variable `allCeckers`; correcting it means re-rendering the diagram, which is why it
   is noted here rather than with the typos in
   [[ISS-039-section-6-bodies-carry-editorial-defects|ISS-039]].)

**Options.**
1. Check both against their sources and rewrite: for [[tip-6-7]], either drop the date because the
   limit still holds, or drop the claim because it does not; for the example, either implement-or-
   remove the "(planned)" marker to match the current HtmlSC, or mark it in the figure too.
2. Leave the dates in place. They are honest — a reader can see the vintage — and the tips' actual
   advice does not depend on either claim.
3. Treat it as the first instance of a general sweep: every "as of <date>" and "(planned)" in the
   site, checked once.

**Resolution.** Open. Neither claim affects the advice, so neither blocks section 6's cut-over.
Option 3 is the one worth weighing, because this is the kind of finding the per-section ingests
cannot size: the twelve sections are now all read, and a single grep for dated claims would say
whether section 6 is unusual or typical.
