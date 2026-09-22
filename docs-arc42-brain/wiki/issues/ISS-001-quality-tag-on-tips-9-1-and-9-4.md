---
id: ISS-001
type: issue
title: Does the legacy tag `quality` on tips 9-1 and 9-4 mean the arc42 quality requirement?
status: resolved
created: '2026-09-17'
updated: '2026-09-22'
sources:
- '[[SRC-015-section-1-content]]'
- '[[SRC-013-section-9-content]]'
- '[[SRC-017-section-10-content]]'
related:
- '[[tip-1-11]]'
- '[[tip-1-14]]'
- '[[tip-9-1]]'
- '[[tip-9-4]]'
- '[[quality-requirement]]'
severity: minor
kind: ambiguity
raised-by: agent
resolved: '2026-09-22'
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

**Resolution (2026-09-22): resolved, and the answer is yes for tip 9-1 and "no evidence" for tip 9-4.**

This issue set its own condition — "revisit when section 10 is ingested and the meaning of
`quality` across the site is known". Section 10 was ingested on 2026-09-21, and the census can now
be taken rather than guessed.

The site tag `quality` sits on **eleven** pages: the seven section 10 tips, the two section 10
quality-scenario examples, and [[tip-9-1]] and [[tip-9-4]]. Nine of the eleven are section 10, where
the tag can only mean the arc42 concept, and `quality-requirement` is the **only** vocabulary page
in the vault claiming the name in `legacy-tags`. So the tag is not ambiguous site-wide, which is
what this issue suspected it might be.

[[tip-9-1]] confirms the mapping from its own body: it asks the reader to document decisions that
are "critical or important for the system" and "influencing important quality attributes". That is
the arc42 concept, and the mapping to [[quality-requirement]] is right.

[[tip-9-4]] does not. Its body compares mind maps with tables as notations for recording decisions
and never mentions quality in any sense — neither the arc42 concept nor the quality of the
documentation, which was this issue's alternative reading. So the tag has no support in the text at
all; it is a stray, not an ambiguity. The mapping is therefore not *wrong* so much as unmotivated,
and since section 9 is cut over it is already published: a reader filtering `quality-requirement`
meets a tip about mind maps. Dropping it costs one tag on one page and breaks no URL.

**What this leaves.** One line for whatever editorial pass is eventually run: remove
`quality-requirement` from [[tip-9-4]] unless the arc42 authors meant something by the tag that the
body does not say. Recorded there rather than kept open here, because the question this issue
asked — what does the tag mean — now has a measured answer.
