---
id: ISS-042
type: issue
title: Two section 6 figures are stored in the section 7 image folder
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-024-section-6-content]]'
related:
- '[[tip-6-3]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** [[tip-6-3]]'s two figures are stored under `assets/images/sections/07/`.
No section 7 page uses either of them, and no other page in the site uses them at all.

**Affects.** [[tip-6-3]].

**Evidence.** The tip's body builds both image paths from the `site.imageurl` Liquid variable
followed by `/07/schematic-sequence.png` and `/07/level-1-for-schematic-sequence.png`.
A grep for `schematic-sequence` across `_posts/` and `_pages/` returns one file —
`_posts/06-runtime/2016-03-01-t-6-3.md` — and `assets/images/sections/07/` holds both files
beside five genuinely-section-7 deployment figures. Both are content: a schematic sequence
diagram and the level-1 building block view it is drawn against, which is the pairing the tip
exists to show.

The site's own convention, stated in `CLAUDE.md`, is `images/[section-number]-[descriptive-name]`,
and every other section 6 figure sits in `assets/images/sections/06/`.

**Options.**
1. Move both files to `assets/images/sections/06/` and update the two references in [[tip-6-3]].
   Image URLs are not page URLs, so nothing is retired and
   `_system/published-permalinks.txt` is untouched; only a hot-linker outside the site would
   notice, which for a figure inside a tip is not a real risk.
2. Leave them and record the exception, so that a later mechanical audit of asset paths does not
   report it again.

**Resolution.** Open. Mechanical, decidable on its own, and independent of section 6's cut-over —
the brain stores the reference as written either way. Worth doing with option 1 during the same
pass as the other asset warts, if one is ever made.
