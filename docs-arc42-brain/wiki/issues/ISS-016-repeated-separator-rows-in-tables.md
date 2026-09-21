---
id: ISS-016
type: issue
title: Tables use separator rows as row dividers, which kramdown renders as data rows
status: open
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-018-section-11-content]]'
- '[[SRC-017-section-10-content]]'
- '[[SRC-015-section-1-content]]'
related:
- '[[11-risk-example-htmlsc]]'
- '[[10-quality-scenario-example-htmlsc-2]]'
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

**Section 10 evidence (2026-09-21).** A fourth instance, and the worst of them:
[[10-quality-scenario-example-htmlsc-2]] puts a `|-------|---...---|` separator between *every*
pair of data rows — four of them in a three-scenario table — so kramdown renders four extra rows
of dashes inside the quality-scenario table the example exists to show. Two instances were a
pattern; four across three sections is a habit, which strengthens option 2 (a lint rule) over
fixing them one at a time.

**Section 11 evidence (2026-09-21).** A fifth instance, in a new position:
[[11-risk-example-htmlsc]] ends its two-row risk table with a trailing
`|------|------|` separator, so kramdown renders a row of dashes as the table's last line. The
earlier four put separators *between* data rows; this one is after the last, which a lint rule
would have to catch as the same defect.

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
