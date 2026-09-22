---
id: ISS-034
type: issue
title: The site tag `scenario` means two different things, and two earlier tags did the same
status: in-progress
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
resolved: null
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

Left to do: apply the same rule to [[tip-3-7]], where `cluster` and `criteria` should fold into
the term the page is actually about rather than stand as keywords of their own. That is a change
to a section already committed, so it travels as its own commit. Section 6 will then be
straightforward: every `scenario` there is a runtime scenario.
