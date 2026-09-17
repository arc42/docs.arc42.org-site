---
id: ISS-005
type: issue
title: The second criteria table in tip 9-2 has an invalid separator row
status: open
created: '2026-09-17'
updated: '2026-09-17'
sources:
- '[[SRC-013-section-9-content]]'
related:
- '[[tip-9-2]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** In tip 9-2 the second example table ("Criteria how to implement complex
business rules") uses `=` instead of `-` in its separator row, which is not a GFM table separator.
The block therefore does not render as a table. The same paragraph also reads "Below you find to
hypothetical sets", where "to" should be "two". Both are verbatim body text, so the ingest records
them instead of fixing them.

**Affects.** [[tip-9-2]].

**Evidence.** The separator row is `|======|========|============|`; the first table on the same
page correctly uses `|----------|-------------|-------------|`.

**Options.**
1. Fix both in the site source and re-import the tip — the body stays a faithful copy of the site.
2. Fix them in the brain once the brain owns the content (after cutover) — avoids editing the
   legacy source twice.

**Resolution.** Open.
