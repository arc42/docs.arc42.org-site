---
id: ISS-008
type: issue
title: Tip 9-8 is contained in the quotation of tip 9-9
status: open
created: '2026-09-17'
updated: '2026-09-17'
sources:
- '[[SRC-013-section-9-content]]'
related:
- '[[tip-9-8]]'
- '[[tip-9-9]]'
severity: minor
kind: question
raised-by: agent
resolved: null
---

**What's unresolved.** Tip 9-8 ("Decisions should have a timestamp!") makes exactly the point that
one of the four bullets quoted in tip 9-9 makes. Two tips two weeks apart say the same thing; a
reader who follows the "suggestions for good ADRs" gets the timestamp advice twice.

**Affects.** [[tip-9-8]], [[tip-9-9]].

**Evidence.** Tip 9-8 (2022-01-14): "decisions (e.g. ADRs) should contain a timestamp attribute.
In the future it might be important to know at what time a certain decision was taken." Tip 9-9
(2022-01-28) quotes: "Timestamps: Identify when each item in the ADR is written. This is especially
important for aspects that may change over time".

**Options.**
1. Keep both — tip 9-8 credits a contributor (Nikolai Alex) and stands on its own; the overlap is
   harmless reinforcement. The two are now linked in `related`.
2. Merge tip 9-8 into tip 9-9 — shorter list, but the permalink `/tips/9-8/` would have to be
   retired and the contribution credit moved.

**Resolution.** Open; option 1 is the state on disk.
