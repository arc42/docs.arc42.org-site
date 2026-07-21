---
target: section page (_layouts/arc42-doc-section.html)
total_score: 28
p0_count: 0
p1_count: 3
timestamp: 2026-07-20T16-32-58Z
slug: layouts-arc42-doc-section-html
---
# Critique: arc42 Documentation, Section Page (`/section-1/`)

Reviewed as it currently renders (the older blue-on-white design). The new `DESIGN.md` deep-blue-masthead direction is not yet built; gaps are noted where useful but not scored against.

## Design Health Score

| # | Heuristic | Score | Key issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 2 | Current section is not marked in the aside nav; no breadcrumb, no "you are here". |
| 2 | Match System / Real World | 3 | Domain language is on point; but `<insert...>` stubs and a `… … …` empty table leak the fill-in-template metaphor onto a reference site. |
| 3 | User Control & Freedom | 3 | Nothing traps the user, but the whole aside precedes content in the DOM with no skip link. |
| 4 | Consistency & Standards | 2 | Heading semantics inverted; home uses red `<font>` h2s, section uses blue CSS h2s; tag pills unstyled; serif ad block. |
| 5 | Error Prevention | 3 | Minimal surface; nothing destructive. |
| 6 | Recognition rather than Recall | 3 | Full-text nav labels and inline guidance (strong), but no active state, so users recall which section they're in. |
| 7 | Flexibility & Efficiency | 3 | Search, tags, hover anchors exist; but a long page has no on-page TOC and no keyboard shortcuts. |
| 8 | Aesthetic & Minimalist | 2 | Whitespace is good, undercut by hierarchy inversion, low-contrast coral, dated blurry shadows, trailing sales block. |
| 9 | Error Recovery | 3 | No on-page error states; happy path is intact. |
| 10 | Help & Documentation | 4 | This is documentation and does it well: contextual callouts, examples, tips, related questions. |
| **Total** | | **28 / 40** | **Good (lower edge)** |

## Anti-Patterns Verdict

**Does it look AI-generated? No.** This is unmistakably hand-built. None of the absolute bans are present: no side-stripe accent borders (the one left border is a conventional gray 5px `#ddd` blockquote rule, which the spec permits), no gradient text, no glassmorphism, no hero-metric template, no identical icon-card grid, no modal. The category-reflex and aesthetic-lane traps are avoided.

The failure it flirts with is the opposite one the brand register warns about: **dated / generic**. Tells that place it around 2014-2016 rather than "current member of a refreshed family": the pale-blue header band (`#d7ecf8`) with muted blue title (`#397ab2`), callouts lifted by a blurred full-opacity bright-blue drop shadow (`box-shadow: 3px 3px 4px 0 rgba(11,82,185,1)`) instead of a crisp hard offset, deprecated `<font color=...>` tags in the header, and a sponsor block set in `Palatino Linotype` serif that appears nowhere else.

**Deterministic scan** (3 rendered pages): home page is clean. Two real findings, repeated on section and examples pages:
- **Skipped heading level** (warning): section pages jump `h1 -> h3`; examples jumps `h2 -> h4`. This directly corroborates the LLM's top finding below.
- **Pure black text** `rgb(0,0,0)` on the "arc42 Documentation" title (advisory): outside the palette, and exactly the pure `#000` the new spec forbids.
- **False positive, dismissed:** "numbered section markers 10, 11, 12". arc42's twelve sections are genuinely numbered; that is the template's real structure, not AI editorial scaffold.

(No visual overlay tab: browser automation is not available in this environment, so this run is code-review plus deterministic scan.)

## Overall Impression

A genuinely useful, calm reference whose content model is its real strength, wearing a surface that reads "old" and an HTML structure that quietly fails accessibility and scanning. The single most damaging problem is invisible to the eye but obvious to a screen reader and to SEO: the page title renders as the *smallest* heading on the page while a lower "Further Info" heading renders largest, and there is no content `<h1>` at all. The biggest opportunity is cheap: fix the heading outline and ship the already-specified deep-blue masthead, and the page jumps from "dated and slightly broken" to "fresh and correct" without touching the content.

## What's Working

1. **Contextual guidance model.** The `.arc42-help` callouts (`#dcf0ff` bg, `#002080` ink, high contrast) put Contents / Motivation / Form exactly where the reader needs them, chunked into threes. This is the site's real strength and earns the heuristic-10 score of 4.
2. **Calm, roomy reading surface.** Consistent 50px vertical rhythm, 1.5 body line-height, near-white page. The content-is-hero intent shows in the whitespace.
3. **Fully labeled primary navigation.** The aside lists all 12 sections plus Home / examples / tips as real text links (no icon-only nav except the hamburger), with a search box on top. Good recognition support for both audiences.

## Priority Issues

**[P1] Inverted heading hierarchy.** The page title "1. Introduction and Goals" is an `<h3>` (renders ~18.7px), while "Further Info" lower down is an `<h2>` at 1.8em (~28.8px blue), and there is no content `<h1>` at all. Both the LLM review and the deterministic scan flag this. It breaks scanning, the screen-reader outline, and SEO. **Fix:** section name becomes a content `<h1>` (2.3em ink, already styled), subsection titles `<h2>` (blue, already styled), demote "Further Info / Tips / Examples"; enforce one descending outline. **Command:** `/impeccable typeset` (with `/impeccable shape` for the outline).

