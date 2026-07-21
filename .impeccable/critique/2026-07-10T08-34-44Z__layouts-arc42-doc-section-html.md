---
target: arc42 doc section page (/section-1/)
total_score: 29
p0_count: 0
p1_count: 2
timestamp: 2026-07-10T08-34-44Z
slug: layouts-arc42-doc-section-html
---
# Critique: arc42 documentation section page (_layouts/arc42-doc-section.html, rendered as /section-1/)

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | No active-page indicator in aside nav; subtle-ad shows a "loading" placeholder |
| 2 | Match System / Real World | 4 | arc42 vocabulary (Motivation/Content/Form) matches the audience exactly |
| 3 | User Control and Freedom | 3 | No in-page TOC or back-to-top on very long section pages |
| 4 | Consistency and Standards | 2 | Heading levels inconsistent and inverted: section title is h3, 24 tips are h1 |
| 5 | Error Prevention | 3 | Mostly n/a (reading surface); search can dead-end |
| 6 | Recognition Rather Than Recall | 3 | No breadcrumb or current-section highlight; no per-page TOC |
| 7 | Flexibility and Efficiency | 2 | No jump links; power users scroll a wall of 24 expanded tips |
| 8 | Aesthetic and Minimalist Design | 2 | 24 giant h1 tips dumped inline; visual hierarchy inverted |
| 9 | Error Recovery | 3 | 404 page exists; nothing notable |
| 10 | Help and Documentation | 4 | The arc42-help callouts are excellent inline guidance |
| **Total** | | **29/40** | **Solid, with clear structural fixes available** |

## Anti-Patterns Verdict

Not AI slop. This is a hand-built theme with genuine identity (the arc42 blue, the help/example callout pairing). None of the absolute bans are present: no gradient text, no glassmorphism, no hero-metric template, no identical card grid.

Deterministic detector (npx impeccable detect):
- section-1: 1 warning (skipped heading level, h1 to h3), 3 advisories (color outside palette rgb(0,0,0); numbered-section-markers 10/11/12 which is a FALSE POSITIVE, that is the section nav; second skipped-heading).
- homepage: clean (0 findings).

## Priority Issues

**[P1] Inverted heading hierarchy.** The page's own title ("1. Introduction and Goals") renders as h3 while all 24 tips render as h1 (2.3em, the largest type on the page). The least important, most-repeated items are visually and semantically the loudest. Breaks the document outline for screen readers and inverts the reading hierarchy. Fix: section title to h1/h2, subsections to h2/h3, tips to h3/h4. Command: /impeccable typeset.

**[P1] No progressive disclosure on long section pages.** All 24 tips are fully expanded inline with no in-page table of contents and no collapse. A reader who wants "maintain a stakeholder table" scrolls a wall to reach Tip 1-21. Nutshell.js collapsibles already exist (used for Related Questions) but are not applied to tips. Fix: sticky in-page TOC + collapse tips by default. Command: /impeccable layout.

**[P2] Body measure too long.** The content column is ~70% of a 1200px container (~820px), so prose runs well past 90 characters per line, violating the DESIGN.md Comfortable Measure Rule (65 to 75ch). Fix: cap prose max-width around 68ch. Command: /impeccable layout.

**[P2] Weak wayfinding.** The aside nav gives no current-section highlight and there is no breadcrumb, so on a long page the reader loses their place in the 12-section structure. Fix: active-state on the current nav item; optional sticky section label. Command: /impeccable layout.

**[P3] Markup drift in the masthead.** Deprecated `<font color=#fe5a83>` tag, a pure-black text value outside the palette, and the h1 carries a stats string ("144 tips and 33 examples") on every page rather than the page topic. Fix: replace `<font>` with a span + token color; give each page a topical h1. Command: /impeccable polish.

## Persona Red Flags

**Practicing Architect (primary, from PRODUCT.md).** Arrives mid-task to find stakeholder-table guidance. The page dumps 24 giant tip headings with no jump nav, so lookup is a scroll hunt. Directly violates the "reference-first, find the answer fast" principle.

**Newcomer to arc42.** The section's real title is smaller (h3) than the 24 tips (h1), so the visual hierarchy tells them the tips outrank the section itself. The outline reads as noise, not structure.

## Cognitive Load

Moderate (3 of 8): no progressive disclosure, inverted hierarchy, long unbroken scroll. The functional color coding (blue help vs pink example) and clear arc42 vocabulary keep it from being critical.
