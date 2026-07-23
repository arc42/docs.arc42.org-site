---
name: arc42 Documentation
description: The public documentation site for the arc42 architecture template.
colors:
  signal-blue: "#1675b9"
  signal-blue-dark: "#115e94"
  deep-blue: "#0e4f80"
  sky-tint: "#dceefa"
  header-tint: "#eaf4fc"
  coral: "#ff5c7c"
  amber: "#ffc95c"
  help-bg: "#e3f2fe"
  help-ink: "#0c3d66"
  example-bg: "#fdebe7"
  example-ink: "#9a3b2e"
  example-ink-dark: "#7d2f24"
  example-icon: "#c8654f"
  tag-bg: "#aee3f8"
  emerald: "#2e9e67"
  maroon: "#8a2e2e"
  maroon-bg: "#fcefef"
  ink: "#2a2e34"
  paper: "#fcfdff"
  muted: "#5e6975"
  surface-1: "#f2f5f8"
  surface-2: "#f7fafd"
  surface-hover: "#e7eef5"
  code-bg: "#f6f8fa"
  hairline: "rgba(20,44,82,0.12)"
  hairline-2: "rgba(20,44,82,0.16)"
typography:
  display:
    fontFamily: "'Libre Caslon Text', Georgia, serif"
    fontSize: "clamp(1.8rem, 1.2rem + 2.2vw, 2.6rem)"
    fontWeight: 700
    lineHeight: 1.1
  headline:
    fontFamily: "'Libre Caslon Text', Georgia, serif"
    fontSize: "clamp(2rem, 1.4rem + 2.4vw, 2.85rem)"
    fontWeight: 700
    lineHeight: 1.12
  title:
    fontFamily: "'Libre Caslon Text', Georgia, serif"
    fontSize: "1.55rem"
    fontWeight: 700
    lineHeight: 1.2
  body:
    fontFamily: "'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', system-ui, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 400
    lineHeight: 1.3
  code:
    fontFamily: "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
    fontSize: "0.9em"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  xs: "3px"
  sm: "4px"
  input: "0.3em"
  pill: "1.5em"
spacing:
  side: "10px"
  section: "50px"
components:
  button-default:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.signal-blue}"
    rounded: "{rounded.input}"
    padding: "0.5em 0.75em"
  button-hover:
    backgroundColor: "{colors.signal-blue}"
    textColor: "{colors.paper}"
    rounded: "{rounded.input}"
    padding: "0.5em 0.75em"
  callout-help:
    backgroundColor: "{colors.help-bg}"
    textColor: "{colors.help-ink}"
    rounded: "{rounded.sm}"
    padding: "16px 48px 16px 20px"
  callout-example:
    backgroundColor: "{colors.example-bg}"
    textColor: "{colors.example-ink}"
    rounded: "{rounded.sm}"
    padding: "16px 48px 16px 20px"
  code-inline:
    backgroundColor: "#f6f8fa"
    textColor: "{colors.ink}"
    rounded: "{rounded.xs}"
    padding: "0 5px"
  tag:
    backgroundColor: "{colors.tag-bg}"
    textColor: "{colors.signal-blue-dark}"
    rounded: "{rounded.pill}"
    padding: "2px 10px"
  masthead:
    backgroundColor: "{colors.deep-blue}"
    textColor: "{colors.header-tint}"
    padding: "16px 10px"
---

# Design System: arc42 Documentation

## 1. Overview

**Creative North Star: "The Field Guide, refreshed"**

This is a reference you flip through fast, not a brochure you admire. The whole system serves one job: a practicing architect or a newcomer has a section open and needs to find "what belongs here, and how do I do it well" in seconds, then get back to work. Every visual decision is measured against that. The bones stay the same as they always were: clear entries, scannable structure, generous whitespace, comfortable measure, a calm reading surface where the content is the hero. What changes with this revision is the surface temperature. The site now reads as a current, colour-aware member of the arc42 family (alongside arc42.org and quality.arc42.org), not an austere blue-on-white outlier.

