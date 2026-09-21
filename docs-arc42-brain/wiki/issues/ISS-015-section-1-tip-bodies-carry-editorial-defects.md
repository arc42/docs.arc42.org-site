---
id: ISS-015
type: issue
title: The section 1 bodies carry typos, a stale tip label and an empty image alt text
status: open
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-015-section-1-content]]'
related:
- '[[tip-1-1]]'
- '[[tip-1-8]]'
- '[[tip-1-9]]'
- '[[tip-1-10]]'
- '[[tip-1-11]]'
- '[[tip-1-16]]'
- '[[tip-1-20]]'
- '[[tip-1-21]]'
- '[[01-overview-example-3]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Section 1 is the largest batch ingested so far (24 tips, 4 examples) and
came in verbatim, defects included. Two of them are more than cosmetic: a tip label that no longer
matches the site's own numbering, and an image with no alt text.

**Affects.** [[tip-1-1]], [[tip-1-8]], [[tip-1-9]], [[tip-1-10]], [[tip-1-11]], [[tip-1-16]],
[[tip-1-20]], [[tip-1-21]], [[01-overview-example-3]].

**Evidence.**
- [[tip-1-16]] links tip 1-12 with the label of a numbering scheme the site no longer uses:
  "see [tip IV-12](/tips/1-12)". The URL is right, the visible text is wrong — a reader looking
  for "tip IV-12" finds nothing on the site.
- [[tip-1-9]]: the rendered PlantUML diagram is included with an empty alt text — the image
  include has nothing between its brackets. It is the same file `simple-activity.png` that
  [[tip-1-6]] includes with a proper alt text ("'Create invoice' activity diagram"), so the fix
  is a copy from the neighbouring tip.
- Typos: "requiremens" ([[tip-1-10]]), "you can captures" ([[tip-1-11]]), "unnessessary"
  ([[tip-1-20]]), "Persistenz" — German — and "Ms. Foobar, Ph.D." next to "Mrs. Lovelace, Ph.D."
  ([[tip-1-21]]), "accompaning", "strenghten", "featurers", "policecar"
  ([[01-overview-example-3]]).
- Missing words and spaces: "Our rule of thumb:Less than one page" and "you should focus only the
  parts of the requirements" — missing "on" ([[tip-1-1]]); "a numbered lists" ([[tip-1-8]]);
  "activity diagrams [see tip 1-6](/tips/1-6) are the better choice" ends without a period
  ([[tip-1-8]]).

**Options.**
1. Fix all of it during the section 1 cut-over, in the commit that publishes the pages, with the
   intended diff recorded in the log — same treatment [[ISS-013-section-2-tip-bodies-carry-editorial-defects|ISS-013]] proposes for section 2.
2. Fix only the two substantive ones (the "tip IV-12" label and the empty alt text) now and leave
   the spelling for a later pass.
3. Leave everything — it is all live on the site today.

**Resolution.** Open, and it is the same decision as
[[ISS-013-section-2-tip-bodies-carry-editorial-defects|ISS-013]], now with a second section's
evidence: two sections in, every ingest has found this class of defect, so the rule should be set
once rather than per section.
