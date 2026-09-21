---
id: ISS-021
type: issue
title: Tip 10-2 is marked deprecated but still published
status: open
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-017-section-10-content]]'
related:
- '[[tip-10-2]]'
- '[[tip-10-3]]'
- '[[10-quality-scenario-example-tpu-1]]'
severity: major
kind: question
raised-by: agent
resolved: null
---

**What's unresolved.** [[tip-10-2]]'s title ends in "(deprecated!)" and its first paragraph
withdraws its own advice — yet the tip is on the site, in section 10's tip list, with its
recommendation and its graphic intact. A reader arriving from a search engine or the keyword page
meets a tip that argues against itself. The brain has no state for "published but withdrawn":
`retired` exists, but it takes the URL off the site, and the status ladder has nothing between
`published` and `retired`.

**Affects.** [[tip-10-2]], and by association [[tip-10-3]], which offers the mind-map variant of
the same graphical tree.

**Evidence.** The title: "Tip 10-2: Document and explain the specific quality tree!
(deprecated!)". The body opens with a block quote: "In previous versions of this tip, we proposed
a graphical quality tree. Now, a few years later, we favor a simple table instead of the
graphics." It closes by conceding "If it grows larger, all overview gets lost - and a simple table
will win", and in between still shows the graphical tree image and tells the reader to use a
mindmap version if they are "a mindmap- or graphics fan". The replacement it points to —
`Q42`, the tag-based pragmatic quality model at quality.arc42.org — is the same destination
[[ISS-018-three-tips-overlap-on-the-quality-model|ISS-018]] found three section 1 tips sending
readers to.

**Options.**
1. Rewrite the tip around the current advice (a table), keeping the URL and the history note.
   The tag `quality-tree` stays true, and [[10-quality-scenario-example-tpu-1]] already shows the
   tree *as* a table, so the example is ready.
2. Retire the tip: `status: retired` plus `/tips/10-2/` in `_system/retired-permalinks.txt` with
   this issue as the reason. The first URL the project would ever withdraw, and the numbering
   would then have a hole.
3. Keep it and add a `deprecated` facet the site renders as a banner — needs a keyword, an emitter
   change and a layout change, but it is the honest state and would serve the next such tip too.
4. Leave it.

**Resolution.** Open — and a cut-over blocker for section 10 in the sense that whichever option
wins should land before the URL becomes permanent. Option 2 is the only one that needs the
retired-permalinks mechanism, which has never been exercised; option 3 is the only one that
generalises, and section 10 will not be the last deprecated tip.
