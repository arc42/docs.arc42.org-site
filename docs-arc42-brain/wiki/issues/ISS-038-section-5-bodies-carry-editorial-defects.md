---
id: ISS-038
type: issue
title: Section 5 bodies carry editorial defects
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[tip-5-1]]'
- '[[tip-5-6]]'
- '[[tip-5-9]]'
- '[[tip-5-10]]'
- '[[tip-5-11]]'
- '[[tip-5-13]]'
- '[[tip-5-17]]'
- '[[tip-5-19]]'
- '[[tip-5-22]]'
- '[[tip-5-27]]'
- '[[05-buildingblock-example-status]]'
- '[[05-buildingblock-example-tpu-lev-1]]'
- '[[05-buildingblock-example-tpu-lev-2]]'
- '[[ISS-044-one-editorial-pass-owns-the-decision-ten-issues-ask-for]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Sixteen defects in thirteen pages — the largest crop of any section, which
is expected from the largest section, but the rate is also the highest: a defect every two pages.
Two of them are German words left inside English sentences.

**Affects.** [[tip-5-1]], [[tip-5-6]], [[tip-5-9]], [[tip-5-10]], [[tip-5-11]], [[tip-5-13]],
[[tip-5-17]], [[tip-5-19]], [[tip-5-22]], [[tip-5-27]],
[[05-buildingblock-example-status]], [[05-buildingblock-example-tpu-lev-1]],
[[05-buildingblock-example-tpu-lev-2]].

**Evidence — German again.**

- [[tip-5-13]]: a heading, "Keep the mapping of code **und** building blocks straightforward".
- [[05-buildingblock-example-tpu-lev-1]]: "can be accessed **as well** internally **as**
  externally" — the German *sowohl … als auch* construction, which in English needs "both … and".

The untranslated paragraph in [[tip-5-24]] and the TODO in [[tip-5-1]] are kept apart in
[[ISS-036-two-section-5-tips-ship-unfinished-text|ISS-036]], because they are unfinished editing
rather than slips.

**Evidence — the rest.**

- [[tip-5-1]]: "explain **responsibiliy** and interfaces".
- [[tip-5-6]] and [[tip-5-27]]: "without **detailling**" and "refined and **detailled**" — the
  same misspelling twice in one section, the third repeated misspelling in the vault after
  `ubiqitous` and `neccessary`.
- [[tip-5-9]]: "should be constructed or **build**" — built.
- [[tip-5-10]]: "**refering** to a crosscutting concept", and a guillemet that never opens —
  "elements of type X-service**»**" where the first mention writes «X-service» correctly.
- [[tip-5-11]]: "obey the important **consisteny** rule".
- [[tip-5-13]]: "Somebody has **accidently** put too many files".
- [[tip-5-17]]: a quotation mark with no opening partner — `_belong_ together".`
- [[tip-5-19]]: "Therefore **its** included in the building block view" — it's.
- [[tip-5-22]]: three in one page — "an additional **purpuse**", "(**programatically**) created",
  "_**behavious** driven_ manner" — plus "One possible framework supporting BDD **this** is".
- [[05-buildingblock-example-status]]: "(left **our** for brevity)" — out; see
  [[ISS-037-the-status-building-block-example-is-an-empty-stub|ISS-037]], whose option 1 removes
  the sentence entirely.
- [[05-buildingblock-example-tpu-lev-2]]: "handles **layouting formatting** of documents" (a
  missing "and"), and "print **thedocuments** out".

**Options.**
1. Fix them at cut-over, in the brain, as part of owning the content.
2. Fix them on the site now, before cut-over, and re-run `brain-raw` so the brain stays verbatim.
3. Leave them.

**Resolution.** Open, the ninth section with a typo issue of its own, and the last one that can be
raised: with section 5 ingested, only section 6 has never been read. That makes the vault-wide
pass proposed in [[ISS-030-section-3-bodies-carry-editorial-defects|ISS-030]] a decision that can
now be taken on almost complete information — nine issues, one per section, describing one job.
`detailling` joins `ubiqitous` and `neccessary` as a misspelling that appears in more than one
place and that no per-section reading would catch.

**The decision this issue asks for lives in [[ISS-044-one-editorial-pass-owns-the-decision-ten-issues-ask-for|ISS-044]]** (2026-09-22). Ten per-section issues each asked the same question — correct in the brain, or stay byte-faithful until cut-over? — and none of them owned the answer. This one keeps its own defect list, which is what the eventual pass works from.
