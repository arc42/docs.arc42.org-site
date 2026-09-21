---
id: ISS-007
type: issue
title: Imported bodies carry legacy raw HTML
status: open
created: '2026-09-17'
updated: '2026-09-21'
sources:
- '[[SRC-017-section-10-content]]'
- '[[SRC-016-section-4-content]]'
- '[[SRC-015-section-1-content]]'
- '[[SRC-013-section-9-content]]'
- '[[SRC-014-section-2-content]]'
related:
- '[[tip-10-2]]'
- '[[tip-10-7]]'
- '[[tip-10-8]]'
- '[[tip-1-15]]'
- '[[01-overview-example-3]]'
- '[[01-overview-example-htmlsc-1]]'
- '[[tip-9-1]]'
- '[[tip-9-2]]'
- '[[tip-9-5]]'
- '[[tip-9-9]]'
- '[[tip-9-10]]'
- '[[09-decision-example-adr]]'
- '[[09-decision-example-htmlsc-1]]'
- '[[09-decision-example-tpu-2]]'
- '[[02-constraint-example-1]]'
- '[[04-solutionStrategy-example-htmlsc-1]]'
- '[[04-solutionStrategy-example-mama-2]]'
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

**Section 1 evidence (2026-09-21).** [[tip-1-15]] raises the stakes for option 1: its example box
is `<div class="arc42-example" markdown="1">` and the Markdown inside it — bold labels, a bullet
list, a `<small>` credit with an external anchor — renders *only* because of that kramdown
attribute. Strip or rewrite the div and the block turns into literal asterisks on the site. The
two overview examples add the pattern section 2 already showed
([[01-overview-example-3]], [[01-overview-example-htmlsc-1]]: a caption div carrying authored
text, one of them with `<i>` inside), and [[01-overview-example-htmlsc-1]] carries the familiar
`<a target="_blank" rel="noopener noreferrer nofollow">` anchors. Three sections in, the tally is:
anchors are mechanical and safe to convert, caption divs and `markdown="1"` are not.

**Section 4 evidence (2026-09-21).** Both examples carry the caption div, and here its content is
not a one-off sentence but a near-verbatim restatement of the section page's own *Contents* help
("You need a brief summary and explanation of the fundamental solution ideas and strategies…"),
identical in both files down to a trailing space. So option 1 would have to decide two questions
at once: what to do with the div, and whether the text inside it should exist twice at all.
[[04-solutionStrategy-example-htmlsc-1]] also has the familiar empty `<p></p>` first line and two
`<a target="_blank" rel="noopener noreferrer nofollow">` anchors, while
[[04-solutionStrategy-example-mama-2]] has neither — the same split as before: anchors and
`<p></p>` are mechanical, caption divs are content. Section 4's six tips contain no HTML at all.

**Section 10 evidence (2026-09-21).** The anchor pattern reaches the tips again, not just the
examples: `<a target="_blank" rel="noopener noreferrer nofollow">` appears in [[tip-10-2]] (twice),
[[tip-10-7]] and [[tip-10-8]], in all three cases wrapping a citation to an external authority —
the SEI's ATAM page, Wikipedia on Murphy's law, a blog post on utility trees. Both section 10
examples open with the empty `<p></p>`. Nothing new in kind, which is itself the finding: five
sections in, the tally from section 1 still holds — anchors are mechanical, caption divs and
`markdown="1"` are not.

**Options.**
1. Normalise mechanically in the importer (anchor → Markdown link, drop `<p></p>`), covered by a
   test — one rule for all sections, but the body is then no longer byte-identical to the site.
2. Normalise per page after cutover, when the brain owns the content.
3. Keep the HTML — kramdown renders it, and `target="_blank"` behaviour would otherwise be lost.

**Resolution.** Open; decide before more sections are ingested, since the choice applies to all of
them (option 1 would need an ADR). Section 2 is ingested and shows the rule cannot be "strip all
HTML": `<div class="arc42-example">` carries meaning that the vault has no other way to express
today.
