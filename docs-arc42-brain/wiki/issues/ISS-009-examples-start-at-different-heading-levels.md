---
id: ISS-009
type: issue
title: The three decision examples start at different heading levels
status: open
created: '2026-09-17'
updated: '2026-09-21'
sources:
- '[[SRC-020-section-8-content]]'
- '[[SRC-018-section-11-content]]'
- '[[SRC-016-section-4-content]]'
- '[[SRC-015-section-1-content]]'
- '[[SRC-013-section-9-content]]'
related:
- '[[08-concept-example-tpu-1]]'
- '[[08-concept-example-tpu-2]]'
- '[[11-risk-example-tpu]]'
- '[[04-solutionStrategy-example-htmlsc-1]]'
- '[[04-solutionStrategy-example-mama-2]]'
- '[[01-overview-example-3]]'
- '[[01-overview-example-htmlsc-1]]'
- '[[09-decision-example-adr]]'
- '[[09-decision-example-htmlsc-1]]'
- '[[09-decision-example-tpu-2]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** The ADR example opens with `# 9. Architecture Decisions` (H1), the other two
with `## 9. Architecture Decisions` (H2). All three are rendered inside section 9 through the same
`%% examples: decisions %%` directive, so the heading hierarchy of the rendered section page is
inconsistent, and the generator of phase 2 will reproduce that inconsistency.

**Affects.** [[09-decision-example-adr]], [[09-decision-example-htmlsc-1]],
[[09-decision-example-tpu-2]].

**Evidence.** `09-decision-example-adr` line 1 of the body after `<p></p>`: `# 9. Architecture
Decisions`; `09-decision-example-htmlsc-1` and `09-decision-example-tpu-2`: `## 9. Architecture
Decisions`. The `title` frontmatter of all three already carries the name, so the in-body heading
may be redundant anyway.

**Section 1 evidence (2026-09-21).** All four section 1 examples open at H2, so the *entry* level
is consistent here — but the two overview examples disagree one level down, which is the same
inconsistency displaced: [[01-overview-example-3]] uses `## 1. Introduction` followed by
`## 1.1 Requirements` (both H2, so the subsection is a sibling of its parent), while
[[01-overview-example-htmlsc-1]] uses `## 1. Introduction` then `### 1.1 Overview for HTML Sanity
Checker`. Option 2 — emit the heading from `title` and let the generator own the levels — would
fix the entry level but not this, since the inner headings are part of the example's content.

**Section 4 evidence (2026-09-21).** The first pair that agrees exactly: both
[[04-solutionStrategy-example-htmlsc-1]] and [[04-solutionStrategy-example-mama-2]] open at
`## 4. Solution Strategy` and neither has an inner heading at all, so there is nothing left to
disagree about. That is evidence for option 2 being cheap here and expensive in section 1, and it
confirms the inconsistency is not systematic — it is per example, which is why a generator-owned
entry heading only solves the part that is.

**Section 11 evidence (2026-09-21).** Both examples open at `## 11. Risks and Technical Debts`,
so the entry level agrees — but one level down they diverge more sharply than section 1's pair
did: [[11-risk-example-htmlsc]] uses `### 11.1 Technical risks` while
[[11-risk-example-tpu]] has no headings at all below its title, only bold paragraphs
([[ISS-023-tpu-risk-example-uses-bold-text-as-headings|ISS-023]]). Option 2 (generate the entry
heading from `title`) would still leave these two pages structured differently, which is now
confirmed for the third section in a row.

**Section 8 evidence (2026-09-21).** The sharpest case yet, and a new kind:
[[08-concept-example-tpu-2]] has **no top-level heading at all** — it opens directly at
`### 8.2 Event Handling`, while its sibling [[08-concept-example-tpu-1]] opens at
`## 8. Crosscutting Concepts` and then `### 8.1 Domain Entity Model`. So the four section 8
examples show three different entry levels between them (H2+H3, H2 only, H3 only). That is an
argument *for* option 2: a generator that emits the entry heading from `title` would give tpu-2
the H2 it is missing, which no per-page fix would generalise to.

**Options.**
1. Demote the ADR example to H2 — one character, makes the three consistent.
2. Let the generator emit the heading from `title` and drop it from the bodies — consistent for
   every section, but changes every example page.
3. Leave as is.

**Resolution.** Open.
