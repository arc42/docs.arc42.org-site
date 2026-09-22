---
id: ISS-030
type: issue
title: Section 3 bodies carry editorial defects
status: open
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-022-section-3-content]]'
related:
- '[[tip-3-3]]'
- '[[tip-3-4]]'
- '[[tip-3-5]]'
- '[[tip-3-8]]'
- '[[tip-3-12]]'
- '[[tip-3-13]]'
- '[[tip-3-14]]'
- '[[tip-3-17]]'
- '[[tip-3-18]]'
- '[[tip-3-19]]'
- '[[03-context-example-business-2]]'
- '[[03-context-example-business-1]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** Fourteen defects in eleven pages, and for the first time a group of them
has a single cause: four are German constructions carried into English, one of which reverses the
meaning of a sentence about security.

**Affects.** [[tip-3-3]], [[tip-3-4]], [[tip-3-5]], [[tip-3-8]], [[tip-3-12]], [[tip-3-13]],
[[tip-3-14]], [[tip-3-17]], [[tip-3-18]], [[tip-3-19]], [[03-context-example-business-2]]; and, for the spelling split alone,
[[03-context-example-business-1]].

**Evidence — the German ones.**

- [[tip-3-4]]: "Security risks: if you receive/send **sensible** data from/to external systems."
  German *sensibel* means sensitive; English *sensible* means reasonable. The sentence as printed
  says the opposite of a security warning, and it is the only defect in this list that a reader
  cannot repair from context.
- [[tip-3-14]]: "high implementation and operating expenses **and -risks**", and "special quality
  requirements **or -goals**". German elides a repeated compound head with a hyphen
  (*Implementierungs- und Betriebsrisiken*); English has no such form, so the hyphen renders as a
  stray dash.
- [[tip-3-3]]: "refer to the relevant chapter (probably 8.1, domain **modell**)" — the German
  spelling of *model*.

**Evidence — the rest.**

- [[tip-3-19]]: "if you focus␣␣more on domain topics (and therefore **and** do without technical
  context." — a doubled space, a stray "and", and a parenthesis that never closes. The second
  unclosed parenthesis in the vault, after [[07-deployment-sample-tpu-2]] in
  [[ISS-029-section-7-bodies-carry-editorial-defects|ISS-029]].
- [[tip-3-8]]: "you could use UML port symbols **at to** denote categories".
- [[tip-3-5]]: "contains too many details for a **context _real_ context** diagram" — two words
  transposed around the emphasis.
- [[tip-3-12]]: "even if it doesn't use **it's** interface directly", and a link labelled "(Show
  risks in **contxt**)".
- [[tip-3-13]]: "as you get **additionel** elements".
- [[tip-3-17]]: "like transmission-**protocolls**".
- [[tip-3-18]]: "you should **explicitely** describe the mapping".
- [[03-context-example-business-2]]: "the **organizatino** which provides MaMa", and "printing
  letters on **MaMas'** behalf" — the possessive of a singular name.
- Spelling split inside one section: *neighbour* twelve times against *neighbor* twice, and the
  two spellings meet in a table header — [[tip-3-3]] writes `| Neighbour |` where
  [[03-context-example-business-1]] writes `|Neighbor |`.

**Options.**
1. Fix them at cut-over, in the brain, as part of owning the content.
2. Fix them on the site now, before cut-over, and re-run `brain-raw` so the brain stays verbatim.
3. Leave them.

**Resolution.** Open, the eighth section with a typo issue of its own. Two things separate this
one from its seven siblings. The "sensible data" line is not cosmetic: it inverts a security
statement, which argues for fixing it ahead of whatever happens to the rest. And the four German
constructions are the first evidence that these sections were translated rather than written in
English — which means a vault-wide pass should look for the pattern (*sensible*, *eventually*,
*actual*, hyphen elisions) and not only for misspellings.
