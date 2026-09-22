---
id: ISS-036
type: issue
title: Two section 5 tips publish unfinished text — an editor's TODO and an untranslated paragraph
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[tip-5-1]]'
- '[[tip-5-24]]'
severity: major
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Two pages of the live site carry text that was never meant to be read by
anyone but the author: a note-to-self and a paragraph of the German original that was never
translated. Both are visible at the top of their pages.

**Affects.** [[tip-5-1]], [[tip-5-24]].

**Evidence.**

[[tip-5-1]] opens — before any content, as the first line of the body and therefore as the page's
excerpt — with:

> TODO: insert links to specific tips for black-/whitebox

The work it asks for has since been done by other means: the tip closes with "Other tips in this
section refer to both black- and whiteboxes", and the vault now links [[tip-5-1]] to [[tip-5-5]],
[[tip-5-7]] and [[tip-5-8]] through `related:`.

[[tip-5-24]] ends with a German sentence that is a *translation of the English paragraph
immediately above it*:

> Eventuell ist diese „sons- tige“ Information nur für kurze Zeit interessant – also lassen Sie
> das im Zweifel lieber weg.

against the English "_Additional_ information might be relevant for only a brief period of time -
so you might better refrain from including it in the documentation." Note `sons- tige`: the word
*sonstige* broken by a hyphen, which is how it would appear if it had been copied out of a
typeset, line-broken source. So the sentence did not survive from a draft — it was pasted in from
a printed or PDF German original and then left behind when the paragraph above it was written.

That matters beyond this page. [[ISS-030-section-3-bodies-carry-editorial-defects|ISS-030]] argued
from four German constructions in section 3 that these pages were translated rather than written
in English; this is the same claim with the evidence still attached, including the print artefact.
Together with [[ISS-026-german-field-names-in-the-hospital-data-model|ISS-026]] and
[[ISS-032-the-comprehensive-context-diagram-is-german-and-renames-its-system|ISS-032]] it makes
four sections carrying German traces.

**Options.**
1. Delete both at cut-over: the TODO is obsolete and the German sentence is a duplicate, so
   nothing is lost in either case. The smallest possible fix for the most visible defect in the
   section.
2. Fix them on the site now and re-run `brain-raw`, since a published TODO is the kind of thing
   worth not waiting on.
3. Keep the German sentence and translate it — but it says exactly what the paragraph above says,
   so this only restores a redundancy.

**Resolution.** Open; option 1 unless the cut-over of section 5 is far off, in which case option 2.
Both are one-line deletions, and neither touches an image, a URL or a tag.
