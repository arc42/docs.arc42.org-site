---
id: ISS-024
type: issue
title: Section 11 bodies carry editorial defects, mostly in the TPU example
status: open
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-018-section-11-content]]'
related:
- '[[tip-11-1]]'
- '[[tip-11-4]]'
- '[[tip-11-6]]'
- '[[11-risk-example-tpu]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Nine defects, seven of them in one page. None changes the meaning, but the
TPU example's density is a different order from the three tips'.

**Affects.** [[tip-11-1]], [[tip-11-4]], [[tip-11-6]], [[11-risk-example-tpu]].

**Evidence.**

- [[tip-11-6]]: "cyclomatic complexitx" — and "statical analysis" where the parallel with
  "dynamical" is what makes it read oddly ("static"/"dynamic").
- [[tip-11-4]]: "management and related decision processes might not aligned with system
  requirements" is missing "be".
- [[tip-11-1]]: "UX or useability experts" — "usability".
- [[11-risk-example-tpu]]: "solid state disks were not avilable"; "we were depend on reliable
  cooperation"; "hard manoevers of accelleration and braking" (two in three words); "several
  tenthousands of kilometers"; and `**Hardware  Risks**` carries a double space, which matters
  only if the bold lines become headings — see
  [[ISS-023-tpu-risk-example-uses-bold-text-as-headings|ISS-023]].

**Options.**
1. Fix them at cut-over, in the brain, as part of owning the content.
2. Fix them on the site now, before cut-over, and re-run `brain-raw` so the brain stays verbatim.
3. Leave them.

**Resolution.** Open, the fifth section with a typo issue of its own
([[ISS-013-section-2-tip-bodies-carry-editorial-defects|ISS-013]],
[[ISS-015-section-1-tip-bodies-carry-editorial-defects|ISS-015]],
[[ISS-020-section-4-bodies-carry-editorial-defects|ISS-020]],
[[ISS-022-section-10-bodies-carry-editorial-defects|ISS-022]]). Five separate issues describing
one decision is itself the argument: these should be one vault-wide spelling pass, decided once.
