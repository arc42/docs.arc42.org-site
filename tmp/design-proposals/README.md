# arc42 docs — three design proposals

Static, self-contained mockups to compare **layout, colour, and font** directions for
docs.arc42.org. They are **not** wired into Jekyll; they exist only to look at and choose from.

## How to view

Open **`index.html`** in a browser (it links to all six pages). Or open any page directly:

| Proposal | Home | Content page (Context view) |
|---|---|---|
| **A — Field Guide** | `a-fieldguide/home.html` | `a-fieldguide/section-3.html` |
| **B — Engineer's Handbook** | `b-handbook/home.html` | `b-handbook/section-3.html` |
| **C — The Spine** (alt nav) | `c-spine/home.html` | `c-spine/section-3.html` |

Fonts load from Google Fonts, so view them **online** for the intended typography (there are system
fallbacks otherwise). The arc42 logo is pulled from the repo via a relative path.

## The three directions

Every proposal obeys the same brief from `PRODUCT.md`, `DESIGN.md`, and the `/impeccable` critique:
calm reading centre, colour in the chrome and callouts, correct `h1 › h2` outline, ~65–75ch measure,
real focus states, cool-guidance / warm-example callouts, and the family's Signal Blue. They differ
in personality, and proposal **C** differs in the navigation model.

### A — "Field Guide, refreshed" · the safe, on-spec choice
Keeps the familiar **left sidebar** but fixes everything the critique flagged. Deep-blue masthead,
editorial serif headings (**Libre Caslon Text**) over a high-legibility body (**Atkinson
Hyperlegible**) — the documented arc42-family type target, so it reads as a sibling of
quality.arc42.org. Lowest risk.

### B — "Engineer's Handbook" · precise, technical
A **three-pane** documentation layout: left section rail + centre content + **right on-page TOC**
(directly answering the critique's "long page has no on-page TOC"). Flatter surfaces, cool slate
neutrals, a single committed workhorse sans (**Public Sans**) with strong weight contrast, monospace
figures (**Spline Sans Mono**). Feels like a well-set software manual.

### C — "The Spine" · the alternative navigation
Replaces the sidebar with a slim vertical **spine of the numbers 1–12** that mirrors arc42's
twelve-section structure — always visible, current section highlighted, names revealing on
hover/focus, plus a **prev/next stepper** at the foot of each page (the "clear next step" the
critique wanted). The freshest, liveliest face: warmer paper, a touch more coral and amber, display
grotesque headings (**Bricolage Grotesque**) over a warm body (**Hanken Grotesk**).

## What each proposal fixes from the critique

- Inverted heading outline → section name is now the page `<h1>`, subheads `<h2>`.
- Dated pale masthead → confident deep-blue (or navy) band with light text.
- No wayfinding → active nav state with `aria-current`, breadcrumb, prev/next; B and C add on-page
  TOC / a "you are here" header.
- Accessibility floor → skip link, `<main>`/`<nav>` landmarks, visible `:focus-visible` rings,
  named controls, reduced-motion respect.
- Measure too wide → prose capped at ~65–75ch.
- Cool/warm callouts → help is cool blue, example is warm blush, in every proposal.
- Sales-y peak-end → the training ad at the foot of the section page is replaced by a next-step
  stepper.

## Fonts used (all avoid the over-used defaults)

| | Headings | Body | Mono |
|---|---|---|---|
| A | Libre Caslon Text | Atkinson Hyperlegible | JetBrains Mono |
| B | Public Sans (heavy) | Public Sans | Spline Sans Mono |
| C | Bricolage Grotesque | Hanken Grotesk | JetBrains Mono |
