---
id: runtime-scenario
type: term
title: Runtime scenario
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
- '[[SRC-024-section-6-content]]'
related:
- '[[runtime-view]]'
- '[[quality-scenario]]'
- '[[activity-diagram]]'
- '[[sequence-diagram]]'
term: Runtime scenario
aliases: []
legacy-tags:
- runtime-scenario
home: '[[section-6]]'
---

**Definition.** One named sequence of interactions between building blocks, followed from its
trigger to its result.

**In arc42.** The unit section 6 is made of, and the thing every one of its eleven tips is about.
[[tip-6-1]] gives the rule that makes a scenario architectural rather than procedural: its steps
must be mapped onto elements of the [[building-block|building block view]], which distinguishes a
runtime scenario from a *required function* — a sequence the system must perform, regardless of
which part performs it. Assigning that mapping is the architect's work, and the notation either
does it for you ([[sequence-diagram]], swimlanes on an [[activity-diagram]]) or leaves it to be
done by hand. [[tip-6-5]] then makes the deflationary point the section keeps returning to: the
value is mostly in drawing the scenario, not in keeping it. Section 5 borrows the term once —
[[tip-5-23]] sends interfaces that are a handshake rather than a single call here, so a scenario
is also where an [[interface]] goes when it is too conversational to fit in a [[blackbox]] table.

**On the tag.** The site tags both kinds of scenario `scenario`, and the ambiguity is now fully
measured: of its sixteen pages, eleven are section 6 and one is [[tip-5-23]] — runtime scenarios,
mapped here — and the remaining four are section 10 tips, which are quality scenarios and belong
to [[quality-scenario]]. Each page is mapped by what it means, under the policy recorded in
[[ISS-034-the-site-tag-scenario-means-two-different-things|ISS-034]]. Section 6's cut-over is the
one that resolves it, and the resolution is that the tag disappears: the four section 10 pages
already emit `quality-scenario`, so once the eleven here emit `runtime-scenario` nothing emits the
bare `scenario` at all. The ambiguous name is replaced by the two unambiguous ones.

**Distinguish from.** [[quality-scenario]] — a required reaction to a stimulus, which is a
requirement about a system that may not exist yet; a runtime scenario describes what the built
system actually does. [[runtime-view]] — the section; a scenario is one path through it.
