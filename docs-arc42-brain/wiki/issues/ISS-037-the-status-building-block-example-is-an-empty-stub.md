---
id: ISS-037
type: issue
title: The status.arc42.org building block example publishes an empty table
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[05-buildingblock-example-status]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** [[05-buildingblock-example-status]] is one of four worked examples of the
building block view, and it consists of a diagram, an apology and a table with two blank rows.

**Affects.** [[05-buildingblock-example-status]].

**Evidence.** After the level-1 image the whole page reads:

> **Contained Blackboxes:**
>
> (left our for brevity)

followed by a two-column table whose only content is `| | |` twice, with separator rows between
them. Rendered, that is a heading, a sentence with a typo for "left out", and an empty ruled box.

The page is nonetheless useful as it stands — it is the only example of the *minimal* case that
[[tip-5-3]] argues for, a level-1 whitebox and nothing else — so the diagram is doing real work.
The empty table is not: it promises the blackbox descriptions that [[tip-5-5]] and [[tip-5-7]]
call the important part, and then withholds them.

**Options.**
1. Delete the "Contained Blackboxes" heading and the empty table, keep the diagram, and let the
   page be honestly what it is: the smallest building block view on the site. Fixes the typo by
   removing the sentence that contains it.
2. Fill the table from the diagram — status.arc42.org is the project's own system, so the
   information is available — and the example becomes a fourth complete one.
3. Leave it.

**Resolution.** Open. Option 1 is one deletion and makes the page consistent with
[[tip-5-3]]; option 2 is more work but would give the section an example of a *small* system
documented properly, which the three others (HtmlSC with three levels, TPU with two) do not
provide.
