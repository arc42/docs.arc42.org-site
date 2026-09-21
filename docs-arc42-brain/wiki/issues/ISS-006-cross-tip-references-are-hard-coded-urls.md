---
id: ISS-006
type: issue
title: Tips reference other tips by hard-coded site URL instead of a wikilink
status: open
created: '2026-09-17'
updated: '2026-09-21'
sources:
- '[[SRC-017-section-10-content]]'
- '[[SRC-016-section-4-content]]'
- '[[SRC-015-section-1-content]]'
- '[[SRC-013-section-9-content]]'
- '[[SRC-014-section-2-content]]'
related:
- '[[tip-10-4]]'
- '[[tip-10-6]]'
- '[[tip-10-8]]'
- '[[tip-1-8]]'
- '[[tip-1-11]]'
- '[[tip-1-14]]'
- '[[tip-1-15]]'
- '[[tip-1-16]]'
- '[[tip-1-17]]'
- '[[tip-1-18]]'
- '[[tip-9-3]]'
- '[[tip-9-5]]'
- '[[tip-2-3]]'
- '[[tip-2-4]]'
- '[[tip-4-1]]'
- '[[tip-4-3]]'
- '[[tip-4-4]]'
- '[[section-4]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Both bodies link tip 9-2 as `](/tips/9-2)`. The vault's convention is that
every cross-reference is a wikilink, so that the link graph is complete and the lint can resolve
it. As bodies stay verbatim during ingest, these two references are invisible to the vault: the
ingest mirrored them in `related:` by hand.

**Affects.** [[tip-9-3]], [[tip-9-5]], [[tip-2-3]], [[tip-2-4]].

**Evidence.** `tip-9-3`: "see [tip 9-2 (decision criteria)](/tips/9-2)". `tip-9-5`: "see
[tip 9-2 (document decision criteria)](/tips/9-2)". `grep -n '](/' wiki/tips/tip-9-*.md` finds no
others in section 9. Section 2, ingested 2026-09-20, shows the same pattern and makes it mutual:
`tip-2-3` ends with "See also [tip 2-4 (technical constraints)](/tips/2-4)." and `tip-2-4` both
opens with "(see [tip 2-3](/tips/2-3))" and ends with "See also [tip 2-3 (organizational
constraints)](/tips/2-3)" — the second reference without a closing period.

**Section 1 evidence (2026-09-21).** Seven more tips, and a new case the first two sections did
not show: references that leave the section. [[tip-1-17]] links `/section-4` and `/tips/4-2`, and
[[tip-1-18]] links `/section-10` — targets in sections that are not in the brain yet. A wikilink
to `[[section-4]]` resolves today (all twelve section pages exist), but a wikilink to tip 4-2 cannot exist
until section 4 is ingested. So option 1 is not a single rewrite: section-internal references can
be converted at any time, cross-section tip references only in ingest order, and a rewrite done
too early would fail the lint. Also affected: [[tip-1-8]] → 1-6 twice, [[tip-1-11]] → 1-12,
[[tip-1-14]] → 1-15, [[tip-1-15]] → 1-12 and 1-24, [[tip-1-16]] → 1-12 (with the stale label
"tip IV-12", see [[ISS-015-section-1-tip-bodies-carry-editorial-defects|ISS-015]]).

**Section 4 evidence (2026-09-21).** Four more references, all section-internal: [[tip-4-1]] and
[[tip-4-3]] link `/tips/4-2`, and [[tip-4-4]] links both `/tips/4-2` and `/tips/4-3`. Two things
are new. First, a *section page* does it too: section 4's *Form* links `/section-5` and
`/section-8` from inside its `[!arc42-help]` callout, so the issue is not limited to tips — the
title's wording is now narrower than the finding. Second, the cross-section case from section 1 is
resolvable for the first time: with section 4 ingested, [[tip-1-17]]'s `/tips/4-2` could become
`[[tip-4-2]]` today. It was deliberately left as it is, so that the rewrite stays one reviewable
sweep instead of a trickle that follows the ingest order; this issue is the record that it is now
possible.

**Section 10 evidence (2026-09-21).** Three more, and one of them is the case this issue has been
waiting for: [[tip-10-4]] links `/tips/1-14/` — a tip in a section that is now **cut over**, so
`[[tip-1-14]]` would resolve today and generate the identical URL. Same for [[tip-10-8]]'s
`/tips/4-2`. Only [[tip-10-6]]'s `/tips/10-5` is section-internal (and it is the broken link of
[[ISS-022-section-10-bodies-carry-editorial-defects|ISS-022]]). With sections 1, 2, 4 and 9 cut
over, most cross-section references in the remaining sections will be resolvable as they are
ingested, which turns option 1 from "one sweep, later" into "the sweep can start whenever we
choose". Note also the spelling: `/tips/1-14/` has a trailing slash where every earlier reference
had none, so a mechanical rewrite has to accept both.

**Options.**
1. Rewrite them to `[[tip-9-2]]` when the brain owns the content (after cutover), and let the
   generator emit the permalink — the permalink `/tips/9-2/` never changes, so the rendered result
   is identical.
2. Leave them — they work on the site, but every future move of a tip breaks them silently.

**Resolution.** Open; the same pattern is expected in other sections, so decide once. Confirmed
in section 2, which is the second section ingested. The `related:` lists of all four tips already
mirror the references by hand, so a rewrite would add no link, only make the body honest.
