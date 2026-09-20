---
id: ISS-006
type: issue
title: Tips reference other tips by hard-coded site URL instead of a wikilink
status: open
created: '2026-09-17'
updated: '2026-09-20'
sources:
- '[[SRC-013-section-9-content]]'
- '[[SRC-014-section-2-content]]'
related:
- '[[tip-9-3]]'
- '[[tip-9-5]]'
- '[[tip-2-3]]'
- '[[tip-2-4]]'
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

**Options.**
1. Rewrite them to `[[tip-9-2]]` when the brain owns the content (after cutover), and let the
   generator emit the permalink — the permalink `/tips/9-2/` never changes, so the rendered result
   is identical.
2. Leave them — they work on the site, but every future move of a tip breaks them silently.

**Resolution.** Open; the same pattern is expected in other sections, so decide once. Confirmed
in section 2, which is the second section ingested. The `related:` lists of all four tips already
mirror the references by hand, so a rewrite would add no link, only make the body honest.
