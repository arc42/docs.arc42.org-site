---
id: ISS-007
type: issue
title: Imported bodies of section 9 carry legacy raw HTML
status: open
created: '2026-09-17'
updated: '2026-09-17'
sources:
- '[[SRC-013-section-9-content]]'
related:
- '[[tip-9-1]]'
- '[[tip-9-2]]'
- '[[tip-9-5]]'
- '[[tip-9-9]]'
- '[[tip-9-10]]'
- '[[09-decision-example-adr]]'
- '[[09-decision-example-htmlsc-1]]'
- '[[09-decision-example-tpu-2]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Eight of the thirteen imported pages contain raw HTML in bodies that the
vault expects to be Markdown: `<a target="_blank" rel="noopener noreferrer nofollow" href="...">`
for every external link, `<br>` at the end of quoted lines in tip 9-5, and an empty `<p></p>` as
the first line of all three examples. The brain's convention is "Markdown only", but rewriting the
bodies would end the verbatim guarantee of this ingest.

**Affects.** [[tip-9-1]], [[tip-9-2]], [[tip-9-5]], [[tip-9-9]], [[tip-9-10]],
[[09-decision-example-adr]], [[09-decision-example-htmlsc-1]], [[09-decision-example-tpu-2]].

**Evidence.** `grep -ln '<a \|<p>' wiki/tips/tip-9-*.md wiki/examples/09-*.md` lists exactly these
eight pages; `wiki/sections/section-9.md` is free of them because its external links are Markdown.
The anchor attributes are uniform, which suggests they were generated once and are not authored
per link. The empty `<p></p>` is an artifact of the examples being pulled into a section page by
the Jekyll include.

**Options.**
1. Normalise mechanically in the importer (anchor → Markdown link, drop `<p></p>`), covered by a
   test — one rule for all sections, but the body is then no longer byte-identical to the site.
2. Normalise per page after cutover, when the brain owns the content.
3. Keep the HTML — kramdown renders it, and `target="_blank"` behaviour would otherwise be lost.

**Resolution.** Open; decide before more sections are ingested, since the choice applies to all of
them (option 1 would need an ADR).
