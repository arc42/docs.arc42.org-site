---
id: ISS-016
type: issue
title: Tables use separator rows as row dividers, which kramdown renders as data rows
status: open
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-015-section-1-content]]'
related:
- '[[tip-1-4]]'
- '[[01-quality-reqs-example-1]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Two section 1 tables use a `|---|---|` row as a visual divider *between*
data rows, and one uses it as a closing line. GFM tables have exactly one separator row, directly
under the header; every later one is a normal row, so kramdown renders a line of dashes as table
content. The author's intent was clearly a ruled table.

**Affects.** [[tip-1-4]], [[01-quality-reqs-example-1]].

**Evidence.** [[tip-1-4]]'s requirements-cluster table ends with
`|--------------------------------|------------------------------------------------|` after the
last data row. [[01-quality-reqs-example-1]] puts `|---|---|---|` between all six quality
requirements, so the rendered table has twelve rows instead of six. Same defect class as
[[ISS-005-tip-9-2-table-markup-broken|ISS-005]], where tip 9-2 uses `=` as its separator row —
which suggests the tables were written for a different Markdown flavour.

**Options.**
1. Delete the surplus separator rows when the brain owns the content, and fold the fix into
   whichever pass resolves [[ISS-005-tip-9-2-table-markup-broken|ISS-005]] — one rule, three
   tables.
2. Add a lint rule that flags a table row consisting only of dashes and pipes below the first
   separator — catches this in the nine sections still to be ingested, at the price of a new
   check with a real chance of false positives.
3. Leave them — the tables are readable, just with stray dash rows.

**Resolution.** Open. Option 2 is attractive precisely because two sections have produced three
instances, so the remaining nine will produce more.
