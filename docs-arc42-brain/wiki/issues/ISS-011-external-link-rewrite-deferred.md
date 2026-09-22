---
id: ISS-011
type: issue
title: The generator does not rewrite external markdown links to target-blank anchors
status: open
created: '2026-09-18'
updated: '2026-09-22'
sources: []
related:
- '[[section-9]]'
severity: minor
kind: contradiction
raised-by: agent
resolved: null
---

**What's unresolved.** Brain spec §4.4 says the generator rewrites every absolute `http(s)://`
markdown link into `<a target="_blank" rel="noopener noreferrer nofollow">` "so the bootstrap parity
holds". The corpus has both forms: section 9's guidance uses plain markdown links (three of them),
while tips and examples carry raw `<a target="_blank" …>` tags (ISS-007). Rewriting would break
parity on section 9, the section that gates phase 2, so the phase-2 generator passes every link
through unchanged.

**Affects.** [[section-9]] now; every section page with plain external links at its cut-over.

**Evidence.** `_pages/section-9.md`: `[architecture decision record](https://thinkrelevance.com/…)`,
`[Nygard 2011](https://cognitect.com/…)`, `[ADR Github collection](https://adr.github.io/)`.

**Options.**
1. Keep pass-through; decide with ISS-007 whether bodies should hold plain markdown links only and
   let the site's layout or a small script open external links in a new tab — no parity break.
2. Implement the rewrite after all section cut-overs, as one deliberate parity break with its own
   PR — every page's HTML changes once.
3. Drop the target-blank convention for markdown links — raw `<a>` tags stay as they are.

**Resolution.**

**Resolution.** Open, and option 1 is the state on disk: the generator passes every link through
unchanged, so no page's HTML has moved. Verified 2026-09-22 — `braingen` contains no occurrence of
`noopener`, so the spec §4.4 rewrite is unimplemented rather than partly implemented, and spec and
code still disagree. This is one question with
[[ISS-007-legacy-raw-html-in-imported-bodies|ISS-007]], not two: that issue asks what form an
external link takes *in a body*, this one what the generator does with it on the way out, and
neither can be answered without the other. Whichever way it goes, the spec clause has to be amended
or the rewrite written — leaving both as they are is the one outcome that keeps the contradiction.
