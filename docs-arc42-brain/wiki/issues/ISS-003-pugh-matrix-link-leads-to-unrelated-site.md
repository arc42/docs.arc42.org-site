---
id: ISS-003
type: issue
title: The Pugh matrix link in tip 9-2 now leads to an unrelated site
status: open
created: '2026-09-17'
updated: '2026-09-17'
sources:
- '[[SRC-013-section-9-content]]'
related:
- '[[tip-9-2]]'
severity: major
kind: risk
raised-by: agent
resolved: null
---

**What's unresolved.** Tip 9-2 recommends the Pugh matrix and links
`https://www.decision-making-confidence.com/pugh-matrix.html`. That domain no longer serves the
article; it redirects to a site about psychopaths and narcissists. The link must be replaced or
removed, which is a content edit and therefore not part of this ingest.

**Affects.** [[tip-9-2]].

**Evidence.** Checked 2026-09-17:
`curl -sI https://www.decision-making-confidence.com/pugh-matrix.html` → `HTTP/2 301`,
`location: http://www.psychobegone.com`; following the redirect gives `200` with the page title
"Psychopaths and narcissists, what you need to know!".

**Options.**
1. Replace with a stable reference (e.g. the Wikipedia article on the Pugh matrix / decision-matrix
   method) — keeps the recommendation, loses the original author's page.
2. Drop the paragraph — the tip stands without it ("No guarantee from our side...").
3. Link an archived snapshot (web.archive.org) — preserves the exact page that was recommended.

**Resolution.** Open.
