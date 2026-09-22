---
id: ISS-016
type: issue
title: Tables use separator rows as row dividers, which kramdown renders as data rows
status: open
created: '2026-09-21'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
- '[[SRC-022-section-3-content]]'
- '[[SRC-021-section-7-content]]'
- '[[SRC-020-section-8-content]]'
- '[[SRC-019-section-12-content]]'
- '[[SRC-018-section-11-content]]'
- '[[SRC-017-section-10-content]]'
- '[[SRC-015-section-1-content]]'
related:
- '[[05-buildingblock-example-hsc]]'
- '[[05-buildingblock-example-status]]'
- '[[tip-5-7]]'
- '[[03-context-example-business-1]]'
- '[[03-context-example-business-2]]'
- '[[03-context-example-technical-1]]'
- '[[tip-3-3]]'
- '[[tip-7-7]]'
- '[[07-deployment-sample-htmlsc-1]]'
- '[[08-concept-example-htmlsc-1]]'
- '[[12-glossary-example-htmlsc-1]]'
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

**Section 12 evidence (2026-09-21).** A sixth instance, and the one that matters most to a reader:
the glossary example — the single table whose job is to be read row by row — has a separator
between every pair of its four terms, and opens with an exotic `|=====|:==========|` header row.
Kept as [[ISS-025-section-12-example-table-uses-an-exotic-separator|ISS-025]] for the parts this
issue does not cover. Six instances across four sections settles the question of whether this is
incidental.

**Section 8 evidence (2026-09-21).** A seventh instance:
[[08-concept-example-htmlsc-1]]'s domain-terminology table separates every pair of entries, the
same shape as the section 12 glossary example. Both are glossary-style tables, which suggests the
habit travels with the table's *purpose* rather than with the author.

**Section 7 evidence (2026-09-22), and the pattern resolved.**
[[07-deployment-sample-htmlsc-1]]'s node/artifact table separates every pair of rows. Counting
separator rows across every ingested example settles what this issue is actually about: the six
pages carrying the habit are **all six HtmlSC examples** — deployment (6 separator rows of 12
table lines), concept 8.1 (14 of 30), concept 8.3 (5 of 10), quality scenarios (8 of 16), risks
(4 of 9) and the glossary (6 of 12) — and **no TPU or MaMa example has a single one**. So this is
not a habit that travels with a table's purpose, as the section 8 note guessed; it tracks the
author of the example. That makes it one editing pass over one set of pages, and it means the
lint rule of option 2 would flag exactly those six.

**Section 3 evidence (2026-09-22), and the author theory survives with one exception.** Three more
example pages, and this time the count was run over every table in the vault by grouping contiguous
table blocks and counting separator rows *after the first in each block*, rather than per page — so
the figures below supersede the ones in the section 7 note above, which counted separator rows
against total table lines and could not tell a two-table page from a ruled one.

The full list, thirteen pages: [[08-concept-example-htmlsc-1]] 14 surplus rows,
[[10-quality-scenario-example-htmlsc-2]] 7, [[01-quality-reqs-example-1]] 6,
[[07-deployment-sample-htmlsc-1]] 5, [[12-glossary-example-htmlsc-1]] 5,
[[03-context-example-technical-1]] 5, [[08-concept-example-htmlsc-2]] 4,
[[03-context-example-business-1]] 4, [[11-risk-example-htmlsc]] 2 (one in each of its two tables),
[[03-context-example-business-2]] 1, [[tip-1-4]] 1, [[tip-3-3]] 1, [[tip-7-7]] 1.

Every example on that list is an HtmlSC example — **except one**. [[03-context-example-business-2]]
is a MaMa example, and it closes its table with the single character pair `|-`. That falsifies the
section 7 note's claim that "no TPU or MaMa example has a single one" in its strict form, and it
matters for option 2 rather than for the prose: a lint rule looking for a row of dashes and pipes
below the first separator would have to match a row one character wide, or it would miss this page.

Three tips also carry one surplus row each ([[tip-1-4]], [[tip-3-3]], [[tip-7-7]]), always a
closing rule under the last data row — a different gesture from the HtmlSC examples' rule between
*every* pair, and one no author theory explains. So the honest summary is: one author accounts for
the systematic habit, and a separate, milder habit of closing a table with a rule is spread across
three sections and two page types.

**Section 5 evidence (2026-09-22): the worst page, a third system, and two corrections.**

[[05-buildingblock-example-hsc]] carries **14 surplus separator rows across three tables** (5, 5
and 4), which ties [[08-concept-example-htmlsc-1]] for the worst page in the vault and makes it
the eighth HtmlSC example with the habit.

[[05-buildingblock-example-status]] is the correction that matters: it is a **status.arc42.org**
example, not HtmlSC, MaMa or TPU, and it puts separators between its rows too. With
[[03-context-example-business-2]] (MaMa) that is now two non-HtmlSC pages, so the section 7 note's
"it tracks the author" should be read as a strong tendency, not a rule: the habit is on eight
HtmlSC examples, one MaMa and one status page. A lint rule is therefore still worth more than a
list of pages to fix, which strengthens option 2.

Two things about the counting itself, both learned here:

- A row of *empty* cells matches "only pipes, dashes, colons and spaces" just as a rule does. The
  status example's table is `| | |` rows between separators — so of its four flagged rows only
  two are surplus separators and two are empty data rows, which belong to
  [[ISS-037-the-status-building-block-example-is-an-empty-stub|ISS-037]]. Option 2's rule must
  require at least one dash in the row or it will flag empty rows as separators.
- Kramdown does **not** require a separator row at all. [[tip-5-7]]'s two blackbox templates have
  none, and both render as proper tables — correctly, since they are label/value templates with no
  header. So the rule cannot simply treat "the first `|` row is the header"; the defect is a
  dash-row *below* a genuine separator, not the presence or absence of one.

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
