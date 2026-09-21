---
id: ISS-001
type: issue
title: Does the legacy tag `quality` on tips 9-1 and 9-4 mean the arc42 quality requirement?
status: open
created: '2026-09-17'
updated: '2026-09-21'
sources:
- '[[SRC-015-section-1-content]]'
- '[[SRC-013-section-9-content]]'
related:
- '[[tip-1-11]]'
- '[[tip-1-14]]'
- '[[tip-9-1]]'
- '[[tip-9-4]]'
- '[[quality-requirement]]'
severity: minor
kind: ambiguity
raised-by: agent
resolved: null
---

**What's unresolved.** The legacy tag `quality` sits on tip 9-1 and tip 9-4. The ingest mapped it
to the term [[quality-requirement]] (the arc42 concept of section 10), but on tip 9-4 it may well
have meant "the quality of the decision documentation" instead.

**Affects.** [[tip-9-1]], [[tip-9-4]], [[quality-requirement]].

**Evidence.** Tip 9-1 lists "influencing important quality attributes" as a reason to document a
decision — there the arc42 concept fits, and section 10's motivation confirms it ("quality
requirements will have a lot of influence on architectural decisions"). Tip 9-4 compares mind-maps
and tables as documentation forms and never mentions a quality of the *system*; the tag can only
refer to the quality of the *notation*.

**Section 1 evidence (2026-09-21).** Section 1 uses the same tag eight times and there it is
unambiguous: every one of [[tip-1-11]] … [[tip-1-18]] and [[tip-1-24]] is about quality
requirements of the system, never about the quality of the documentation. That settles what the
tag means where it is *most* used, and makes the section 9 occurrences the outliers rather than
the rule — which strengthens option 1 below.

**Options.**
1. Keep [[quality-requirement]] on both — consistent, but tip 9-4's vocabulary stays misleading.
2. Drop the term from tip 9-4 and leave it with no term but [[architecture-decision]] — honest,
   but loses the (possibly intended) navigation from quality to decision forms.
3. Introduce a keyword for "documentation quality" — a new facet for a single page; likely too
   fine-grained.

**Resolution.** Open. The mapping of option 1 is in place so that `legacy-tags` could be emptied;
revisit when section 10 is ingested and the meaning of `quality` across the site is known.
