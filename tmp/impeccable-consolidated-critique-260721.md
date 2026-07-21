---
target: full site & design system (docs.arc42.org)
total_score: 28.5
gemini_score: 30
fable_score: 27
p0_count: 0
p1_count: 4
p2_count: 3
timestamp: 2026-07-21T10:20:41Z
slug: impeccable-consolidated-critique-260721
detectors: [Gemini 3.5 Flash (High), Fable Independent Reviewer]
---

# Consolidated Impeccable Critique: arc42 Documentation Site

Synthesized from independent design critiques by **Gemini** (`impeccable-critique-agy260721.md`) and **Fable** (`impeccable-critique-fable-260721.md`). 

> **Prioritization Note:** Issues detected independently by **both** Gemini and Fable represent consensus friction points and are given highest priority (P1). Individual findings detected by a single reviewer are preserved and categorized by impact.

---

## Executive Summary & Attribution Index

| # | Issue Description | Detector Attribution | Priority | Target Command |
|---|-------------------|----------------------|----------|----------------|
| 1 | **Unconstrained Prose Measure (~95–110ch)** | **Gemini + Fable** (Duplicate) | **P1** | `/impeccable typeset` |
| 2 | **Aspirational DESIGN.md Refresh (Pale Masthead, Callout Inks, Shadow Drift)** | **Gemini + Fable** (Duplicate) | **P1** | `/impeccable colorize` |
| 3 | **Heading Hierarchy Inversion & Outline Drift (`h1`→`h3` skips)** | **Gemini + Fable** (Duplicate) | **P1** | `/impeccable typeset` |
| 4 | **Contrast Failures in Masthead Tagline & Tag Pills** | **Gemini + Fable** (Duplicate) | **P1** | `/impeccable colorize` |
| 5 | **Lack of In-Page TOC & Prev/Next Section Stepper** | **Gemini** *(Supported by Fable)* | **P1** | `/impeccable layout` |
| 6 | **24-Tip Stack Visual Noise & Buried "Further Info" Payoff** | **Fable** | **P2** | `/impeccable layout` |
| 7 | **Template, HTML Validation & QA Debris (`<font>` tags, duplicate IDs/titles, `<em>**</em>`)** | **Gemini + Fable** (Duplicate) | **P2** | `/impeccable polish` |
| 8 | **Accessibility Landmark & ARIA Floor Expansion (`aria-expanded`, `aria-hidden`)** | **Fable** | **P2** | `/impeccable harden` |

---

## Consolidated Design Health Score

Average Score: **28.5 / 40** (*Gemini: 30/40, Fable: 27/40*)

| # | Usability Heuristic | Gemini | Fable | Consensus Score | Key Issue & Detector Attribution |
|---|---------------------|--------|-------|-----------------|----------------------------------|
| 1 | **Visibility of System Status** | 3 | 3 | **3 / 5** | Active section marked via `aria-current="page"`; missing sticky on-page TOC / position indicator on long pages `[Gemini + Fable]`. |
| 2 | **Match System / Real World** | 3 | 3 | **3 / 5** | Excellent domain terminology; raw `<insert requirements overview>` placeholders leak template internals `[Gemini + Fable]`. |
| 3 | **User Control & Freedom** | 4 | 3 | **3.5 / 5** | 12-section nav + search give exits; long 1,600-line pages lack intra-page jump anchors `[Fable]`. |
| 4 | **Consistency & Standards** | 2 | 2 | **2 / 5** | Heading levels jump irregularly; deprecated `<font>` tags; near-miss blues violate the One Blue Rule `[Gemini + Fable]`. |
| 5 | **Error Prevention** | 4 | 3 | **3.5 / 5** | Static site has minimal error surface; placeholder headings could mislead copy-pasters `[Fable]`. |
| 6 | **Recognition Rather Than Recall** | 3 | 3 | **3 / 5** | Clear nav labels; help vs. example blocks lack explicit text labels ("the template's advice") `[Fable]`. |
| 7 | **Flexibility & Efficiency** | 3 | 2 | **2.5 / 5** | Instant static loads; missing keyboard accelerators (e.g. `/` for search) & prev/next section steppers `[Gemini + Fable]`. |
| 8 | **Aesthetic & Minimalist Design** | 3 | 2 | **2.5 / 5** | Wall of 24 identical tip panels with redundant `<hr>`s; wide ~110ch line length `[Gemini + Fable]`. |
| 9 | **Error Recovery** | 3 | 2 | **2.5 / 5** | Clean static search results; htmx ad-fetch fails gracefully to local fallback `[Fable]`. |
| 10 | **Help & Documentation** | 4 | 4 | **4 / 5** | Exceptional core content delivery via contextual guidance callout blocks `[Gemini + Fable]`. |
| **Total** | | **30** | **27** | **28.5 / 40** | **Refresh In Progress / Strong Foundation** |

---

## Anti-Patterns Verdict

### AI-Generated Slop Check: **Passed (0 / 5 AI Tells)** `[Gemini + Fable]`
Both detectors confirm the site is 100% human-authored with zero generative slop:
- No gradient text or floating glassmorphic cards.
- No generic icon-card grid boxes.
- No fake metric counters ("10k+ Users").
- No decorative background blobs or generic dark-mode toggles.

