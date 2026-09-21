---
id: plantuml
type: term
title: PlantUML
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-015-section-1-content]]'
related:
- '[[activity-diagram]]'
- '[[functional-requirement]]'
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
[[activity-diagram]], which is the point: same picture, different source form. The site also tags
tip 8-7 with it, in a section not yet ingested.

**Distinguish from.** [[activity-diagram]] — PlantUML is the tool, the activity diagram is what it
draws. Being text, its source belongs in version control next to the code, which is the practical
argument [[tip-1-9]] makes for it.

**Note on the tag.** The site spells this tag `plantUML`, the only mixed-case tag in the
vocabulary; the slug follows the vault's kebab convention, so the emitted tag is `plantuml`. The
old spelling is kept in `legacy-tags` so it still resolves.
