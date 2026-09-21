---
id: risk
type: term
title: Risk
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-018-section-11-content]]'
related:
- '[[problem]]'
- '[[technical-debt]]'
- '[[atam]]'
- '[[assumption]]'
term: Risk
aliases:
- Technical risk
legacy-tags:
- risk
- risks
home: '[[section-11]]'
---

**Definition.** Something that may damage the system or the project later, and has not happened
yet.

**In arc42.** Section 11 records the risks and technical debts the architects know about, so that
they are decided on rather than discovered. Its tips are a list of places to look, and the list is
the point: [[stakeholder|stakeholders]] of many kinds ([[tip-11-1]], a breadth-first search),
interfaces ([[tip-11-2]]), a qualitative comparison of requirements against the architecture
([[tip-11-3]]), the processes around the system ([[tip-11-4]]), the data ([[tip-11-5]]), and the
code ([[tip-11-6]]). A risk named in section 11 is not a failure of the architecture; an unnamed
one is.

**Distinguish from.** [[problem]] — a problem is present, a risk is potential; every section 11
tip looks for both in the same place. [[technical-debt]] — debt is a deliberate shortcut whose
interest is being paid; a risk may never come due at all. [[assumption]] — an assumption is what
the architecture takes for granted, and it becomes a risk exactly when it might not hold.
