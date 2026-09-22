---
id: ISS-041
type: issue
title: The sequence diagram published on tips 6-6 and 6-11 contradicts itself
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-024-section-6-content]]'
related:
- '[[tip-6-5]]'
- '[[tip-6-6]]'
- '[[tip-6-11]]'
- '[[sequence-diagram]]'
severity: major
kind: contradiction
raised-by: agent
resolved: null
---

**What's unresolved.** The sequence diagram that [[tip-6-6]] and [[tip-6-11]] both publish shows a
call to a participant that never answers and an answer from a participant that was never called.
It is the section's specimen of the notation whose whole claim — [[tip-6-11]]'s own words — is
that it "clearly denote[s] the responsibility of all participating building blocks".

**Affects.** [[tip-6-6]], [[tip-6-11]], and by contrast [[tip-6-5]].

**Evidence.** The listing, identical on both pages
([[ISS-040-tips-6-6-and-6-11-publish-the-same-figure-and-listing|ISS-040]]), reads in part:

```
G -> I : authorize( X )
I -> L : check(X)
I <--H : ok
```

`I` calls `L`, and the reply arrives from `H`. The rendered figure
(`assets/sections/06/short-and-interesting.png`) draws it faithfully: `L`'s lifeline receives
`check(X)` and sends nothing back, `H`'s lifeline sends `ok` without having been called, and `F`,
who sent `start` on the first line, never receives a result.

The listing on [[tip-6-5]] is the same sketch one participant shorter, and it is *consistent*:

```
G -> I : blabla( X )
I -> H : check( X )
I <--H : ok
```

So the defect is an edit: `H` was renamed to `L` on the call line and not on the reply line. The
same edit introduced `L` as a fifth lifeline that does nothing else.

A second, smaller inconsistency rides along on both pages: the closing note says "G return result
to A", and there is no `A` — not in this listing and not in [[tip-6-5]]'s. The diagram's
participants are `F`, `G`, `H`, `I` and `L`.

**Options.**
1. Change `I -> L : check(X)` to `I -> H : check(X)` and drop `L`, matching [[tip-6-5]]. The
   smallest fix, and it restores the property the tip is claiming. It also removes an unused
   lifeline from a figure whose point is that it is short.
2. Change the reply instead — `I <--L : ok` — keeping `L` as a fifth participant. Equally
   correct, but it leaves the figure one lifeline wider than the argument needs.
3. Regenerate both figures from the corrected listing and re-render, also fixing the note to name
   `F` rather than `A`.

**Resolution.** Open. This wants deciding before section 6 is cut over: it is the section's
central worked example, it is published twice, and the error is the exact property the tip is
recommending the notation for. Option 1 plus the note fix is the minimal change; whichever is
chosen, [[ISS-040-tips-6-6-and-6-11-publish-the-same-figure-and-listing|ISS-040]] decides whether
it has to be made once or twice.
