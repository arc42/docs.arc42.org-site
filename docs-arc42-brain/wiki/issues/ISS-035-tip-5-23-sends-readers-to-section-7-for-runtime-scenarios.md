---
id: ISS-035
type: issue
title: Tip 5-23 sends readers to section 7 for runtime scenarios, which live in section 6
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[tip-5-23]]'
severity: major
kind: contradiction
raised-by: agent
resolved: null
---

**What's unresolved.** [[tip-5-23]] tells the reader to describe multi-step interfaces as runtime
scenarios and links the wrong section. Runtime scenarios are arc42 section 6; the tip points at
section 7, which is the [[deployment-view]].

**Affects.** [[tip-5-23]].

**Evidence.** The body reads: "You can describe or specify such interactions by runtime scenarios,
[arc42-section 7](/section-7)." The link text and the URL agree with each other and both are
wrong. [[section-6]] is "6 - Runtime view"; [[section-7]] is "7 - Deployment view". The tip's own
tags confirm the intent — it carries `runtime-scenario`, the tag that otherwise appears only on
section 6 tips.

This is not a typo of the [[ISS-038-section-5-bodies-carry-editorial-defects|ISS-038]] kind: a
reader who follows it lands on a page about infrastructure and finds nothing about scenarios, and
the error is in a tip whose whole content is "go and read about this elsewhere". It is the first
factually wrong cross-section reference found in ten ingested sections — every other one in
[[ISS-006-cross-tip-references-are-hard-coded-urls|ISS-006]] points where it says it points.

**Options.**
1. Fix it at cut-over to `[[section-6]]`, which is also the wikilink conversion ISS-006 wants.
2. Fix it on the site now and re-run `brain-raw`, since a wrong link is worse than a stale brain.
3. Leave it.

**Resolution.** Open, but it should not wait for a general pass: option 1 or 2, not 3. Note that
fixing it needs no new page — [[section-6]] has existed since the bootstrap — so the correction
is available whether or not section 6 has been ingested.
