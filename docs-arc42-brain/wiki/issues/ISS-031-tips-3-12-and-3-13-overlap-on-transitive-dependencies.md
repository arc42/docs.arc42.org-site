---
id: ISS-031
type: issue
title: Tips 3-12 and 3-13 explain the same figure and largely the same point
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-022-section-3-content]]'
related:
- '[[tip-3-12]]'
- '[[tip-3-13]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** [[tip-3-12]] and [[tip-3-13]] are consecutive tips that embed the *same*
image and explain the *same* two arrows in it. A reader arriving from the section page meets the
figure twice, with the second page adding one sentence the first does not have.

**Affects.** [[tip-3-12]], [[tip-3-13]].

**Evidence.** Both end with `![dependency diagram example](../assets/sections/03/context-different-dependencies.webp)`.
[[tip-3-12]] — "Show external influences in the context!" — lists six kinds of dependency, walks
the figure step by step, and already draws the conclusion: "Steps 3 and 6 are transitive (also
called indirect) dependencies. The system depends on the registry office, even if it doesn't use
it's interface directly." [[tip-3-13]] — "Show transitive dependencies in the context!" — then
says: "The dependencies 3 and 6 as well as the registry office in the upper left corner are
indirect." The same two step numbers, the same registry office, the same figure.

What 3-13 adds, and 3-12 does not have, is the counter-argument: transitive dependencies
"contradict the rule of economicalness … therefore you should only describe them if it is
necessary". That caution is the only content unique to the page, and it sits in tension with
3-12, which presents the transitive steps as something to show without qualification.

**Options.**
1. Merge 3-13's caution into 3-12 as a closing paragraph and retire 3-13. This is the honest
   shape — one figure, one explanation, one caveat — but `/tips/3-13/` is a published URL, so it
   needs an entry in `_system/retired-permalinks.txt` with a reason.
2. Narrow 3-12 to the six *kinds* of dependency and let it stop before the transitive case, so
   that 3-13 owns transitivity and its caveat. Both pages survive, the figure is still shown
   twice, but neither repeats the other's conclusion.
3. Leave them; two short pages cost a reader little.

**Resolution.** Open. The same shape as
[[ISS-008-tips-9-8-and-9-9-overlap-on-timestamps|ISS-008]] and
[[ISS-018-three-tips-overlap-on-the-quality-model|ISS-018]], so this is the third overlapping pair
found by ingest and the first where the two pages also share an image. Option 1 would be the
project's first deliberate retirement of a tip URL, which is why it should be decided before
section 3 is cut over rather than during it.