**[P1] Accessibility floor: no focus, no landmarks, no skip link.** The compiled CSS has zero `:focus`/`:focus-visible` rules and the reset actively removes outlines (`a:active,a:hover{outline:0}`). The entire aside (search + 15 links) precedes `.site-content` with no skip link, no `<main>`, no `<nav>`, and the current page is not `aria-current`. The hamburger `<button class="fa fa-bars nav-toggle">` has no accessible name. **Fix:** add a 2px `#1675b9` `:focus-visible` outline (2px offset), a skip-to-content link, wrap the aside in `<nav aria-label>`, add `<main>`, mark the active link, give the toggle an `aria-label`. **Command:** `/impeccable harden`.

**[P1] No wayfinding: no active state, no on-page TOC.** In a 12-section reference the aside never highlights the current section, there is no breadcrumb, and a long page offers no jump list to 1.1 / 1.2 / 1.3 (anchor links surface only on hover). Both audiences lose "where am I / where can I jump." **Fix:** visual plus `aria-current` active state on the aside link, and a small sticky on-page TOC. **Command:** `/impeccable clarify` (with `/impeccable layout`).

**[P2] Reading measure too wide.** `.site-content` is 70% of a 1200px container (~840px), so prose runs ~100-110 characters per line, well past the 65-75ch the site's own spec mandates for a long-form reference. This is the site's primary job and it is under-tuned. **Fix:** cap the prose column at ~68ch (~640-720px), let tables and images span wider. **Command:** `/impeccable typeset` (with `/impeccable layout`).

**[P2] Dated masthead and low-contrast coral tagline.** The header description renders in coral `#fe5a83` on pale blue `#d7ecf8` at ~2.6:1, failing AA even at ~26px, and the entire tagline (not just an accent) is coral via a deprecated `<font>` tag. This is the "old pale wash" the new spec explicitly replaces, and it violates the spec's "coral is a spark, never a line of text." **Fix:** ship the deep-blue `#0e4f80` masthead with Header-Tint text, reserve coral for a small counter accent, delete the `<font>` tags. **Command:** `/impeccable colorize` (with `/impeccable clarify`).

## Persona Red Flags

**Sam (accessibility-dependent).**
- Tabs through the search input and 15 aside links before reaching any content on every page; no skip link, no `<main>`.
- No visible focus ring anywhere (zero `:focus-visible` rules; reset sets `outline:0`).
- Screen-reader heading order is nonsensical: page title `<h3>`, "Further Info" `<h2>`, no content `<h1>`.
- The hamburger button has no accessible name (icon font only).
- Coral on pale blue fails contrast; the current aside item is not `aria-current`.

**Jordan (arc42 newcomer / confused first-timer).**
- In the first five seconds the biggest content heading is "Further Info", not the actual page title, so Jordan cannot tell where the section's content begins.
- `<insert requirements overview>`, `<complete the stakeholder table:>`, and a `… … …` empty table look like broken or unfinished content; nothing says they are fill-in placeholders.
- Examples use the same navy ink `#002080` as guidance (the intended cool-vs-warm split is not built), so Jordan cannot tell the template's advice from a worked example.
- No "what is a section / start here" orientation; the page dives straight into guidance.

**Alex (impatient power user).**
- No on-page TOC, so jumping to "Form" or a specific tip means scrolling a long page; anchor links appear only on hover.
- The 24-tip list is flat and nearly every entry shows `#requirement`, so the tag scent does not discriminate; no on-page filter.
- Search exists but there is no `/`-to-focus or any keyboard accelerator.
- Positive: guidance is immediately visible and the static page loads instantly.

**Priya (returning arc42 practitioner, from PRODUCT.md).**
- The three help boxes answer "what belongs here" fast and well; the design serves her core loop here.
- But to grab a worked example she must spot two links buried mid-page inside the pale help box; examples are not a distinct warm block, so they do not pop when scanning.
- PRODUCT.md's success metric is "return to your own docs with a clear next step," yet the page's terminal content is a training ad plus footer, not a next-step control.

## Minor Observations

- **Peak-end closes on a sales pitch.** The last content before the footer is a training advertisement ("arc42 offers architecture training") in a mismatched serif, quietly contradicting PRODUCT.md's "expert confidence, no selling." Its CSS also has bugs: `.subtle-ad a { color: ff796a }` is missing the `#`, and `.subtle-ad h4 { line-height: 1.2pt }` is a near-zero line-height.
- **Tag pills do not render as pills.** The cyan `#aee3f8` background is scoped to `.tag-box a`, but tips use `<a class="tag">`, so tags show as bare small blue `#requirement` links.
- `p { font-family: sans-serif }` globally overrides the Helvetica stack for paragraphs only. Harmless but sloppy.
- Example link titles render with a stray leading colon (":Overview Example: ...").
- Duplicate `id="search-results"` and a duplicate `<title>` in `<head>` make the HTML invalid.
- `<meta name="theme-color" content="#ffffff">` matches neither the current header nor the intended deep-blue.

## Questions to Consider

1. If the site's whole job is "find what belongs here and get back to work," why does the page end on a training ad instead of a "next section / back to your doc" control, and why is the page's own title the smallest heading on it?
2. The spec commits to a deep-blue masthead and a warm/cool callout split as the family signal, but the shipped page still renders the exact pale wash it says it replaces. If the masthead is the cheapest change that makes this read as "refreshed arc42 family," what is blocking it?
3. Fill-in-template stubs (`<insert...>`, `… … …`) appear on a reference site. Are those helping a reader who came to learn, or are they an artifact of shipping the downloadable template markup verbatim?
4. Every tip on section 1 is tagged `#requirement`. If the tag cannot discriminate between 24 items, is it wayfinding or decoration?
