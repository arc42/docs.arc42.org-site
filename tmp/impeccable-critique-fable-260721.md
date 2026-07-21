# /impeccable critique: arc42 documentation section page

**Target:** `_layouts/arc42-doc-section.html` (judged via rendered `/section-1/`, `/section-7/`, `/home/`, `/examples/`)
**Date:** 2026-07-21 · **Register:** brand · **Method:** independent LLM design review + deterministic detector, synthesized

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Active-nav state and skip link are solid; no in-page position cue (TOC/back-to-top) on 1,600-line pages |
| 2 | Match System / Real World | 3 | Speaks fluent architect; raw `<insert requirements overview>` placeholders leak template internals at readers |
| 3 | User Control and Freedom | 3 | Persistent 12-section nav + search give exits; no intra-page escape on very long sections |
| 4 | Consistency and Standards | 2 | Sub-section heading levels differ between section-1 and section-7; two accent reds; four near-miss blues vs the One Blue Rule; duplicate `<title>` in head |
| 5 | Error Prevention | 3 | Placeholder headings could mislead a copy-paster into thinking the page is the template itself |
| 6 | Recognition Rather Than Recall | 3 | Help vs example blocks distinguished only by tint + unlabeled corner icon (violates the site's own Colour-Is-Never-Alone rule) |
| 7 | Flexibility and Efficiency | 2 | No in-page TOC, no anchor-jump aid for a 24-tip page, no keyboard accelerators |
| 8 | Aesthetic and Minimalist Design | 2 | Bottom half is a wall of 24 identical tinted panels with redundant `<hr>`s; ~110-char line length |
| 9 | Error Recovery | 2 | Minimal error surface (static site); htmx ad-fetch fails silently to a local fallback, which is fine |
| 10 | Help and Documentation | 4 | The product is documentation and it practices it: contextual examples inside guidance, FAQ links, search |
| **Total** | | **27/40** | **Acceptable (top of band, one point below Good)** |

## Anti-Patterns Verdict

**Does this look AI-generated? No, decisively.**

**LLM assessment:** Zero generative tells. No gradient text, no glassmorphism, no icon-card grids, no hero-metric templates, no colored side-stripes (the 5px blockquote border is gray and sanctioned by DESIGN.md). The "144 tips and 35 examples" count is real and computed, not fabricated. What the page reads as instead is a human-maintained ~2015 Jekyll theme with visible hand-editing scars: a `<font color="#dd354b">` tag on home, a stray `<em>**</em>` artifact in section-7, float/clearfix layout, jQuery. The brand risk is "dated and drifted," not "machine-generated."

**Deterministic scan** (4 rendered pages): after false-positive analysis, three real findings.
- **Skipped heading levels (2 warnings), which the LLM review missed:** home jumps h1 → h3 at "We stand with the people of Ukraine"; the examples page jumps h1 → h4 at the subtle-ad's "Prefer to learn arc42 hands-on?" (on section pages, h2s precede it, so the include only breaks outlines on pages without intermediate headings).
- **Marketing buzzword (1):** "shorten or streamline your documentation" on home. Borderline: it describes literal behavior, but "streamline" is on the stock-phrase list and an easy rewrite.
- **False positive (4 hits):** "skip-link text is rgb(0,0,0), outside DESIGN.md." The compiled CSS actually styles it #1675b9 background with white text; the detector's DOM pass cannot resolve the external stylesheet. One legitimate footnote from it: the skip-link text is pure `#fff` where the palette says never-pure-white paper `#fcfdff`.

## Overall Impression

The bones are genuinely good and the recent hardening is real: the semantic floor (landmarks, focus states, aria-current, reduced motion) now beats most documentation sites. What is left is a gap between paper and pixels. DESIGN.md describes a fresh, colour-aware member of the arc42 family, but the shipped chrome is still the old pale-wash header, the old navy callout ink, and an unconstrained 110-character measure. The single biggest opportunity: implement the DESIGN.md tokens that currently exist only in the spec and, ironically, in the sponsor block, which is now the most on-brand component on the site.

## What's Working

1. **The callout-heading normalization** (`_sass/_content.scss`): headings inside `.arc42-help`/`.arc42-example` render as compact 1.05em labels while keeping their semantic levels. The outline stays honest without shouting.
2. **The accessibility hardening is real, not cosmetic:** skip link with slide-in, universal `:focus-visible` ring, `prefers-reduced-motion` respect, `aria-current="page"` paired with a visible bold+tint state, visually-hidden h1 on home.
3. **The `.subtle-ad` is the best-executed component on the site:** kicker line, quarantined maroon, hard offset shadow, honest information-first copy, measure-capped at 34em. It matches DESIGN.md line for line.

## Priority Issues

**[P1] Unconstrained prose measure (~110 characters per line)**
- **Why it matters:** DESIGN.md's Comfortable Measure Rule (65 to 75 chars) is the most emphasized readability rule for this text-heavy reference, and it is violated on every section page. Only the ad box is measure-capped.
- **Fix:** `max-width: ~46em` on the article content within `.site-content`, left-aligned in the column.
- **Suggested command:** `/impeccable typeset`

**[P1] The DESIGN.md refresh is mostly aspirational; the chrome still ships the old design**
- **What:** masthead is still pale `#d7ecf8` with `#397ab2` title (target: Deep Blue `#0e4f80` band with Header Tint text); both callouts use navy `#002080` ink (targets: `#0c3d66` cool help / `#9a3b2e` warm example, so the signature cool/warm temperature pairing does not exist yet); the help shadow is blurred, not the signature hard offset.
- **Why it matters:** the brand promise "modern, fresh, part of the refreshed family" hinges almost entirely on these tokens. Today only the sponsor block got the refresh.
- **Fix:** implement the frontmatter tokens in `_sass/base/_variables.scss` and `assets/css/arc42-doc.css`: masthead band, callout inks, hard-offset Callout Lift.
- **Suggested command:** `/impeccable colorize`

**[P1] Contrast failures in the header and tags**
- **What:** coral description `#fe5a83` on `#d7ecf8` is roughly 2.5:1 (fails even the 3:1 large-text bar) and sits on every page; tag-pill text `#1675b9` on `#aee3f8` is roughly 3.5:1 at small size (fails AA 4.5:1).
- **Why it matters:** PRODUCT.md commits to AA spirit; both are sitewide.
- **Fix:** move the coral line onto the target Deep Blue band (where `#ff5c7c` passes) or darken it; darken tag text or lighten the pill.
- **Suggested command:** `/impeccable colorize` (falls out of the token implementation above)

**[P2] The 24-tip stack buries the "Further Info" payoff**
- **What:** every tip renders as a full tinted panel with a decorative `fa-tags` icon (missing `aria-hidden`), tag pills, an empty `ul.meta`, plus an `<hr>` between every pair.
- **Why it matters:** it is the least scannable part of the page for the audience that scans most, and it is the page's visual ending (peak-end: the visit closes on repetition, then the ad).
- **Fix:** compact link list grouped by subsection (1.1 / 1.2 / 1.3); drop the panel chrome, redundant `<hr>`s, and empty meta list.
- **Suggested command:** `/impeccable layout`

**[P2] Template and QA debris undermines "expert, current"**
- **What:** rendered `<em>**</em>` in section-7.1's help block; an empty `<h4>` in section-7; `:Overview Example:` colon-prefixed titles; deprecated `<font color="#dd354b">` on home (a second, off-palette red); duplicate `<title>` in head (jekyll-seo-tag already emits one); `id="search-results"` duplicated 3x per page; `id="motivation"` duplicated in section-7; the two skipped-heading warnings from the detector (Ukraine banner h3 on home, subtle-ad h4 on heading-less pages).
- **Why it matters:** newcomers read rendering artifacts as "this page is broken"; duplicate IDs and titles break assistive-tech assumptions.
- **Fix:** a content sweep plus three one-liners (drop the layout's own `<title>`, unique include IDs, demote the ad heading to a styled `<p><strong>`).
- **Suggested command:** `/impeccable polish`

## Cognitive Load

3 failures of 8: moderate. Chunking (flat ungrouped stack of up to 24 tip panels), visual hierarchy in the lower half (every panel identical weight, double-separated), and borderline on minimal choices (15 nav items, mitigated because 12 are intrinsic arc42 structure). Passes: single focus, grouping of examples inside guidance (genuinely good IA), one-thing-at-a-time, working memory, progressive disclosure.

## Persona Red Flags

**Alex (impatient expert, ~50% of audience):** gets "what belongs here" within seconds (h1 + guidance callout above the fold). Red flags: no in-page TOC or back-to-top, so reaching tip 19 means scrolling a wall of identical panels; 110-char lines slow the exact scan the design claims to serve; no keyboard accelerator for search.

**Jordan (newcomer, ~50% of audience):** `<insert requirements overview>` and `< insert table of quality goals here>` styled as real headings read as a broken page, not a template slot; the `<em>**</em>` artifact confirms the suspicion; help vs example blocks carry no textual label saying "this is arc42's advice," only tint and an unlabeled icon.

**Sam (screen reader / keyboard):** strengths first: skip link, focus rings, aria-current, reduced motion all present. Red flags: `.nav-toggle` has `aria-controls` but no `aria-expanded` state; duplicate `id="search-results"` and duplicate `<title>`; document outline ranks section-7's callout labels (h2) above its actual sub-sections (h3), inconsistent with section-1; decorative `fa-tags` icons lack `aria-hidden`.

## Minor Observations

- The editorial callouts lost the signature hard-offset "pinned note" shadow (blurred instead) while the ad kept it; the sponsor block currently wears more arc42 identity than the guidance does.
- `nutshell.js` loads synchronously in `<head>` (no defer); htmx pulled from unpkg on every page for the ad swap.
- Footer status icon is `#50C878`, not the palette's `#2e9e67` (aria-hidden decorative, low stakes).
- The aside takes 30% of a 1200px shell for a 15-link list; content gets 70%.
- "streamline your documentation" on home: an easy rewrite away from the stock-phrase list.
- Footer's `/imprint` link (no trailing slash) causes a needless redirect hop under `permalink: pretty`.
- Skip-link text is pure `#fff`; palette paper is `#fcfdff`.

## Questions to Consider

1. On section pages, 70 to 80% of the actual content lives inside tinted help callouts. At that point is the callout still an "annotation on the page," or has the tinted box quietly become the reading surface, structurally violating the Calm-Centre rule the system is built on?
2. Why does the sponsor note get the brand's signature hard-offset shadow, a measure cap, a kicker label, and a matched ink (every refinement DESIGN.md promises) while the editorial guidance blocks get none of them? The ad is currently the most designed thing on the page.
3. Is this site the arc42 template or a reference about the template? The raw `<insert…>` placeholders say "template," the tips and examples say "reference." Until that is decided, newcomers will keep reading the placeholders as broken pages.

---

**Trend for `layouts-arc42-doc-section-html` (last 3 runs): 29 (2026-07-10) → 28 (2026-07-20) → 27 (2026-07-21)**
Snapshot: `.impeccable/critique/2026-07-21T09-40-50Z__layouts-arc42-doc-section-html.md`

---

## Recommended Actions (hand-off)

Priority order, with the context each command needs:

1. **`/impeccable colorize`** (assigned to a separate agent): implement the DESIGN.md tokens that are still aspirational. Concretely: masthead becomes a Deep Blue `#0e4f80` band with Header Tint `#eaf4fc` title/logo and the Coral `#ff5c7c` description line (passes contrast on the dark band, fixing the 2.5:1 failure); help callout ink `#002080` → `#0c3d66`, example callout ink `#002080` → `#9a3b2e` (establishes the cool/warm pairing); help shadow becomes the hard offset `3px 3px 0 0 rgba(14,79,128,1)` (currently blurred); tag pills need ≥4.5:1 (darken text or lighten `#aee3f8`); consolidate the near-miss blues (`#397ab2`, `#002080`, `#0b52b9`) onto the One Blue Rule (`#1675b9` + chrome relatives); footer status icon `#50C878` → `#2e9e67`. Files: `_sass/base/_variables.scss`, `_sass/_header.scss`, `assets/css/arc42-doc.css`.
2. **`/impeccable typeset`**: cap prose measure at ~46em within `.site-content`; the 65–75ch Comfortable Measure Rule is violated on every section page.
3. **`/impeccable layout`**: rework the 24-tip "Further Info" stack into a compact link list grouped by subsection; drop panel chrome, redundant `<hr>`s, empty `ul.meta`.
4. **`/impeccable polish`**: debris sweep: `<em>**</em>` in section-7.1, empty `<h4>`, `:Overview Example:` colon titles, `<font color="#dd354b">` on home, duplicate `<title>` (remove the layout's own; jekyll-seo-tag emits one), duplicate `id="search-results"`/`id="motivation"`, Ukraine-banner h1→h3 skip on home, subtle-ad `<h4>` → styled `<p><strong>` (fixes the h1→h4 skip on the examples page), `aria-expanded` on `.nav-toggle`, `aria-hidden` on decorative `fa-tags` icons.

Open design question for the maintainers (not blocking): how to present the `<insert…>` template placeholders so newcomers read them as intentional slots rather than broken pages.
