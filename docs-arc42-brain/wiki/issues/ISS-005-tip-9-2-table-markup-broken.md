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
business rules") uses `=` instead of `-` in its separator row, so the table renders without a
header. The same paragraph also reads "Below you find to hypothetical sets", where "to" should be
"two". Both are verbatim body text, so the ingest records them instead of fixing them.

**Correction (2026-09-22).** This issue was raised claiming that `=` "is not a GFM table separator"
and that "the block therefore does not render as a table". Both halves are wrong, and checking the
built site is what showed it. `|====` *is* meaningful to kramdown — it is the **footer** separator,
not an invalid one — so the block renders as a `<table>`, but with the header row demoted into
`<tbody>` as `<td>` cells and every data row pushed into `<tfoot>`. The defect is real and worth
fixing; it is just not the defect this issue described.

**Affects.** [[tip-9-2]].

**Evidence.** The separator row is `|======|========|============|`; the first table on the same
page correctly uses `|----------|-------------|-------------|`. In `_site/tips/9-2/index.html` the
first table opens `<table><thead><tr><th><strong>ID</strong></th>…`, and the second opens
`<table><tbody><tr><td><strong>ID</strong></td>…` followed by `<tfoot>` holding C1 to C4. So the
two tables on one page differ in structure, and the second has no `<th>` anywhere — which is an
accessibility defect as well as a visual one.

The same construct appears once more in the vault, in [[12-glossary-example-htmlsc-1]], where
[[ISS-025-section-12-example-table-uses-an-exotic-separator|ISS-025]] described it the opposite way round — as
"kramdown's header separator with alignment, which is valid". That was also wrong: the glossary
table renders `<tbody><tr><td>Term</td>…` with no `<thead>` either. One construct, two issues, two
different incorrect explanations; this paragraph is the correct one for both.

**Options.**
1. Fix both in the site source and re-import the tip — the body stays a faithful copy of the site.
2. Fix them in the brain once the brain owns the content (after cutover) — avoids editing the
   legacy source twice.

**Resolution.** Open, with the description now corrected. It should be decided together with
[[ISS-025-section-12-example-table-uses-an-exotic-separator|ISS-025]] and
[[ISS-016-repeated-separator-rows-in-tables|ISS-016]]: all three are about kramdown table rows that
do not do what their author meant, and a fix for one is a fix for the same two characters in the
other.
