---
id: ISS-007
type: issue
title: Imported bodies carry legacy raw HTML
status: open
created: '2026-09-17'
updated: '2026-09-20'
sources:
- '[[SRC-013-section-9-content]]'
- '[[SRC-014-section-2-content]]'
related:
- '[[tip-9-1]]'
- '[[tip-9-2]]'
- '[[tip-9-5]]'
- '[[tip-9-9]]'
- '[[tip-9-10]]'
- '[[09-decision-example-adr]]'
- '[[09-decision-example-htmlsc-1]]'
- '[[09-decision-example-tpu-2]]'
- '[[02-constraint-example-1]]'
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
[[09-decision-example-adr]], [[09-decision-example-htmlsc-1]], [[09-decision-example-tpu-2]],
[[02-constraint-example-1]].

**Evidence.** `grep -ln '<a \|<p>' wiki/tips/tip-9-*.md wiki/examples/09-*.md` lists exactly these
eight pages; `wiki/sections/section-9.md` is free of them because its external links are Markdown.
The anchor attributes are uniform, which suggests they were generated once and are not authored
per link. The empty `<p></p>` is an artifact of the examples being pulled into a section page by
the Jekyll include.

Section 2, ingested 2026-09-20, adds a variant that option 1 must not strip:
[[02-constraint-example-1]] opens with `<div class="arc42-example">`, a `<br>`, a sentence of
*content* ("Key constraints can often be explained as simple enumeration in plain text.") and
`</div>`. Unlike `<p></p>` this markup is load-bearing — the class is what styles the caption box
on the site, and the sentence inside it is authored text, not an artifact. A mechanical
normaliser therefore needs a rule per HTML construct, not one blanket "strip HTML" pass. The five
section 2 tips contain no HTML at all.

**Options.**
1. Normalise mechanically in the importer (anchor → Markdown link, drop `<p></p>`), covered by a
   test — one rule for all sections, but the body is then no longer byte-identical to the site.
2. Normalise per page after cutover, when the brain owns the content.
3. Keep the HTML — kramdown renders it, and `target="_blank"` behaviour would otherwise be lost.

**Resolution.** Open; decide before more sections are ingested, since the choice applies to all of
them (option 1 would need an ADR). Section 2 is ingested and shows the rule cannot be "strip all
HTML": `<div class="arc42-example">` carries meaning that the vault has no other way to express
today.
