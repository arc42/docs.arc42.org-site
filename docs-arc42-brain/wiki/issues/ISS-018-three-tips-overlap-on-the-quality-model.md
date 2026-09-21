---
id: ISS-018
type: issue
title: Tips 1-14, 1-15 and 1-24 all send the reader to the arc42 quality model
status: open
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-015-section-1-content]]'
related:
- '[[tip-1-14]]'
- '[[tip-1-15]]'
- '[[tip-1-24]]'
- '[[quality-model]]'
severity: minor
kind: question
raised-by: agent
resolved: null
---

**What's unresolved.** Three of the nine quality tips have the same payload — "use the ~150
examples at quality.arc42.org" — and the reader meets it three times without being told why there
are three tips. [[tip-1-24]] in particular says little that [[tip-1-15]] does not say better, and
the two were written ten years apart.

**Affects.** [[tip-1-14]], [[tip-1-15]], [[tip-1-24]].

**Evidence.** [[tip-1-14]] ("Use checklists for quality requirements!") offers ISO 25010 as the
checklist and then points at Q42 as "a more practical alternative", linking tip 1-15.
[[tip-1-15]] ("Use examples to work out quality goals together with your stakeholders!") is the
one that explains the technique — put a concrete example in front of people and their reaction is
the requirement — and cites the same 150 examples and 190 characteristics. [[tip-1-24]] ("Make
use of the (open-source) arc42 Quality Model and its many examples!") is three sentences and adds
only the caveat that the collection is neither complete nor perfect. Its `date` is 2021-12-12,
the other two are 2016-03-02, so 1-24 reads like the announcement Q42 needed before 1-15 existed.

**Options.**
1. Merge 1-24 into 1-15, keeping its caveat sentence, and retire `/tips/1-24/` — this needs an
   entry with a reason in `_system/retired-permalinks.txt`, because the URL is public and cited.
2. Keep all three and give each a distinct job in its first sentence: 1-14 the standard as a
   checklist, 1-15 the technique, 1-24 the model itself. Cheapest, no URL disappears.
3. Leave as is — three overlapping tips is a redundancy, not an error.

**Resolution.** Open, and the arc42 authors' call. Note that option 1 is the first case in the
project where a published tip URL would be given up, so it is also a test of the retirement
mechanism.