The move is deliberate and contained: **colour is concentrated in the chrome and the callouts, while the reading surface stays quiet.** A confident deep-blue masthead replaces the old pale wash. The help and example callouts get fresher, warmer, better-matched colour pairs. Links, section markers, and tags carry the signature blue. But body text still sits on near-white paper in soft ink, at 65 to 75 characters per line, because that is where a long reference is actually read. Freshness lives at the edges; the centre stays calm. Signal Blue remains this site's signature within the family the way teal-green is quality.arc42.org's: shared style, per-site hue.

This system still explicitly rejects the same things, now with two more. It is **not a salesy marketing page or brochure**: no gradient heroes, no fabricated metrics, no conversion-funnel CTAs, no sales sheen. It is **not a heavy enterprise documentation portal**: no dense, bureaucratic chrome. It is **not trendy or gimmicky**: adding colour is not licence for neon, glassmorphism, dark-mode-for-cool, or gratuitous motion. It is **not a sterile generic template**, **not AI-generated slop** (no identical icon-card grids, no hero-metric templates, no interchangeable stock layouts), and **not cluttered information overload** (whitespace and hierarchy always win over density).

**Key Characteristics:**
- Near-white paper, soft cool ink, one confident Signal Blue carrying links, titles, and structure.
- Colour concentrated at the edges: a saturated deep-blue masthead, refreshed help (cool) and example (warm) callouts, colour-coded links and tags. The reading surface stays calm.
- Functional and family-aware colour: blue for structure and action, cool blue for guidance, warm blush for examples, a single coral spark, plus amber, emerald, and maroon quarantined to specific jobs.
- Roomy 50px vertical rhythm; a two-column read (content + aside nav) on desktop.
- Flat surfaces with one signature hard offset shadow reserved for annotation-style callouts. That tactile "pinned note" remains arc42's signature.

## 2. Colors

A blue-forward palette on near-white, warmed and freshened so it reads as one of the arc42 family. Hue does real work here: it separates structure from guidance from example from action, and it carries family identity, rather than decorating.

