---
id: ISS-002
type: issue
title: The ADR structure proposed in section 9 omits the timestamp and the decision criteria that the tips demand
status: open
created: '2026-09-17'
updated: '2026-09-17'
sources:
- '[[SRC-009-section-9-page]]'
- '[[SRC-013-section-9-content]]'
related:
- '[[section-9]]'
- '[[tip-9-5]]'
- '[[tip-9-8]]'
- '[[09-decision-example-adr]]'
severity: major
kind: contradiction
raised-by: agent
resolved: null
---

**What's unresolved.** Section 9 reproduces the Nygard ADR structure (Title, Context, Decision,
Status, Consequences) as *the* proposal of arc42. Two tips contradict that proposal: tip 9-8 asks
for a timestamp on every decision, tip 9-5 states that these ADRs are missing the decision
criteria. The guidance itself was never updated.

**Affects.** [[section-9]], [[tip-9-5]], [[tip-9-8]], [[09-decision-example-adr]].

**Evidence.** Section 9, "Our proposal concerning decisions": the table has exactly five rows and
no date. Tip 9-8: "decisions (e.g. ADRs) should contain a timestamp attribute." Tip 9-5, heading
"(These) ADR are missing _criteria_": "I (Gernot) am missing the decision criteria ... but maybe
I'm overly peculiar in that aspect". The example goes a third way and writes the date into the
body: "Date: 2022-01-30 (we propose to always use such a timestamp!)".

**Options.**
1. Extend the table in section 9 by a *Date* row and a *Criteria* row — one edit, makes the arc42
   proposal self-consistent, but deviates from the Nygard original that is quoted.
2. Keep the quoted original and add a sentence below it that arc42 additionally recommends a
   timestamp and explicit criteria, linking tips 9-8 and 9-2 — least invasive.
3. Leave as is — the reader has to find the two tips to learn what the guidance omits.

**Resolution.** Open; needs a maintainer decision, since it changes published guidance text.
