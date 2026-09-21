---
id: technical-debt
type: term
title: Technical debt
status: review
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-018-section-11-content]]'
related:
- '[[risk]]'
- '[[problem]]'
term: Technical debt
aliases:
- Technical debts
legacy-tags:
- technical-debt
home: '[[section-11]]'
---

**Definition.** A shortcut taken knowingly in the architecture or the code, whose cost has to be
paid back later with interest.

**In arc42.** Section 11 is titled "Risks and Technical Debt", so debt sits beside risk by name,
and both example pages use the plural heading "11. Risks and Technical Debts". [[tip-11-3]] is the
tip that finds it: comparing the requirements against what was actually built is what turns a
vague unease into a named debt with a price. arc42 asks for the debt to be written down, not
repaid — the decision whether to repay it belongs to the people reading section 11.

**Distinguish from.** [[problem]] — every debt is a kind of problem, but one the team chose and
can justify; a problem in general may be nobody's decision. [[risk]] — a risk might never come
due; debt is accruing interest now.
