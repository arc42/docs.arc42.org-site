---
id: ISS-040
type: issue
title: Tips 6-6 and 6-11 publish the same figure and the same PlantUML listing
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-024-section-6-content]]'
related:
- '[[tip-6-6]]'
- '[[tip-6-11]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** [[tip-6-6]] and [[tip-6-11]] embed the same image and then reprint the
same twelve-line PlantUML listing, character for character. Two of the section's eleven tips are
therefore carrying one example between them, and a reader who follows the section's own
cross-references meets it twice.

**Affects.** [[tip-6-6]], [[tip-6-11]].

**Evidence.** Both pages end with
`![…](../assets/sections/06/short-and-interesting.png){:width="30%"}` and a fenced `PlantUML`
block beginning `note right of F: before start, a1-a5 have completed` and ending
`note right of G: G return result to A`. Diffing the two listings finds no difference.

The pages do make different points. [[tip-6-6]] — "Describe excerpts of scenarios (partial
scenarios)" — shows the figure as the *short* half of a before-and-after pair, against
`long-and-mostly-boring.png`, and its argument is about what to leave out. [[tip-6-11]] — "Use
sequence diagrams to describe or specify runtime scenarios" — shows the same figure as a
specimen of the notation, and its argument is that sequence diagrams make responsibility legible.
The listing is reprinted on 6-11 for a third reason again: to show that the figure was generated
from text.

So this is not the duplication of
[[ISS-031-tips-3-12-and-3-13-overlap-on-transitive-dependencies|ISS-031]], where
two tips explain the same figure to make the same point. Here the overlap is the *asset*, not the
argument. The cost is that a defect in the listing has to be fixed twice — see
[[ISS-041-the-sequence-diagram-on-tips-6-6-and-6-11-contradicts-itself|ISS-041]], which is exactly
that.

**Options.**
1. Keep both figures, but print the listing once — on [[tip-6-11]], where the point is that the
   diagram came from text — and have [[tip-6-6]] link to it. One copy to maintain, both arguments
   intact.
2. Give [[tip-6-11]] a sequence diagram of its own, so the notation tip is not illustrated by the
   partial-scenario tip's figure. More work, and the new diagram would have to earn its place.
3. Leave both. The pages are short and the repetition is cheap for a reader arriving at only one.

**Resolution.** Open. Unlike [[ISS-031-tips-3-12-and-3-13-overlap-on-transitive-dependencies|ISS-031]]
this needs no URL retirement — both tips have their own point and both should survive — so it can
be decided independently of section 6's cut-over. Option 1 should be decided together with
[[ISS-041-the-sequence-diagram-on-tips-6-6-and-6-11-contradicts-itself|ISS-041]]: fixing the
listing once is a reason to have only one copy of it.
