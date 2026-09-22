---
id: ISS-027
type: issue
title: Section 8 bodies carry editorial defects
status: open
created: '2026-09-21'
updated: '2026-09-22'
sources:
- '[[SRC-020-section-8-content]]'
related:
- '[[tip-8-3]]'
- '[[tip-8-5]]'
- '[[tip-8-10]]'
- '[[tip-8-11]]'
- '[[ISS-044-one-editorial-pass-owns-the-decision-ten-issues-ask-for]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Seven defects, and one of them is a word the vault now spells two ways.

**Affects.** [[tip-8-3]], [[tip-8-5]], [[tip-8-10]], [[tip-8-11]].

**Evidence.**

- [[tip-8-5]]: "the so called _ubiqitous language_" is missing a `t`. [[tip-12-2]] spells the same
  DDD term correctly ("„ubiquitous language“"), so the vault carries both spellings of one term —
  in the two tips that point at each other's sections.
- [[tip-8-5]]: "In case you follow a Domain-Driven Design approach (DDD) approach for design" says
  "approach" twice.
- [[tip-8-3]]: "absolutely relevant or neccessary" — "necessary".
- [[tip-8-10]]: "non-reputiability" should be "non-repudiability", and "Parallization and
  threading" should be "Parallelization".
- [[tip-8-11]]: "the French guillements «..»" — "guillemets"; and "Thanx to Wolfgang Reimesch" is
  the only contributor credit written into a tip body anywhere in the vault, which is a question of
  where credits belong rather than a typo.

**Options.**
1. Fix them at cut-over, in the brain, as part of owning the content.
2. Fix them on the site now, before cut-over, and re-run `brain-raw` so the brain stays verbatim.
3. Leave them.

**Resolution.** Open, the sixth section with a typo issue of its own. Six issues now describe one
decision, which is the argument for a single vault-wide spelling pass rather than a seventh at
section 3 — the `ubiqitous`/`ubiquitous` split is the first case where two pages disagree with each
other rather than with a dictionary, and only a pass over the whole vault would notice that class.

**The decision this issue asks for lives in [[ISS-044-one-editorial-pass-owns-the-decision-ten-issues-ask-for|ISS-044]]** (2026-09-22). Ten per-section issues each asked the same question — correct in the brain, or stay byte-faithful until cut-over? — and none of them owned the answer. This one keeps its own defect list, which is what the eventual pass works from.
