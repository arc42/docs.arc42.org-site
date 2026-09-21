---
id: external-interface
type: term
title: External interface
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-018-section-11-content]]'
related:
- '[[interface]]'
term: External interface
aliases: []
legacy-tags:
- external-interface
home: '[[section-3]]'
---

**Definition.** An interface between the system and a communication partner that is not part of
it — a neighbouring system, a user, a device.

**In arc42.** Section 3 exists for these: delimiting the system from its communication partners
"thereby specifies the external interfaces", as the section page puts it. They are the interfaces
the architects cannot change alone, which is what makes them worth their own name and what makes
[[tip-11-2]] point at them first when looking for problems and [[risk|risks]].

**Distinguish from.** [[interface]] — the general term, and the one section 5 uses for the
interfaces between a system's own building blocks. The site tags many pages with both, because an
external interface is also an interface.
