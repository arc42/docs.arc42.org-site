---
id: ISS-033
type: issue
title: The context examples' numbers and permalinks do not line up with their systems
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-022-section-3-content]]'
related:
- '[[03-context-example-business-1]]'
- '[[03-context-example-business-2]]'
- '[[03-context-example-business-3]]'
- '[[03-context-example-business-4]]'
- '[[03-context-example-technical-1]]'
- '[[03-context-example-technical-4]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Section 3 is the first section with two example categories, and its six
examples number them independently. The trailing number therefore identifies a system in one
category and a different system in the other, and one permalink inverts its own words.

**Affects.** all six section 3 examples.

**Evidence.** The business examples are 1 = HtmlSC, 2 = MaMa, 3 = TPU, 4 = status.arc42.org. The
technical examples are 1 = HtmlSC and 4 = TPU. So *business-1* and *technical-1* are the same
system, which reads as a rule — and then *business-4* is status.arc42.org while *technical-4* is
TPU, whose business half is *business-3*. Anyone linking "the technical context of example 4"
lands on the wrong system half the time.

The permalinks disagree with the filenames as well:

| page | permalink |
|---|---|
| [[03-context-example-business-1]] | `/examples/business-context-1/` |
| [[03-context-example-business-2]] | `/examples/context-business-2/` |
| [[03-context-example-business-3]] | `/examples/business-context-3/` |
| [[03-context-example-business-4]] | `/examples/business-context-4/` |
| [[03-context-example-technical-1]] | `/examples/technical-context-1/` |
| [[03-context-example-technical-4]] | `/examples/technical-context-4/` |

Five follow `<category>-<n>`; [[03-context-example-business-2]] alone reverses the two words.

**Options.**
1. Leave every URL exactly as it is and record the mapping — in the examples index or in each
   page's own front matter — so that "example 4" is never used as an identifier in prose. Costs
   nothing and breaks nothing.
2. Renumber the technical examples to follow their business twins (`technical-3` for TPU) and
   retire the old URLs through `_system/retired-permalinks.txt`. Correct, and the site has no
   redirect plugin, so every retired URL becomes a hard 404 for anyone holding a link.
3. Fix only the odd permalink of business-2. Same cost as option 2 for one page, and it makes the
   set consistent in spelling while leaving the numbering wrong — the smaller of the two problems
   solved.

**Resolution.** Open, and the recommendation is option 1: these are published URLs, a retirement
is irreversible for anyone holding a link, and the inconsistency costs a reader nothing as long as
the project never refers to an example by its number. Worth deciding before section 3 is cut over,
because cut-over is what makes the six URLs permanent entries in
`_system/published-permalinks.txt`.