### Generic / Dated Tells: **Present (4 Tells)** `[Gemini + Fable]`
1. **Pale-Blue Header Band (`#d7ecf8`)**: Renders the old pale wash instead of the committed Deep Blue masthead (`#0e4f80`) with Header-Tint text `[Gemini + Fable]`.
2. **Unconstrained Measure**: Body prose stretches to ~95–110 characters per line, breaking the 65–75ch requirement in `DESIGN.md` `[Gemini + Fable]`.
3. **Deprecated Inline Markup**: `_pages/home.md` and `keywords.html` contain legacy `<font color="#dd354b">` tags `[Gemini + Fable]`.
4. **Blurred Callout Drop Shadows**: `.arc42-help` uses a blurred drop shadow (`rgba(11,82,185,1)`) rather than the signature hard offset Callout Lift shadow `[Fable]`.

---

## Overall Impression

Both reviewers agree that **arc42 documentation is a fast, trustworthy, and content-rich technical reference with solid accessibility foundations** (landmarks, focus rings, `aria-current`, reduced motion). 

However, there is a clear gap between the specification in `DESIGN.md` and the shipped implementation. Implementing the design tokens, capping the reading measure, and unifying heading structures will instantly elevate the site to modern family standards.

---

## Priority Issues

### **P1 (Highest Priority — Consensual / Core Architecture)**

#### **[P1] Unconstrained Prose Reading Measure (~95–110ch)** `[Gemini + Fable]`
- **Detected By**: **Gemini** & **Fable**
- **Location**: `_sass/base/_layout.scss` (`.site-content`)
- **Problem**: `.site-content` takes 70% of a 1200px container (~840px), forcing body copy to run 95–110 characters per line. This directly violates the 65–75ch Comfortable Measure Rule in `DESIGN.md`.
- **Fix**: Apply `max-width: 68ch` (or `~46em`) to prose elements inside `.site-content`.
- **Suggested Command**: `/impeccable typeset`

#### **[P1] Aspirational DESIGN.md Refresh & Contrast Failures** `[Gemini + Fable]`
- **Detected By**: **Gemini** & **Fable**
- **Location**: `_sass/base/_variables.scss`, `_sass/_header.scss`, `assets/css/arc42-doc.css`
- **Problem**: 
  - The masthead uses the legacy pale-blue wash (`#d7ecf8`) with a coral description line (`#fe5a83`) that fails AA contrast at ~2.5:1 `[Fable]`.
  - Both guidance (`.arc42-help`) and example (`.arc42-example`) callouts use near-identical navy ink (`#002080`), missing the intended cool guidance (`#0c3d66`) vs. warm blush example (`#9a3b2e`) pairing `[Fable]`.
  - Help callout shadow is blurred rather than the signature hard offset `[Fable]`.
- **Fix**: Implement Deep Blue (`#0e4f80`) masthead, Header-Tint (`#eaf4fc`) text, Coral (`#ff5c7c`) tagline, cool/warm callout inks, and hard offset Callout Lift shadow `[Gemini + Fable]`.
- **Suggested Command**: `/impeccable colorize`

#### **[P1] Heading Hierarchy Inversion & Outline Drift** `[Gemini + Fable]`
- **Detected By**: **Gemini** & **Fable**
- **Location**: `_pages/section-*.md`, `_pages/home.md`, `_pages/examples.md`, `_includes/further-info.md`
- **Problem**: Heading outlines jump unpredictably:
  - Section pages jump `h1` → `h3` in sub-content `[Gemini]`.
  - Home page jumps `h1` → `h3` at the Ukraine banner `[Fable]`.
  - Examples page jumps `h1` → `h4` at the subtle-ad block `[Fable]`.
- **Fix**: Enforce single descending heading outlines (`h1` section title → `h2` subheads in Signal Blue → `h3` tips/examples) `[Gemini + Fable]`.
- **Suggested Command**: `/impeccable typeset`

