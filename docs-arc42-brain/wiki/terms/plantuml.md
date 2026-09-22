---
id: plantuml
type: term
title: PlantUML
status: review
created: '2026-09-21'
updated: '2026-09-22'
sources:
- '[[SRC-020-section-8-content]]'
- '[[SRC-015-section-1-content]]'
- '[[SRC-024-section-6-content]]'
related:
- '[[activity-diagram]]'
- '[[functional-requirement]]'
- '[[sequence-diagram]]'
term: PlantUML
aliases: []
legacy-tags:
- plantUML
home: '[[section-1#1.1 Requirements Overview]]'
---

**Definition.** An open-source tool that renders diagrams from a plain-text description.

**In arc42.** [[tip-1-9]] uses it as the example of a semi-formal notation for functional
requirements: activities are written between `:` and `;`, branches read as pseudo code, and the
tool renders the result — "that way you combine the benefits of plain text with graphical
representation". The diagram it produces in that tip is the same
`../assets/sections/01/simple-activity.png` that [[tip-1-6]] shows as a hand-drawn
[[activity-diagram]], which is the point: same picture, different source form.

[[tip-8-7]] is the other page the site tags, and it goes further than any other tip in the
vault: the hospital data model it shows is followed by its **complete PlantUML source**, some
sixty lines in a fenced block, so the reader can regenerate the picture. That is the argument for
the tool made by demonstration rather than by claim.

**Distinguish from.** [[activity-diagram]] — PlantUML is the tool, the activity diagram is what it
draws. Being text, its source belongs in version control next to the code, which is the practical
argument [[tip-1-9]] makes for it.

**Note on the tag.** The site spells this tag `plantUML`, the only mixed-case tag in the
vocabulary; the slug follows the vault's kebab convention, so the emitted tag is `plantuml`. The
old spelling is kept in `legacy-tags` so it still resolves. Section 1's cut-over left the site
carrying both names — `plantUML` on tip 8-7, `plantuml` on tip 1-9 — and **section 8's cut-over
ends that**: 8-7 is the only other page, so `plantUML` goes to zero and `plantuml` to two.
