---
target: full site & design system (docs.arc42.org)
total_score: 30
p0_count: 0
p1_count: 3
timestamp: 2026-07-21T09:27:54Z
slug: docs-arc42-org-site-critique
---

# Critique: arc42 Documentation Site (Full Site & Design System Review)

Reviewed against the updated specifications in `PRODUCT.md` and `DESIGN.md`, alongside the current codebase (`_layouts/`, `_includes/`, `_sass/`, `_pages/`).

Recent maintenance has significantly upgraded the accessibility foundation (adding skip-to-content links, `:focus-visible` focus rings, HTML5 `<main>`/`<nav>` landmarks, and `aria-current="page"` active state in the navigation). However, visual design system tokens (such as the saturated Deep-Blue masthead, capped prose measure, and heading outline unification) remain partially unfulfilled in the SCSS and Markdown source files.

---

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | **Visibility of System Status** | 3 / 5 | Active section is now highlighted in the aside nav via `aria-current="page"`, but no breadcrumbs or sticky on-page TOC exist for long section pages. |
| 2 | **Match System / Real World** | 3 / 5 | Domain language and 12-section architecture match the arc42 mental model perfectly; placeholder stubs (`<insert...>`, `… … …`) occasionally leak raw template fill-in syntax into reference docs. |
| 3 | **User Control & Freedom** | 4 / 5 | Navigation is straightforward; skip-to-content link allows keyboard users to bypass the aside nav immediately. |
| 4 | **Consistency & Standards** | 2 / 5 | Heading levels jump irregularly across Markdown pages (`h1` -> `h3` in sections, `h2` -> `h4` in examples); `_pages/home.md` and `keywords.html` contain deprecated `<font color="#dd354b">` tags and off-palette red colors. |
| 5 | **Error Prevention** | 4 / 5 | Low interactive error surface; form inputs are limited to static GET search. |
| 6 | **Recognition rather than Recall** | 3 / 5 | Navigation labels are clear, but long section pages require scrolling up and down to recall subsection anchors (no sticky TOC or in-page jump list). |
| 7 | **Flexibility & Efficiency** | 3 / 5 | Instant static page loads and full-text search exist; missing keyboard accelerators (e.g. `/` to focus search) and prev/next section steppers. |
| 8 | **Aesthetic & Minimalist** | 3 / 5 | Clean reading surface and high-contrast callouts (`.arc42-help`), but held back by the pale-blue masthead, wide reading measure, and hardcoded inline red fonts. |
| 9 | **Error Recovery** | 3 / 5 | Search results provide clean feedback; minimal complex interactions. |
| 10 | **Help & Documentation** | 4 / 5 | The site's primary job—delivering arc42 guidance, examples, and tips—is executed with strong contextual callout blocks. |
| **Total** | | **30 / 40** | **Moderate / Refresh In Progress** |

---

## Anti-Patterns Verdict

### AI-Generated Slop Check: **Passed (0 / 5 AI Tells)**
The site shows zero hallmarks of AI-generated template slop:
- No gradient hero bands or floating glassmorphic cards.
- No generic icon grid boxes (e.g., 3-column Lucide icon grids).
- No fake metric counters ("10k+ Users", "99.9% Satisfaction").
- No generic dark-mode toggles or decorative background blobs.

### Generic / Dated Tells: **Present (3 Tells Remaining)**
1. **Pale Blue Header Band (`$brand-color: #d7ecf8`)**: Renders the old pale wash instead of the committed Deep Blue masthead (`#0e4f80`) with Header-Tint text (`#eaf4fc`).
2. **Deprecated Inline HTML Tags**: `_pages/home.md` and `_pages/keywords.html` use deprecated `<font color="#dd354b">` tags with hardcoded, un-tokenized red values.
3. **Unconstrained Measure**: `.site-content` takes 70% of a 1200px container (~840px), causing body prose to stretch to ~95–110 characters per line (violating the 65–75ch requirement in `DESIGN.md`).

---

## Overall Impression

The site is a clean, trustworthy, and fast technical reference. The recent addition of basic accessibility landmarks (`<main>`, `<nav>`, `.skip-link`, `:focus-visible`) removes major accessibility blockers.

The remaining gaps are visual and structural alignment with `DESIGN.md`:
1. The masthead still uses the legacy pale-blue wash instead of the Deep Blue band.
2. Long pages lack an in-page Table of Contents and Next/Previous Section navigation.
3. Markdown heading hierarchies across sections and includes are inconsistent.

---

## What's Working

1. **Accessibility Infrastructure**: `:focus-visible` outlines, skip-to-content links, semantic `<main>` / `<nav>` elements, and `aria-current="page"` navigation states are fully operational.
2. **Callout Guidance Architecture**: `.arc42-help` blocks (Help Blue `#e3f2fe` bg / `#0c3d66` ink) provide readable, high-contrast advice exactly where needed.
3. **Pure Content Focus**: No marketing fluff, sales funnels, or distracting animations.

