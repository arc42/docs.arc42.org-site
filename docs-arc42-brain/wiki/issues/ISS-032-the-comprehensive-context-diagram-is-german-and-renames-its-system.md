---
id: ISS-032
type: issue
title: The comprehensive context diagram is labelled in German and renames its own system
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-022-section-3-content]]'
related:
- '[[tip-3-2]]'
- '[[tip-3-8]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** `assets/sections/03/big-context.png` is the site's showpiece context
diagram — it appears on two pages — and roughly half of its labels are German. The same drawing
exists in a second, English version under a different system name, and [[tip-3-8]] shows both,
one after the other, without saying they are the same system.

**Affects.** [[tip-3-2]], [[tip-3-8]].

**Evidence.** In `big-context.png` the system is named **VENOM** and its neighbours read
*Zahlungsabwicklung*, *Bonitätsprüfung*, *Produkthersteller und -lieferanten*, *Exportkontrolle*,
*Marktforschung*, *Transportunternehmen*, *Telephone, Call-Center*, *Kredit-Rating*. The port
labels around the boundary — Payment, Rating, ECI, BI Data, Accounting, Market Research, Transport
Logistics, UIs, Product, CTI — are English.

`context-with-ports.png`, shown directly above it in [[tip-3-8]], has that same ring of ports in
that same order, but the box is labelled **Big System** and every label is English. So the two
figures are one diagram at two levels of detail, and a reader is given no way to know it: the
names differ, the languages differ, and the text between them says only "below you find the more
extensive version with ports and explicit neighbour systems".

**Options.**
1. Redraw `big-context.png` in English and name the system *Big System*, matching its twin. The
   most work, and the only option that makes [[tip-3-8]]'s two figures read as one story.
2. Relabel only the system box, so at least the name is consistent, and leave the German
   neighbours — which are, after all, plausible names for a German company's neighbours.
3. Leave the images and fix the prose instead: say in [[tip-3-8]] that the second figure is the
   same system drawn in full. Cheapest, and it removes the reader's confusion without touching a
   binary asset.

**Resolution.** Open. Second instance of German surviving into English content, after
[[ISS-026-german-field-names-in-the-hospital-data-model|ISS-026]] — but that one is text in a
PlantUML block a reader can edit, and this one is a PNG. Note also that this is now the third
distinct German trace in the site, alongside the four constructions in
[[ISS-030-section-3-bodies-carry-editorial-defects|ISS-030]].
