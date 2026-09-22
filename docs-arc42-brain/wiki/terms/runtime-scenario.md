---
id: runtime-scenario
type: term
title: Runtime scenario
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[runtime-view]]'
- '[[quality-scenario]]'
term: Runtime scenario
aliases: []
legacy-tags:
- runtime-scenario
home: '[[section-6]]'
---

**Definition.** One named sequence of interactions between building blocks, followed from its
trigger to its result.

**In arc42.** The content of section 6, borrowed here by section 5: [[tip-5-23]] observes that
some interfaces are not a single call but a handshake or a protocol, and says those should be
described as runtime scenarios and referenced from the documentation of every building block that
takes part. So a scenario is the place an [[interface]] goes when it is too conversational to fit
in a [[blackbox]] table.

**Distinguish from.** [[quality-scenario]] — the other thing arc42 calls a scenario, and the
source of a live ambiguity: the site tags both kinds `scenario`, so the same tag means a quality
scenario on the section 1 and 10 pages and a runtime scenario here and throughout section 6.
Each page is mapped by what it means, which is recorded in
[[ISS-034-the-site-tag-scenario-means-two-different-things|ISS-034]]. A quality scenario states a
required reaction to a stimulus and is a requirement; a runtime scenario describes what the built
system actually does.