---

## Priority Issues

### **[P1] Pale-blue Masthead & Low-Contrast Tagline vs. Deep-Blue Spec**
- **Location**: `_sass/base/_variables.scss`, `_sass/_header.scss`
- **Problem**: `$brand-color` is set to `#d7ecf8` (pale blue) and description uses `#fe5a83` (coral text on pale blue), failing AA contrast and violating `DESIGN.md` (which mandates Deep Blue `#0e4f80` masthead background and Header-Tint text `#eaf4fc`).
- **Fix**: Update `_variables.scss` and `_header.scss` to use `$deep-blue: #0e4f80` for masthead background, `#eaf4fc` for text/title, and reserve Coral (`#ff5c7c`) for small accent badges.
- **Suggested Command**: `/impeccable colorize`

### **[P1] Heading Hierarchy Inversion & Outline Drift**
- **Location**: `_pages/section-1.md` through `section-12.md`, `_includes/further-info.md`
- **Problem**: Markdown section pages render section titles as `h1`, subheads as `h2`, but `_includes/further-info.md` injects `## Further Info` (`h2`) and `### Tips` (`h3`) with article headers using `h4`. In some pages, headings skip levels (`h1` -> `h3`), breaking document outline for screen readers and SEO.
- **Fix**: Standardize section page outline: Page Title = `h1`, Subsections (1.1, 1.2) = `h2` (styled Signal Blue), Further Info = `h2`, Tips/Examples = `h3`.
- **Suggested Command**: `/impeccable typeset`

### **[P1] Lack of In-Page TOC & Prev/Next Section Stepper**
- **Location**: `_layouts/arc42-doc-section.html`, `_pages/section-*.md`
- **Problem**: Long reference pages (e.g. Section 1, 5, 8) contain extensive content with no in-page TOC or jump links, forcing users to scroll long distances. Pages end abruptly on sponsor blocks rather than a "Next Section" navigation control.
- **Fix**: Add a sticky or collapsible in-page TOC for section pages and a Next/Previous section footer navigation stepper.
- **Suggested Command**: `/impeccable layout`

### **[P2] Prose Reading Measure Too Wide (~95–110ch)**
- **Location**: `_sass/base/_layout.scss` (`.site-content`)
- **Problem**: `.site-content` width is `70%` of a `1200px` container (~840px), resulting in line lengths exceeding 95-110 characters for body text, violating the 65–75ch rule in `DESIGN.md`.
- **Fix**: Apply `max-width: 68ch` to `.post-content p, .post-content li` (while allowing wide tables and code blocks to use full container width).
- **Suggested Command**: `/impeccable layout`

### **[P2] Deprecated `<font>` Markup & Non-Token Red Palette Leaks**
- **Location**: `_pages/home.md`, `_pages/keywords.html`
- **Problem**: Files use legacy `<font color="#dd354b">` tags. `#dd354b` is a harsh red outside the design system palette.
- **Fix**: Replace `<font color="...">` with CSS classes or semantic elements utilizing tokenized colors (Signal Blue `#1675b9` or Coral `#ff5c7c`).
- **Suggested Command**: `/impeccable polish`

---

## Persona Red Flags

- **Sam (Accessibility-dependent reader)**:
  - *Status*: **Improved**. Keyboard focus rings, skip-to-content links, and landmarks are active.
  - *Remaining Issue*: Skipping heading levels in section subparts still causes outline confusion in screen readers.

- **Jordan (arc42 newcomer)**:
  - *Status*: **Needs Orientation**.
  - *Remaining Issue*: Raw template stubs (`<insert requirements overview>`, `… … …`) can look like broken page content to first-time readers.

- **Alex (Impatient power user)**:
  - *Status*: **Friction on Long Pages**.
  - *Remaining Issue*: No sticky on-page TOC to jump directly to subsection 1.2 or 1.3; search lacks a `/` shortcut.

- **Priya (Returning arc42 practitioner)**:
  - *Status*: **Good Guidance Lookup**.
  - *Remaining Issue*: No "Next Section" button at the bottom of section pages to seamlessly continue reviewing the 12-section structure.

---

## Minor Observations

- `_includes/subtle-ads.html` uses external htmx script loading; styled as an aside block.
- `_pages/keywords.html` contains legacy `<font>` tags in category headers.
- Tag pills in tip lists could use Tag Cyan (`#aee3f8`) background styling for better visual recognition.

---

## Questions to Consider

1. Should the Deep-Blue masthead (`#0e4f80`) be applied globally across all layouts, or should home/section layouts feature distinct header treatments?
2. How can in-page TOC generation be automated cleanly in Liquid/Kramdown without requiring manual TOC lists in every `section-*.md` file?
3. Should placeholder stubs (like `<insert...>`) be visually styled as callout badges ("Template Stub") so readers clearly distinguish reference guidance from fill-in instructions?
