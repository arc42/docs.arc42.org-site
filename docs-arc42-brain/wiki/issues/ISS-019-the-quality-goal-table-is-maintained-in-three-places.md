---
id: ISS-019
type: issue
title: The quality-goal table is maintained in three places
status: open
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-017-section-10-content]]'
- '[[SRC-016-section-4-content]]'
- '[[SRC-004-section-4-page]]'
related:
- '[[tip-10-8]]'
- '[[section-4]]'
- '[[tip-4-2]]'
- '[[tip-4-3]]'
severity: minor
kind: risk
raised-by: agent
resolved: null
---

**What's unresolved.** The same four-column table — *Quality goal · Scenario · Solution approach ·
Link to Details* — is written out three times: in section 4's *Form*, in [[tip-4-2]] and again in
[[tip-4-3]]. All three copies are byte-identical today, including the two placeholder rows and the
`_&lt;Q-goal 1>_` escaping. Nothing keeps them that way: a fifth column added to one copy leaves
the other two silently stale, and the brain has no rule that would catch it.

**Affects.** [[section-4]], [[tip-4-2]], [[tip-4-3]].

**Evidence.** [[tip-4-2]] introduces the table as its actual advice ("Describe the solution
approaches as a table containing the following columns"), and its four bullets explain the four
columns. [[tip-4-3]] then says "See the table below (already shown in [tip 4-2](/tips/4-2))" and
repeats it in full — the tip acknowledges the duplication in prose and duplicates anyway. Section
4's *Form* has the third copy, introduced with "You might use a list of solution-approaches or a
table similar to the following". The advice in the three places genuinely differs (a form, a
tabular form, and quality requirements as the driving force); only the illustration is shared.

**Section 10 evidence (2026-09-21).** A fourth copy of the table, and this one is not identical:
[[tip-10-8]] uses *Quality goal · Scenario · Solution approach · **Risk*** — tip 4-2's four
columns with the last one swapped — and says so itself ("similar to the structure proposed in
[tip 4-2](/tips/4-2)"). That changes the shape of the problem: it is not one block duplicated
three times but a family of variants, so option 3 (a shared snippet) would need parameters, and
option 4 (a lint rule for identical blocks) would not catch this one at all. A single canonical
table with a documented variation is the only option that fits both.

**Options.**
1. Leave all three — a reader of one page sees the table without following a link, which is why
   it was copied in the first place. The drift risk stays.
2. Keep the table in [[tip-4-2]] only, and have [[tip-4-3]] and the section's *Form* link to it.
   Costs the standalone readability of two pages, and changes what the site serves for three URLs.
3. One shared include. No mechanism for this exists: the brain forbids Liquid in `wiki/`
   (ADR-0005), and the only directives are `%% examples: … %%` and `%% examples-link %%`. A
   snippet directive would have to be designed, emitted for the site, and linted.
4. A lint rule that flags identical multi-line blocks across pages — catches the drift instead of
   preventing it, and would also fire on the three tables in [[tip-1-4]] and the HtmlSC quality
   example (see [[ISS-016-repeated-separator-rows-in-tables|ISS-016]]).

**Resolution.** Open. Not a cut-over blocker: the site already serves all three copies, so
generating them changes nothing a reader sees. Decide before section 5, whose tips carry the same
`table` tag (tip 5-7, not ingested yet), in case the duplication is wider than section 4.
