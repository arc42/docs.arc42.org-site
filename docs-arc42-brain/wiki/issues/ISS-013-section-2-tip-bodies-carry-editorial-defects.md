---
id: ISS-013
type: issue
title: The section 2 tip bodies carry a typo and mix British and American spelling
status: open
created: '2026-09-20'
updated: '2026-09-20'
sources:
- '[[SRC-014-section-2-content]]'
related:
- '[[tip-2-2]]'
- '[[tip-2-4]]'
- '[[tip-2-5]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Three editorial defects came in verbatim with the ingest and are live on
the site today. The brain now owns these bodies, so it is the place to fix them — but a fix
changes bytes that the parity check compares against the site, so it must happen deliberately,
either before the section 2 cut-over or as an edit right after it.

**Affects.** [[tip-2-2]], [[tip-2-4]], [[tip-2-5]].

**Evidence.**
- [[tip-2-4]]: "technical **contraints** will probably apply as well" — missing `s`. Also
  "guidelines from the **managements**" (plural) where the sentence needs the singular.
- Spelling is mixed inside single pages and across the section: [[tip-2-4]] has "organisational
  constraints" in the body and "organizational" in the reference to [[tip-2-3]]; [[tip-2-5]] has
  "organizational constraints" and "organisational conventions" in the same sentence. The rest of
  the vault, including `wiki/sections/section-2.md`, is American.
- [[tip-2-2]]: the second paragraph starts with a stray leading space (" If constraints bring
  *unreasonable* consequences"), which is in the raw post too
  (`raw/ingested/section-2-content/posts/2016-03-01-t-2-2.md`).

**Options.**
1. Fix all three during the section 2 cut-over, in the same commit that publishes the pages, and
   note the intended diff in the log — the generated files then differ from today's site by
   exactly these characters.
2. Fix them after the cut-over as an ordinary content edit — keeps the cut-over a pure move, costs
   a second regeneration.
3. Leave them — they are cosmetic and the site has carried them since 2016.

**Resolution.** Open. Deciding this also sets the rule for the ten sections still to be ingested:
does an ingest correct obvious typos, or does the brain stay byte-faithful until cut-over?
