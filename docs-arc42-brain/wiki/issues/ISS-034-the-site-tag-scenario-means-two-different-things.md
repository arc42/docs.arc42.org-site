---
id: ISS-034
type: issue
title: The site tag `scenario` means two different things, and two earlier tags did the same
status: resolved
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-023-section-5-content]]'
related:
- '[[tip-5-23]]'
- '[[tip-3-7]]'
- '[[runtime-scenario]]'
- '[[quality-scenario]]'
severity: major
kind: ambiguity
raised-by: agent
resolved: '2026-09-22'
---

**What's unresolved.** `scenario` sits on 16 pages and means a *quality* scenario on four of them
and a *runtime* scenario on twelve. The vault has no way to record that in `legacy-tags`, because
that field says "these old tags mean this term" and a tag cannot mean two terms. Two earlier tags
have the same shape and were handled inconsistently, which is what turns this from a section 5
detail into a policy question.

**Affects.** [[tip-5-23]] and all eleven section 6 tips (not yet ingested) for `scenario`;
[[tip-3-7]] for `cluster` and `criteria`.

**Evidence.** The 16 pages: [[tip-5-23]], the eleven section 6 tips, and
[[tip-10-5]], [[tip-10-6]], [[tip-10-7]], [[tip-10-8]]. Sections 1 and 10 mapped it to
[[quality-scenario]], whose `legacy-tags` therefore read `[scenario, quality-scenario]`. But
[[tip-5-23]] says "you can describe or specify such interactions by runtime scenarios" about
handshakes and protocols between building blocks, which is [[runtime-scenario]] and not a
requirement at all. Section 6, whose eleven tips all carry `scenario` *and* `runtime-view`, will
multiply the case by eleven.

Two tags reached this point before and were resolved the other way round:

| tag | folded into | where | still on the site |
|---|---|---|---|
| `cluster` | [[requirement]] | section 1, at cut-over | 1 page — [[tip-3-7]] |
| `criteria` | [[decision-criteria]] | section 9, at cut-over | 1 page — [[tip-3-7]] |
| `scenario` | [[quality-scenario]] | sections 1 and 10 | 16 pages |

The section 3 ingest then made `cluster` and `criteria` **keywords** without noticing that both
names were already claimed as legacy tags of a term. Nothing broke — a keyword's slug emits the
same tag, so parity passed — but the vault now answers "what does `cluster` mean?" in two places
with two answers.

**Resolution (decided 2026-09-22).** Fold per meaning: each page's ambiguous tag becomes the term
that matches what *that page* says, and the ambiguity is recorded here rather than in
`legacy-tags`. Applied to [[tip-5-23]], whose `scenario` becomes [[runtime-scenario]] — one tag
delta on one page. [[quality-scenario]] keeps the `scenario` legacy tag, since it holds the
majority reading and two sections already fold that way; [[runtime-scenario]] does not claim it,
and says in its *Distinguish from* paragraph why.

Applied to [[tip-3-7]] in the same session. Its `cluster` and `criteria` fold into [[context]],
the term the page already carried — on that page the two tags only say "group the neighbours, and
say by what rule", which is what the context section is for. Neither name is claimed by
[[context]] in `legacy-tags`, because [[requirement]] and [[decision-criteria]] hold those claims
for their own sections; the exception is recorded in [[context]]'s prose and here. Both tags reach
**zero** at section 3's cut-over, which finishes the consolidation sections 1 and 9 began, and the
two keyword pages created for them are deleted.

So the rule, stated once: **one term owns a legacy tag name; a page whose use of that tag means
something else is mapped by meaning, and the exception is recorded in this issue and in the
receiving term's prose.** Every name in the vault is now claimed by exactly one vocabulary page.
Section 6 needs no new decision — all eleven of its tips mean a runtime scenario.
