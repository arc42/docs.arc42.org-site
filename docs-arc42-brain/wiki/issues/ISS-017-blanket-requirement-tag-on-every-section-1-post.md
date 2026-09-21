---
id: ISS-017
type: issue
title: The legacy tag `requirement` marks the section, not a topic, on 22 of 24 section 1 tips
status: open
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-015-section-1-content]]'
related:
- '[[requirement]]'
- '[[tip-1-19]]'
- '[[tip-1-21]]'
severity: major
kind: ambiguity
raised-by: agent
resolved: null
---

**What's unresolved.** On the site, `requirement` tags 22 of the 24 section 1 posts — including
every quality tip and four of the five stakeholder tips. As a reading facet it therefore carries
no information: it selects "section 1", which the reader already has from the section page and
which the brain models in `section:`. The two exceptions give the pattern away: [[tip-1-21]] and
[[tip-1-23]] lack the tag while their neighbours [[tip-1-19]], [[tip-1-20]] and [[tip-1-22]] —
five tips on one topic, the stakeholder table — carry it. The tag was applied by habit, not by
meaning.

This ingest referenced the new term [[requirement]] only on the ten tips of section 1.1, which
genuinely are about requirements in general, and dropped the tag on the quality and stakeholder
tips in favour of their specific terms. That is a consolidation, and at cut-over it changes the
site: twelve pages would leave this tag.

**Affects.** [[requirement]], and at cut-over the twelve tips that carried the tag and no longer
reference the term — [[tip-1-11]] through [[tip-1-20]], [[tip-1-22]] and [[tip-1-24]] — plus the
site's keyword page.

**Evidence.** Over the raw batch, `requirement` appears in the `tags:` line of 22 of the 24 posts
and of none of the 4 examples; the two without it are `tags: stakeholder essential thorough`
([[tip-1-21]]) and `tags: stakeholder lean` ([[tip-1-23]]). [[tip-1-19]] ("Search broadly for
stakeholders!") is the clearest case of the tag being meaningless: the body is a long list of
stakeholder roles and mentions requirements nowhere, yet it is tagged `requirement` while 1-21,
on the same topic, is not. ADR-0003
anticipates exactly this — "Consolidating tags may change tag names on the site's keyword page;
page URLs never change".

**Options.**
1. Keep the consolidation as ingested: `requirement` means the concept, and section membership is
   expressed by `section:`. The site's tag list gets shorter and more meaningful; readers who
   used `/keywords/requirement` as "all of section 1" lose that path, which the section page
   already serves better.
2. Reference [[requirement]] on all 21 tips, preserving the site's tag counts exactly and making
   the cut-over a pure move — at the price of a term that means nothing on two thirds of its
   pages.
3. Introduce a per-section facet keyword and map blanket section tags to it, which would give
   `requirement`, and the same pattern in later sections, somewhere harmless to live.

**Resolution.** Open — this is the tag-consolidation decision the project has been carrying since
section 9, now with a concrete, countable case. It must be settled before section 1 is cut over,
because that is when the site's tag page changes.
