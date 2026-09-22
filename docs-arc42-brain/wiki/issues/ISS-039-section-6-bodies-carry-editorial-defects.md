---
id: ISS-039
type: issue
title: Section 6 bodies carry editorial defects
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-024-section-6-content]]'
related:
- '[[tip-6-1]]'
- '[[tip-6-6]]'
- '[[tip-6-7]]'
- '[[tip-6-9]]'
- '[[tip-6-11]]'
- '[[06-runtime-example-htmlsc-1]]'
- '[[06-runtime-example-mama-2]]'
- '[[06-runtime-example-tpu-1]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Eleven defects in the section 6 bodies: misspellings, a doubled verb, a
list numbered wrong in the source, an unfinished sentence and a link with no label. None changes
the advice; all of them are visible to a reader.

**Affects.** [[tip-6-1]], [[tip-6-6]], [[tip-6-7]], [[tip-6-9]], [[tip-6-11]],
[[06-runtime-example-htmlsc-1]], [[06-runtime-example-mama-2]], [[06-runtime-example-tpu-1]].

**Evidence.**

Misspellings:

1. [[tip-6-6]] — "just propagate date over several participants", for *data*.
2. [[tip-6-6]] — "boring, standard, simple of straightforward stuff", for *or*.
3. [[tip-6-7]] — "in wich case you need different tools", for *which*.
4. [[tip-6-9]] — "It has a lightweigth textual syntax (DSL)", for *lightweight*.
5. [[tip-6-11]] — "have somt tool render the diagrams for you", for *some*.
6. [[06-runtime-example-mama-2]] — "a uniqe ID identifying the mandator", for *unique*.
7. [[06-runtime-example-tpu-1]] — "the propegation of the distance per frame", for
   *propagation*; the same sentence the page spells correctly two paragraphs earlier.
8. [[06-runtime-example-tpu-1]] — "showing asynchonously communicating activity diagrams", for
   *asynchronously*.

Grammar and structure:

9. [[06-runtime-example-mama-2]] — "Such files contain always contain `Client` related data": the
   verb appears twice, and the surviving word order ("contain always") is the German one. The same
   translation signature [[ISS-030-section-3-bodies-carry-editorial-defects|ISS-030]] found in
   section 3 and [[ISS-036-two-section-5-tips-ship-unfinished-text|ISS-036]] in section 5.
10. [[tip-6-1]] — the link text is empty of its own subject: "see [tip (sequence diagrams)](/tips/6-11)",
    where every other cross-reference in the section names the tip's number.
11. [[06-runtime-example-tpu-1]] — a sentence that was never finished: "the processing and
    propagation of all measuring data: speedometer pulses,  ......)". The ellipsis is published.

And one that is only a defect in the source: [[06-runtime-example-htmlsc-1]]'s explanation of the
main loop numbers its seven steps `0. 1. 2. 2. 3. 4. 5.` — a repeated 2 and a start at 0.
Kramdown renumbers them 1–7 in the rendered page, so the reader sees a correct list and only
someone editing the Markdown meets the wrong numbers. Worth fixing with the rest, not worth
fixing alone.

**Options.**
1. Fix all eleven with the section 6 pass — mechanical, no decisions needed.
2. Fold them into the one vault-wide spelling pass that
   [[ISS-013-section-2-tip-bodies-carry-editorial-defects|ISS-013]],
   [[ISS-015-section-1-tip-bodies-carry-editorial-defects|ISS-015]],
   [[ISS-020-section-4-bodies-carry-editorial-defects|ISS-020]],
   [[ISS-022-section-10-bodies-carry-editorial-defects|ISS-022]],
   [[ISS-024-section-11-bodies-carry-editorial-defects|ISS-024]],
   [[ISS-027-section-8-bodies-carry-editorial-defects|ISS-027]],
   [[ISS-029-section-7-bodies-carry-editorial-defects|ISS-029]],
   [[ISS-030-section-3-bodies-carry-editorial-defects|ISS-030]] and
   [[ISS-038-section-5-bodies-carry-editorial-defects|ISS-038]] all describe.

**Resolution.** Open. The tenth and last of the per-section editorial issues: with section 6
ingested, every one of the twelve sections has now been read, and nine of the twelve carry
defects of this kind. Defect 9 is the third section in which the German source shows through the
English, after sections 3 and 5, which is the argument for one pass over the whole vault rather
than ten separate ones.
