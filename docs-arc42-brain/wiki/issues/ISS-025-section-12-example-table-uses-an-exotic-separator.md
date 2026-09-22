---
id: ISS-025
type: issue
title: The glossary example's table mixes two separator styles, one of them exotic
status: open
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-019-section-12-content]]'
related:
- '[[12-glossary-example-htmlsc-1]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** [[12-glossary-example-htmlsc-1]]'s table opens with `|=====|:==========|`
and then puts a `|-----|-----|` between every pair of data rows. The `=` row costs the table its
header; the rest are the pattern [[ISS-016-repeated-separator-rows-in-tables|ISS-016]] has now
found in six places. On the site the glossary — the one table whose whole job is to be read row by
row — renders with a row of dashes between each entry.

**Correction (2026-09-22).** This issue originally called `|=====|:==========|` "kramdown's
*header separator with alignment*, which is valid". That is wrong. `|====` is kramdown's **footer**
separator, so the row does not mark a header at all: the rendered glossary opens
`<table><tbody><tr><td>Term</td><td>Definition</td>` with no `<thead>` and no `<th>` — the column
titles are ordinary cells. The alignment colon is read, but on a row that is not doing the job the
author meant it to do.

The same construct, with the same consequence, is the subject of
[[ISS-005-tip-9-2-table-markup-broken|ISS-005]], which described it wrongly in the opposite
direction — as markup that stops the block rendering as a table at all. Two issues, one construct,
two incorrect explanations, both now corrected; ISS-005 carries the verified account.

**Affects.** [[12-glossary-example-htmlsc-1]].

**Evidence.** The table is four terms long (Link, Cross Reference, External Hyperlink, Run Result)
and carries four separator rows between and after them, plus the `=` header row. The same page is
the example [[tip-12-2]] points to for "an alphabetically sorted table", and the entries are not
in fact alphabetical.

**Options.**
1. Fix it with ISS-016's decision — it is the same defect, and this page is the strongest argument
   for fixing rather than tolerating it.
2. Keep the `=` header separator, which is legal kramdown and renders a slightly heavier rule, and
   drop only the interior separators.
3. Leave it.

**Resolution.** Open, and folded into ISS-016 for the separator rows; kept as its own issue for
the two findings ISS-016 does not cover — the exotic `=` header row, and the example not being
sorted alphabetically while the tip that links it asks for exactly that.