### Primary
- **Signal Blue** (#1675b9): The load-bearing colour. Carries links, section titles, `h2` headings, header-links, and the primary button fill on hover. When something is this blue, it means "this is the structure" or "this is actionable." This is the site's signature hue within the arc42 family, kept from the previous design so the site stays recognizably itself.
- **Deep Blue** (#0e4f80): The confident, saturated masthead fill and the footer's top rule. New in this revision. It replaces the old pale sky wash so the header reads as a bold family-style colour band with light text, matching the saturated-header treatment quality.arc42.org uses (in teal-green). Reserved for the masthead band, the footer rule, and the offset callout shadow.

### Secondary
- **Sky Tint** (#dceefa): A pale, calm blue wash for soft secondary surfaces such as article header panels. A quiet relative of the signature blue, never used behind long body text.
- **Header Tint** (#eaf4fc): The near-white text, logo, and title colour that sits on the Deep Blue masthead. High contrast against the band, so the identity reads cleanly at the top of every page.

### Tertiary
- **Help Blue** (#e3f2fe background / #0c3d66 ink): The `.arc42-help` guidance callout. A fresher, slightly brighter cool blue than before, with a deep readable blue ink (replacing the old near-black-blue). Cool, quiet, clearly "the template's advice."
- **Example Blush** (#fdebe7 background / #9a3b2e ink): The `.arc42-example` block. Warmed from the old flat pink toward a fresh blush, with a matched warm ink instead of the previous blue ink, echoing the family habit of pairing a warm background with a warm text colour. A clear warm counterpoint to the cool help block, so guidance and worked example read apart at a glance.
- **Coral** (#ff5c7c): The single warm spark. Used for the masthead description line and small header accents (counters, markers), never on body content. One warm note against the deep blue.
- **Amber** (#ffc95c): A secondary warm accent for tips and lightweight emphasis, borrowed from the family's "standards" colour. Used sparingly, always paired with text or an icon, never as the sole signal.
- **Tag Cyan** (#aee3f8): Tag and label pills.
- **Emerald** (#2e9e67): The footer status indicator only. Signals "operational" and nothing else, deepened from the old value for legibility.
- **Maroon** (#8a2e2e): The subtle-ad border and accent. Quarantined to sponsor blocks; never used in editorial content.

### Neutral
- **Ink** (#2a2e34): Body text. A soft near-black with a faint cool tint, easier on the eyes than pure black across long reading sessions.
- **Paper** (#fcfdff): The page. Near-white with the faintest cool tint, never pure `#fff`. The content sits directly on it.
- **Muted** (#5e6975): Blockquote text and de-emphasized meta, a cool grey.
- **Hairline** (rgba(20,44,82,0.12)): Table borders, aside nav dividers, input strokes. A blue-tinted hairline.
- **Hairline 2** (rgba(20,44,82,0.16)): The same hairline where it must actually be *seen* — the stepper's boxes, directory rows, input strokes. Plain Hairline over Paper measures 1.26:1, which reads as no border at all; anything asked to look like a container uses this instead.

### Surfaces
Three tinted surfaces, one job each. There are deliberately only three.
- **Surface 1** (#f2f5f8): Tinted chrome panels — the navigation rail and the footer.
- **Surface 2** (#f7fafd): The faintest wash — table headers and zebra rows.
- **Surface Hover** (#e7eef5): Every interactive hover fill, on both Paper and Surface 1.
- **Code** (#f6f8fa): Inline code and code blocks. Neutral, not blue-tinted — see the One Blue Rule.

### Named Rules
**The Functional-and-Family Colour Rule.** Colour earns its place by carrying meaning or family identity, never by decorating. Blue means structure or action; cool blue means guidance; warm blush means example; coral and amber are warm accents; green means status; maroon means sponsor; the deep-blue band means "this is the arc42 masthead." If a colour is doing none of those jobs, it does not belong on the page.

**The Calm-Centre Rule.** Colour is concentrated in the chrome and the callouts. Body text is always soft ink on near-white paper. Never tint the reading surface behind long-form prose, and never put a saturated fill behind running text. Freshness lives at the edges; the centre stays quiet.

**The One Blue Rule.** There is a single editorial blue (#1675b9). Deep Blue, Sky Tint, Header Tint, and Signal Blue Dark are its darker and lighter family relatives for chrome. Do not introduce a second competing accent blue into content.

Signal Blue Dark (#115e94) is not a second accent — it is Signal Blue where Signal Blue cannot clear AA: hover states, and small or pilled text that would otherwise land in the 3.5–4.5:1 band. Reach for it because of a contrast measurement, never because of taste.

**The Three-Surfaces Rule.** Tinted surfaces are limited to the three named above plus the code wash. A design draft once carried eight near-identical near-white blues, all within lightness 0.93–0.98 — indistinguishable in use and impossible to choose between. If a new surface seems necessary, it is almost certainly one of the three with a different job description.

**The Colour-Is-Never-Alone Rule.** Colour never carries meaning by itself. Every coloured signal is paired with text, an icon, or a shape, so the site stays legible for colour-blind readers and in any lighting.

## 3. Typography

**Display / Heading Font:** Libre Caslon Text (Georgia, Times New Roman, serif fallback)
**Body Font:** Atkinson Hyperlegible Next (Atkinson Hyperlegible, system-ui fallback)
**Mono Font:** the system monospace stack (`ui-monospace`, SF Mono, Menlo, Consolas)

**Character:** An editorial serif for headings over a body face engineered for maximum legibility. The serif gives the reference an authored, considered voice; the body face does the real work across long reading sessions. Monospace is reserved for the 01–12 section numbers and for code, so figures line up and read as an index rather than as prose.

> **Decision landed (2026-07-22).** The typeface refresh is now committed and aligns with what quality.arc42.org ships: **Atkinson Hyperlegible Next** for body and UI, **Libre Caslon Text** for headings. Both are **self-hosted** (`assets/fonts/`, SIL OFL) rather than loaded from the Google Fonts CDN — a third-party font hop is both a render-blocking dependency and a privacy liability for a site with an imprint. Plain *Atkinson Hyperlegible* is kept as the immediate fallback so the stack degrades to the right letterforms rather than to `system-ui`; the two are different families with different metrics, so the order matters. Mono is the system stack — no downloaded mono face, because its only jobs are section numbers and inline code.

### Hierarchy
- **Display** (bold, 2.7em, line-height 1): The masthead title only. Appears once per page, in Header Tint on the Deep Blue band.
- **Headline** (bold, 2.3em, line-height 1.3): Page `h1`, in ink. The section's name.
- **Title** (bold, 1.8em, line-height 1.3, Signal Blue): Major `h2` subheads. Blue on purpose, so the reader can scan the structural skeleton of a long page by colour alone.
- **Body** (regular, 16px, line-height 1.5): All prose. Comfortable leading for extended reading. Target 65 to 75 characters per line.
- **Label** (regular, 0.95em, line-height 1.2): Aside navigation, meta lines, tags, footnotes.
- **Code** (regular, 0.85em monospace): Inline code and code blocks.

### Named Rules
**The Blue-Subhead Rule.** `h2` section headings are Signal Blue while `h1` stays ink. This lets a reader scan a long section page and perceive its structure at a glance. It is a navigation aid, not decoration, so do not extend the blue to `h1` or body text.

**The Comfortable Measure Rule.** Body copy targets 65 to 75 characters per line. On wide desktop the content column must not let prose run the full width; long unbroken measures are the enemy of a reference read at length.

## 4. Elevation

Mostly flat. The page is near-white, the content sits directly on it, and structure is conveyed through spacing, hairline rules, and tonal background tints rather than through stacked shadows. There is one deliberate exception: annotation-style callouts.

### Shadow Vocabulary
- **Callout Lift** (`box-shadow: 3px 3px 0 0 rgba(14,79,128,1)`): The signature hard offset shadow under `.arc42-help` blocks, now tuned to Deep Blue. A hard, colored, directional drop shadow that makes the callout read like a note pinned onto the page. This is arc42's tactile signature, not a generic Material elevation.
- **Sponsor Lift** (`box-shadow: 3px 3px 0 0 rgba(138,46,46,1)`): The same offset treatment in maroon, reserved for `.subtle-ad` sponsor blocks so they read as "attached" rather than part of the editorial flow.

### Named Rules
**The Flat-Page, Lifted-Note Rule.** The document itself is flat. The signature offset shadow is reserved exclusively for callout and sponsor blocks, the things that are annotations *on* the page rather than part of it. Never put this shadow on a heading, a table, or an ordinary content container.

## 5. Components

### Buttons
- **Shape:** Gently rounded (0.3em radius), 1px solid border.
- **Default:** Paper fill, Signal Blue text and border, padding 0.5em 0.75em. Reads as a quiet outlined control.
- **Hover:** Fills with Signal Blue, text flips to Paper, underline removed. A clear, confident state flip with no ornament.
- **Focus:** A visible 2px Signal Blue outline with 2px offset. Keyboard users must always see where they are.

### Callouts (signature component)
The heart of the system. Two annotation blocks that structure every documentation section.
- **Help block** (`.arc42-help`): Help Blue background (#e3f2fe), deep-blue ink (#0c3d66), 4px radius, Callout Lift shadow, roomy 16px/48px/16px/20px padding, 1.5 line-height, and a `help42.svg` icon pinned top-right (absolutely positioned, not floated, so it never crowds the first line of text). Carries the template's guidance.
- **Example block** (`.arc42-example`): Example Blush background (#fdebe7), matched warm ink (#9a3b2e), same 4px radius, same roomy padding and top-right info icon. No shadow, so it reads as lighter than a help block. Carries worked examples.
- **Rule:** Help is cool blue, example is warm blush, always. The temperature pairing (cool guidance, warm illustration) is how the reader tells advice from example at a glance.

### Code
- **Inline** (`code`): Faint cool-gray background (#f6f8fa), 1px hairline border, 3px radius, small horizontal padding. A subtle chip, not a loud highlight.
- **Block** (`pre`): 1px hairline border, faint gray background, 3px radius, horizontal scroll on overflow. Rouge syntax highlighting.

### Tags
- **Style:** Tag Cyan (#aee3f8) pill, **Signal Blue Dark (#115e94)** text, full pill radius, 2px 10px padding. Small, secondary, used for post taxonomy.
- **Contrast note:** this component previously specified Signal Blue (#1675b9) on Tag Cyan, which measures **3.54:1** and fails AA at every size a tag is ever set in. Signal Blue Dark on the unchanged Tag Cyan measures **4.96:1**. Do not revert the ink to #1675b9; the pill background is the part that carries the identity.
- **Always a link.** Tags name a keyword that has a page. A tag that is not a link is a visible dead end — point it at `/keywords/#<tag>`.

### Navigation
- **Aside nav:** A vertical list of section links with hairline top/bottom borders per item, roomy 0.5em padding, label-scale type. Collapses behind a toggle below 800px. Quiet and list-like; the current structure of the twelve sections, not a chrome-heavy menu.
- **Masthead:** A confident Deep Blue (#0e4f80) band with a circular avatar, Header Tint (#eaf4fc) title and logo, and a single Coral (#ff5c7c) description line. This is the fresh, family-style header: colour lives here so the reading surface below can stay calm.

### Blockquotes
- **Style:** 5px gray left border (#ddd), Muted text, 0.5em 1em padding. This is a conventional quotation mark, not a coloured accent stripe on a card. The left border stays gray, never a brand colour.

### Sponsor / training note (`.subtle-ad`)
The arc42 training funds this free site, so the note stays, but it must read as an honest pointer from the maintainers, never a foreign ad. Site sans (never a serif that appears nowhere else), a small maroon "from the arc42 team" kicker, information-first copy, and one quiet maroon link (no shouting button). Warm maroon-tinted background (#fcefef) with a 1px Maroon (#8a2e2e) border and the maroon Sponsor Lift hard offset, so it reads as an aside attached to the page. It lives in an `<aside aria-label>`, outside the editorial flow. The colour and the kicker openly declare "this is us, and it is a sponsor note," which is exactly what keeps it from feeling like a hidden ad.

## 6. Do's and Don'ts

### Do:
- **Do** concentrate colour in the chrome and callouts, and keep body text as soft Ink on near-white Paper. Freshness at the edges, a calm centre.
- **Do** use colour functionally and for family identity: Signal Blue for structure and action, Help Blue for guidance, Example Blush for examples, Coral and Amber as sparing warm accents, Emerald only for status, Maroon only for sponsor blocks, Deep Blue for the masthead band.
- **Do** colour `h2` subheads Signal Blue so a reader can scan a long section's skeleton at a glance.
- **Do** cap body measure at 65 to 75 characters; constrain the content column so prose never runs full desktop width.
- **Do** reserve the signature hard offset shadow for callout and sponsor blocks only, the things that are annotations on the page.
- **Do** distinguish help (cool blue) from example (warm blush) callouts by temperature, every time, and always pair colour with text or an icon.
- **Do** feel like one arc42 family: share the saturated-header style and warm-plus-cool palette logic with arc42.org and quality.arc42.org.

### Don't:
- **Don't** build a **salesy marketing page or brochure**: no gradient heroes, no fabricated metrics, no conversion-funnel CTAs, no "sign up now" energy, no sales sheen.
- **Don't** drift toward a **heavy enterprise documentation portal**: no dense, cluttered, bureaucratic chrome or deep nested megamenus.
- **Don't** mistake "more colour" for **trendy or gimmicky**: no neon, no glassmorphism, no dark-mode-for-cool, no gratuitous animation. Colour carries meaning and identity, used with restraint.
- **Don't** settle for a **sterile generic template**: no anonymous default-framework look with no arc42 identity.
- **Don't** ship **AI-generated slop**: no identical icon-and-heading card grids, no gradient hero-metric templates, no decorative glassmorphism, no interchangeable stock layouts.
- **Don't** create **cluttered information overload**: no stacked competing callouts, no dense sidebars fighting the text, nothing that buries the content. Whitespace and hierarchy win.
- **Don't** tint the reading surface behind long-form prose, and never put a saturated fill behind running text.
- **Don't** introduce a second competing accent blue into editorial content; there is one editorial blue.
- **Don't** put the offset callout shadow on headings, tables, or ordinary content containers.
- **Don't** use `border-left` greater than 1px as a coloured accent stripe on cards, list items, or alerts. The gray blockquote rule is the only permitted left border, and it stays gray.
- **Don't** use gradient text or `background-clip: text`. Emphasis comes from weight, size, and the one blue.
- **Don't** let colour be the only carrier of meaning; always pair it with text, an icon, or a shape.
