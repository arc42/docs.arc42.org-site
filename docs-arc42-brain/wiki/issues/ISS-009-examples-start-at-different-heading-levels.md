---
id: ISS-009
type: issue
title: The three decision examples start at different heading levels
status: open
created: '2026-09-17'
updated: '2026-09-17'
sources:
- '[[SRC-013-section-9-content]]'
related:
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

**Options.**
1. Demote the ADR example to H2 — one character, makes the three consistent.
2. Let the generator emit the heading from `title` and drop it from the bodies — consistent for
   every section, but changes every example page.
3. Leave as is.

**Resolution.** Open.
