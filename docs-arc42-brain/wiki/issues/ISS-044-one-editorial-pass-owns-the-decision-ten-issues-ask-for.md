---
id: ISS-044
type: issue
title: Ten per-section editorial issues ask for one decision; this issue owns it
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-024-section-6-content]]'
related:
- '[[ISS-013-section-2-tip-bodies-carry-editorial-defects]]'
- '[[ISS-015-section-1-tip-bodies-carry-editorial-defects]]'
- '[[ISS-020-section-4-bodies-carry-editorial-defects]]'
- '[[ISS-022-section-10-bodies-carry-editorial-defects]]'
- '[[ISS-024-section-11-bodies-carry-editorial-defects]]'
- '[[ISS-027-section-8-bodies-carry-editorial-defects]]'
- '[[ISS-029-section-7-bodies-carry-editorial-defects]]'
- '[[ISS-030-section-3-bodies-carry-editorial-defects]]'
- '[[ISS-038-section-5-bodies-carry-editorial-defects]]'
- '[[ISS-039-section-6-bodies-carry-editorial-defects]]'
severity: minor
kind: question
raised-by: agent
resolved: null
---

**What's unresolved.** Ten issues hold the defect lists of ten sections, and every one of them ends
by saying the same thing in its own words: this is one decision, not ten. The decision has never
been recorded anywhere, so it is asked again at every ingest and answered nowhere. With all twelve
sections read there is nothing left to wait for, and this issue exists to be the one place it is
settled. The ten keep their evidence; only the decision moves here.

**The decision.** Does the brain correct an obvious defect in an imported body, and if so, when —
during ingest, before a section's cut-over, or as an edit after it? [[ISS-013-section-2-tip-bodies-carry-editorial-defects|ISS-013]]
put it first and most plainly: "does an ingest correct obvious typos, or does the brain stay
byte-faithful until cut-over?" Everything else here is evidence for answering it.

**Affects.** Every section. The ten issues above, plus three that carry defects of the same kind
without being one of the ten: [[ISS-005-tip-9-2-table-markup-broken|ISS-005]] (section 9's "to
hypothetical sets"), [[ISS-025-section-12-example-table-uses-an-exotic-separator|ISS-025]] (section
12's glossary), and [[ISS-026-german-field-names-in-the-hospital-data-model|ISS-026]].

**Evidence.**

*The size.* Nine of the ten issues state a count: 3 defects in section 2, 4 in section 4, 6 in
section 10, 7 in section 8, 8 in section 7, 9 in section 11, 11 in section 6, 14 in section 3, 16
in section 5 — **78 enumerated defects**. [[ISS-015-section-1-tip-bodies-carry-editorial-defects|ISS-015]]
lists section 1's without totalling them; they number about fifteen. So the pass is of the order of
ninety corrections across twelve sections, none of which changes any advice.

*Two findings no single-section reading could produce.* A defect can span sections, and only a pass
over all of them finds it. `ubiqitous` against `ubiquitous` is spelled both ways on different pages
([[ISS-027-section-8-bodies-carry-editorial-defects|ISS-027]]), and `neccessary` is misspelled
identically in sections 7 and 8 ([[ISS-029-section-7-bodies-carry-editorial-defects|ISS-029]]).
Each looks like a typo from inside its own section and like a house-style question from outside it.

*The one finding that is not cosmetic.* [[ISS-030-section-3-bodies-carry-editorial-defects|ISS-030]]
records `sensible data` where the sentence means *sensitive data* — a German false friend that
**inverts a security warning**. Every other defect in all ten issues can be repaired by the reader
from context; this one cannot, because it reads as correct English saying the wrong thing. It is
the argument for not letting the whole pass wait on the whole decision.

*What the German residue turned out to be.* Five issues found German surviving into English, and
together they say something none of them says alone. Section 1 has a stray `Persistenz`
([[ISS-015-section-1-tip-bodies-carry-editorial-defects|ISS-015]]); section 8 has five German
attribute names inside a printed PlantUML model ([[ISS-026-german-field-names-in-the-hospital-data-model|ISS-026]]);
section 3 has four German constructions and a half-German diagram
([[ISS-030-section-3-bodies-carry-editorial-defects|ISS-030]], [[ISS-032-the-comprehensive-context-diagram-is-german-and-renames-its-system|ISS-032]]);
section 5 has two German words and a whole untranslated paragraph
([[ISS-036-two-section-5-tips-ship-unfinished-text|ISS-036]]); section 6 has German word order
surviving a doubled verb ([[ISS-039-section-6-bodies-carry-editorial-defects|ISS-039]]). The
decisive piece is ISS-036's `sons- tige` — *sonstige* broken by a **print hyphen** — which shows the
text was pasted out of a typeset German original rather than drafted in English. That reframes the
pass: it is not a spellcheck, it is a hunt for translation artefacts, and a spellchecker finds
`propegation` but not `sensible data`, `contain always contain` or a hyphen inside a German word.

**Options.**
1. **One pass, after the last cut-over.** The brain owns every body, so a correction is an ordinary
   edit and parity is not involved. Cleanest, and furthest away: seven sections are still at
   `review` and cut-over has no date.
2. **One pass, now, in the brain, accepting a deliberate parity break per section.** Every corrected
   section's `generate-check` would report body deltas until that section is cut over, which turns
   a check that currently means "nothing unexpected" into one with a standing exception list. That
   is the real cost, and it is the reason the ten issues all hesitated.
3. **Fix at cut-over, section by section.** Each section is corrected in the same change that
   publishes it, so parity is never broken and the work is spread. The two cross-section defects
   have to be handled deliberately, or the sections will be corrected to disagree with each other
   again.
4. **Fix the inverted security warning now** ([[ISS-030-section-3-bodies-carry-editorial-defects|ISS-030]]),
   and choose between 1, 2 and 3 for the rest. This is orthogonal to the others and can be taken
   whichever way the main question goes.

**Resolution.** Open. This issue asks for nothing new — it names a decision the ten made ten times
and records what is now known that none of them could know alone: the size (about ninety), the two
defects that span sections, the one that inverts a meaning, and the fact that the German residue is
a translation artefact rather than carelessness. The ten stay open and keep their lists; whichever
option is chosen here, they are what the pass works from.