#### **[P1] Lack of In-Page TOC & Prev/Next Section Stepper** `[Gemini]`
- **Detected By**: **Gemini** *(Supported by Fable's Alex Persona feedback)*
- **Location**: `_layouts/arc42-doc-section.html`, `_pages/section-*.md`
- **Problem**: Long 1,600-line section pages offer no in-page Table of Contents or jump list. Pages end abruptly on a training ad rather than a "Next Section" navigation stepper.
- **Fix**: Add a sticky in-page TOC for section pages and a Next/Previous section footer navigation stepper.
- **Suggested Command**: `/impeccable layout`

---

### **P2 (Medium Priority — Quality, Structural & Accessibility Floor)**

#### **[P2] 24-Tip Stack Visual Noise & Buried "Further Info" Payoff** `[Fable]`
- **Detected By**: **Fable**
- **Location**: `_includes/further-info.md`, `_sass/_content.scss`
- **Problem**: Every tip renders as a full tinted panel with redundant `<hr>` dividers, un-hidden decorative icons, and empty `ul.meta` containers, creating extreme visual noise at the bottom of section pages.
- **Fix**: Compact tip lists into grouped link lists by subsection (1.1 / 1.2 / 1.3); drop redundant `<hr>`s and empty meta lists.
- **Suggested Command**: `/impeccable layout`

#### **[P2] Template, HTML Validation & QA Debris** `[Gemini + Fable]`
- **Detected By**: **Gemini** & **Fable**
- **Location**: `_pages/home.md`, `_pages/keywords.html`, `_pages/section-7.md`, `_layouts/default.html`
- **Problem**: 
  - Deprecated `<font color="#dd354b">` tags on home and keywords pages `[Gemini + Fable]`.
  - Rendered `<em>**</em>` syntax artifacts in section-7.1 `[Fable]`.
  - Duplicate `<title>` tag in `<head>` (layout + `jekyll-seo-tag`) `[Fable]`.
  - Duplicate `id="search-results"` (emitted up to 3x per page) `[Gemini + Fable]`.
  - Colon-prefixed titles (`:Overview Example:`) `[Gemini + Fable]`.
- **Fix**: Clean up template artifacts, remove deprecated `<font>` tags, ensure unique HTML IDs, and remove duplicate title tags.
- **Suggested Command**: `/impeccable polish`

#### **[P2] Accessibility Floor Expansion & ARIA Hardening** `[Fable]`
- **Detected By**: **Fable**
- **Location**: `_layouts/default.html`, `_includes/further-info.md`
- **Problem**: `.nav-toggle` has `aria-controls` but lacks `aria-expanded` state; decorative `fa-tags` icons lack `aria-hidden="true"`; skip-link text uses pure `#fff` instead of paper tint `#fcfdff`.
- **Fix**: Add `aria-expanded` toggle script, add `aria-hidden` to decorative icons, tune skip-link text color.
- **Suggested Command**: `/impeccable harden`

---

## Persona Red Flags

- **Sam (Accessibility-dependent reader)**:
  - *Strengths*: Focus rings, skip link, landmarks (`<main>`, `<nav>`), `aria-current="page"` active state present `[Gemini + Fable]`.
  - *Friction*: Skipped heading levels (`h1`→`h3`, `h1`→`h4`) confuse screen reader outline; `.nav-toggle` missing `aria-expanded` `[Fable]`.

- **Jordan (arc42 newcomer)**:
  - *Friction*: Raw template stubs (`<insert requirements overview>`, `… … …`) read like broken or incomplete page content `[Gemini + Fable]`. Help vs. example callouts lack text labels ("the template's advice"), relying only on tint `[Fable]`.

- **Alex (Impatient power user)**:
  - *Friction*: Unconstrained 110ch line lengths slow down rapid scanning `[Gemini + Fable]`. No in-page TOC to jump directly to subsection 1.2 or 1.3 `[Gemini + Fable]`. Search lacks a `/` keyboard shortcut `[Gemini + Fable]`.

- **Priya (Returning arc42 practitioner)**:
  - *Friction*: Contextual help blocks deliver guidance fast, but lack a "Next Section" control at the foot of pages to seamlessly move through the 12 sections `[Gemini]`.

---

## Minor Observations

- **Sponsor Block Excellence**: The `.subtle-ad` sponsor block currently matches `DESIGN.md` most faithfully (kicker label, maroon border, hard offset shadow, capped measure) `[Fable]`.
- **Performance & Asset Loading**: `nutshell.js` loads synchronously in `<head>`; `htmx.org` is fetched from an external CDN (`unpkg.com`) for the ad container `[Fable]`.
- **Footer Icon Color**: Status icon uses `#50C878` instead of token `#2e9e67` `[Fable]`.
- **URL Redirect Hops**: Footer link to `/imprint` causes a redirect hop under `permalink: pretty` (should be `/imprint/`) `[Fable]`.

---

## Questions for Maintainers

1. How should raw `<insert…>` template stubs be styled so newcomers immediately perceive them as fill-in placeholders rather than broken site content? `[Gemini + Fable]`
2. Should in-page TOC generation be automated across all 12 section pages via Liquid/Kramdown, or integrated into a 3-pane layout? `[Gemini + Fable]`
3. Can the sponsor block's hard-offset shadow and kicker styling be mirrored onto `.arc42-help` callouts to ensure guidance carries equal design authority? `[Fable]`

---

## Execution Hand-Off Plan

1. **`/impeccable colorize`** — Implement Deep Blue masthead, Header Tint title, Coral tagline, cool/warm callout inks, hard offset Callout Lift shadow, and tokenized tag pills.
2. **`/impeccable typeset`** — Cap prose measure at ~68ch (`~46em`) and unify heading levels (`h1` → `h2` → `h3`).
3. **`/impeccable layout`** — Add in-page TOC, prev/next section steppers, and compact the 24-tip stack.
4. **`/impeccable polish`** — Remove deprecated `<font>` tags, syntax artifacts (`<em>**</em>`), duplicate IDs/titles, and colon prefixes.
5. **`/impeccable harden`** — Add `aria-expanded` toggle state and `aria-hidden` attributes to decorative icons.
