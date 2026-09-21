---
id: ISS-023
type: issue
title: The TPU risk example uses bold text where it means headings
status: open
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-018-section-11-content]]'
related:
- '[[11-risk-example-tpu]]'
- '[[11-risk-example-htmlsc]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** [[11-risk-example-tpu]] is organised into four sections — hardware risks,
harddisk robustness, software risks, and more — but each one is a `**bold paragraph**`, not a
heading. The page therefore has exactly one real heading, its H2 title, so nothing below it can be
linked to, listed in a table of contents, or used as the target of a wikilink with a heading. Its sibling
[[11-risk-example-htmlsc]] uses a real `### 11.1 Technical risks` for the same job, one page over.

**Affects.** [[11-risk-example-tpu]], and [[11-risk-example-htmlsc]] as the contrast.

**Evidence.** In the TPU example: `**Hardware  Risks**` (with the double space),
`**Robustness of harddisks under harsh conditions**`, `**Software Risks**`. In the HtmlSC example:
`## 11. Risks and Technical Debts` then `### 11.1 Technical risks`. The vault's own rule makes the
difference load-bearing: CLAUDE.md says a link to a subsection uses the heading text exactly as
written, and only headings can be targets — so the TPU example's four topics are unreachable by
construction, while the HtmlSC one's are not.

**Options.**
1. Promote the four bold paragraphs to `###` headings at cut-over. Changes the rendered page (the
   text becomes larger and gains anchors) but nothing a reader would call content.
2. Leave them — the page reads fine top to bottom, and nothing links into it today.
3. Lint rule: warn when a bold-only paragraph is the first line of a block in an example, which
   would find the next one automatically. Likely noisy.

**Resolution.** Open. Not a cut-over blocker, and deliberately raised separately from
[[ISS-009-examples-start-at-different-heading-levels|ISS-009]]: that issue is about which level the
examples *start* at, this one about a page having no headings to be inconsistent with.
