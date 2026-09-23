---
id: ISS-002
type: issue
title: The ADR structure proposed in section 9 omits the timestamp and the decision
  criteria that the tips demand
status: resolved
created: '2026-09-17'
updated: '2026-09-23'
sources:
- '[[SRC-009-section-9-page]]'
- '[[SRC-013-section-9-content]]'
related:
- '[[section-9]]'
- '[[tip-9-5]]'
- '[[tip-9-8]]'
- '[[09-decision-example-adr]]'
- '[[tip-9-2]]'
- '[[tip-9-8]]'
severity: major
kind: contradiction
raised-by: agent
resolved: '2026-09-23'
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

**Resolution (2026-09-23): resolved, by option 1 with the criteria row marked optional.**

The facilitator's ruling: add the date, and add the criteria too but mark it as optional. The
table now carries both, each labelled *(an arc42 addition, not part of the original Nygard
structure)* so the attribution two lines above — "thanx to Michael Nygard for this proposal" —
stays true:

- `| Date |` after *Title*, where the ADR example already puts it, with tip 9-8's own reason
  ("in the future it might be important to know at what time a certain decision was made") and a
  link to [[tip-9-8]].
- `| (optional) Criteria |` after *Decision*, linking [[tip-9-2]].

The two rows differ in force because the two tips do. [[tip-9-8]] states its recommendation flat
— "decisions (e.g. ADRs) should contain a timestamp attribute" — and the ADR example backs it
with "(we propose to always use such a timestamp!)". [[tip-9-5]] hedges its own: "I (Gernot) am
missing the decision criteria ... but maybe I'm overly peculiar in that aspect". A row marked
optional says exactly that, and `(optional)` is the site's own convention for it — [[tip-5-7]]'s
blackbox template uses it four times, and section 7's page for a whole heading.

**What this also closed.** [[09-decision-example-adr]] wrote the date into its body with the aside
"(we propose to always use such a timestamp!)", which this issue recorded as the example "going a
third way". It is no longer a third way: the example now demonstrates the proposal.

**What it cost, and what it bought.** This was the first correction the brain has ever made to a
published body, and it did not work: `test_parity_against_the_ingested_originals` compares every
ingested section against the immutable copy in `raw/ingested/`, so a deliberate edit is
indistinguishable to it from an emitter regression. That test is, in its own words, "the only
guard that survives cut-over". The fix is
**ADR-0006** (`_system/adr/0006-approved-body-edits.md`): a correction is approved one change at a
time by a human who has seen the diff (`make brain-approve-edit`), and the approval — keyed by a
fingerprint of the body it was shown — is appended to `_system/approved-body-edits.tsv`. This
issue's edit is its first entry.

That unblocks every other content fix the vault has queued:
[[ISS-035-tip-5-23-sends-readers-to-section-7-for-runtime-scenarios|ISS-035]],
[[ISS-036-two-section-5-tips-ship-unfinished-text|ISS-036]],
[[ISS-041-the-sequence-diagram-on-tips-6-6-and-6-11-contradicts-itself|ISS-041]] and the roughly
ninety corrections of
[[ISS-044-one-editorial-pass-owns-the-decision-ten-issues-ask-for|ISS-044]], none of which could
have been made before today.
