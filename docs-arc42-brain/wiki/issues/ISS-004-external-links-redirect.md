---
id: ISS-004
type: issue
title: Three external links in the section 9 content redirect to new locations
status: open
created: '2026-09-17'
updated: '2026-09-17'
sources:
- '[[SRC-009-section-9-page]]'
- '[[SRC-013-section-9-content]]'
related:
- '[[section-9]]'
- '[[tip-9-1]]'
- '[[tip-9-5]]'
- '[[tip-9-9]]'
- '[[09-decision-example-adr]]'
- '[[09-decision-example-htmlsc-1]]'
severity: minor
kind: risk
raised-by: agent
resolved: null
---

**What's unresolved.** Three external targets still answer, but only through a redirect. Redirects
are the stage before a dead link, and one of them makes the section cite the same article under two
different domains.

**Affects.** [[section-9]], [[tip-9-1]], [[tip-9-5]], [[tip-9-9]],
[[09-decision-example-adr]], [[09-decision-example-htmlsc-1]].

**Evidence.** Checked 2026-09-17 with `curl -sI`:

| Link | Status | Redirects to | Used on |
|---|---|---|---|
| `https://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions` | 301 | `https://cognitect.com/blog/...` (200) | tip 9-1, tip 9-5 (twice), ADR example |
| `https://github.com/joelparkerhenderson/architecture-decision-record` | 301 | `https://github.com/architecture-decision-record/architecture-decision-record` (200) | tip 9-9 (twice) |
| `https://wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance` | 301 | `https://en.wikipedia.org/wiki/...` (200) | HtmlSC example |

Section 9 itself already links Nygard's article under the target domain
(`https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions`), so the same text is
cited under two domains within one section. The anchor
`#suggestions-for-writing-good-adrs` still exists after the GitHub move, and tip 9-9 still names
Joel Parker Henderson, who now owns the organization of the same name.

**Options.**
1. Rewrite all three to their current targets — one small content edit per page, removes the
   double citation.
2. Leave them; the redirects work today — but they will break silently.

**Resolution.** Open.
