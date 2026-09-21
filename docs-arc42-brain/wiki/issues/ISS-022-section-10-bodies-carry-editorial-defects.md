---
id: ISS-022
type: issue
title: Section 10 bodies carry editorial defects, one of them a broken link
status: open
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-017-section-10-content]]'
related:
- '[[tip-10-4]]'
- '[[tip-10-5]]'
- '[[tip-10-6]]'
- '[[tip-10-7]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Six defects in section 10's bodies. One is not cosmetic: a misplaced
bracket in [[tip-10-6]] leaves a stray parenthesis in the rendered link text.

**Affects.** [[tip-10-4]], [[tip-10-5]], [[tip-10-6]], [[tip-10-7]].

**Evidence.**

- [[tip-10-6]], the broken one: the link is written `[usage or application scenarios (see tip
  10-5](/tips/10-5))` — the closing bracket sits before the parenthesis it should follow, so the
  link text keeps an unbalanced "(" and a ")" is left over after the link.
- [[tip-10-6]]: "reaction to changes service-level agreements" is missing a word ("changes *to*"),
  and "statuory" should be "statutory".
- [[tip-10-4]]: "Let your stakeholders decide wether" — "whether".
- [[tip-10-5]]: `Some authors call these _externally visible quality".` opens the phrase with an
  underscore and closes it with a double quote, so kramdown renders a literal quotation mark and
  no emphasis.
- [[tip-10-7]]: "Murphys’ law" — the apostrophe is on the wrong side of the s.

**Options.**
1. Fix them at cut-over, in the brain, as part of owning the content.
2. Fix them on the site now, before cut-over, and re-run `brain-raw` so the brain stays verbatim.
3. Leave them.

**Resolution.** Open, and now the fourth section with a typo issue of its own
([[ISS-013-section-2-tip-bodies-carry-editorial-defects|ISS-013]],
[[ISS-015-section-1-tip-bodies-carry-editorial-defects|ISS-015]],
[[ISS-020-section-4-bodies-carry-editorial-defects|ISS-020]]). The broken link in 10-6 is the
first defect in this class that a reader plainly sees, which argues for fixing that one ahead of
the rest rather than waiting for a vault-wide pass.
