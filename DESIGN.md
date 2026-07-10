---
name: arc42 Documentation
description: The public documentation site for the arc42 architecture template.
colors:
  signal-blue: "#1675b9"
  steel-blue: "#397ab2"
  sky-tint: "#d7ecf8"
  coral: "#fe5a83"
  help-bg: "#dcf0ff"
  help-ink: "#002080"
  example-bg: "#fde2e5"
  tag-bg: "#aee3f8"
  emerald: "#50c878"
  maroon: "#800000"
  ink: "#383838"
  paper: "#ffffff"
  muted: "#777777"
typography:
  display:
    fontFamily: "Helvetica, Arial, sans-serif"
    fontSize: "2.7em"
    fontWeight: 700
    lineHeight: 1
  headline:
    fontFamily: "Helvetica, Arial, sans-serif"
    fontSize: "2.3em"
    fontWeight: 700
    lineHeight: 1.3
  title:
    fontFamily: "Helvetica, Arial, sans-serif"
    fontSize: "1.8em"
    fontWeight: 700
    lineHeight: 1.3
  body:
    fontFamily: "Helvetica, Arial, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Helvetica, Arial, sans-serif"
    fontSize: "0.95em"
    fontWeight: 400
    lineHeight: 1.2
  code:
    fontFamily: "Consolas, Monaco, 'Andale Mono', monospace"
    fontSize: "0.85em"
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
    lineHeight: 1.5
  callout-example:
    backgroundColor: "{colors.example-bg}"
    textColor: "{colors.help-ink}"
    rounded: "{rounded.sm}"
    padding: "16px 48px 16px 20px"
    lineHeight: 1.5
  code-inline:
    backgroundColor: "#fafafa"
    textColor: "{colors.ink}"
    rounded: "{rounded.xs}"
    padding: "0 5px"
  tag:
    backgroundColor: "{colors.tag-bg}"
    textColor: "{colors.signal-blue}"
    rounded: "{rounded.sm}"
    padding: "4px 6px"
---

# Design System: arc42 Documentation

## 1. Overview

**Creative North Star: "The Field Guide"**

This is a reference you flip through fast, not a brochure you admire. The whole system serves one job: a practicing architect has a section open in their editor and needs to find "what belongs here and how do I do it well" in seconds, then get back to work. Every visual decision is measured against that. Clear entries, scannable structure, generous whitespace, and a calm blue-forward palette that stays out of the reading's way. The content is the hero; the design recedes.

The character is expert, clear, and pragmatic: the voice of an experienced practitioner sharing hard-won advice. Structure is treated as a feature, mirroring arc42's own disciplined twelve-section shape. Color is used functionally, not decoratively, to mark what is guidance, what is an example, and what is actionable. White page, dark ink, one confident blue.

This system explicitly rejects four things. It is **not a salesy SaaS landing page**: no gradient heroes, no fabricated metrics, no conversion-funnel CTAs. It is **not a heavy enterprise documentation portal**: no dense, cluttered, bureaucratic chrome. It is **not trendy or flashy**: no neon, no glassmorphism, no dark-mode-for-cool, no gratuitous motion. And it is **not a sterile generic template**: it should feel like arc42, not like an anonymous framework starter.

**Key Characteristics:**
- White paper, dark-gray ink, a single confident Signal Blue carrying links, titles, and headings.
- Functional color coding: blue for guidance callouts, soft pink for examples.
- Roomy 50px vertical rhythm between blocks; a two-column read (content + aside nav) on desktop.
- Flat surfaces with one signature offset shadow reserved for annotation-style callouts.
- Sans-serif throughout, monospace for code. No decorative type.

## 2. Colors

A functional, blue-forward palette on white. Hue does work here: it separates guidance from example from action, rather than decorating.

### Primary
- **Signal Blue** (#1675b9): The load-bearing color. Carries links, section titles, `h2` headings, header-links, and the primary button fill on hover. When something is this blue, it means "this is the structure" or "this is actionable." Also the footer's top rule and article panel headings.

### Secondary
- **Steel Blue** (#397ab2): The site-title and header voice. Used at 20% opacity as the tonal background for article header panels, and as the contrast border accent framing the masthead.
- **Sky Tint** (#d7ecf8): The masthead background. A pale, calm wash that establishes the arc42 identity at the top of every page without competing with the content below.

### Tertiary
- **Help Blue** (#dcf0ff background / #002080 ink): The `.arc42-help` guidance callout. Cool, quiet, clearly "the template's advice."
- **Example Pink** (#fde2e5 background / #002080 ink): The `.arc42-example` block. Warm counterpoint to the help blue, so a reader instantly distinguishes "guidance" from "worked example."
- **Coral** (#fe5a83): The masthead description accent, a single warm spark against the sky tint. Used sparingly, never on body content.
- **Tag Cyan** (#aee3f8): Tag and label pills.
- **Emerald** (#50c878): The footer status indicator only. Signals "operational" and nothing else.
- **Maroon** (#800000): The subtle-ad border and accent. Quarantined to sponsor/ad blocks; never used in editorial content.

### Neutral
- **Ink** (#383838): Body text. A soft near-black, easier on the eyes than pure black across long reading sessions.
- **Paper** (#ffffff): The page. White is the default surface; the content sits directly on it.
- **Muted** (#777777): Blockquote text and de-emphasized meta.
- **Hairline** (rgba(0,0,0,0.1)): Table borders, aside nav dividers, input strokes.

### Named Rules
**The Functional Color Rule.** Color earns its place by carrying meaning, never by decorating. Blue means structure or action; pink means example; green means status; maroon means sponsor. If a color is not doing one of those jobs, it does not belong on the page.

**The One Blue Rule.** There is a single editorial blue (#1675b9). Steel and sky are its lighter framing relatives for the masthead. Do not introduce a second competing accent blue into content.

## 3. Typography

**Display Font:** Helvetica, Arial (with sans-serif fallback)
**Body Font:** Helvetica, Arial (with sans-serif fallback)
**Label/Mono Font:** Consolas, Monaco, Andale Mono (monospace)

**Character:** One honest workhorse sans for everything, monospace for code. Nothing decorative, nothing to learn. The type gets out of the way so the words carry the weight, which is exactly what a field guide wants.

### Hierarchy
- **Display** (bold, 2.7em, line-height 1): The masthead title only. Appears once per page, in Steel Blue on the Sky Tint header.
- **Headline** (bold, 2.3em, line-height 1.3): Page `h1`. The section's name.
- **Title** (bold, 1.8em, line-height 1.3, Signal Blue): Major `h2` subheads. Blue on purpose, so the reader can scan the structural skeleton of a long page by color alone.
- **Body** (regular, 16px, line-height 1.5): All prose. Comfortable leading for extended reading. Target 65 to 75 characters per line.
- **Label** (regular, 0.95em, line-height 1.2): Aside navigation, meta lines, tags, footnotes.
- **Code** (regular, 0.85em monospace): Inline code and code blocks.

### Named Rules
**The Blue-Subhead Rule.** `h2` section headings are Signal Blue while `h1` stays ink. This lets a reader scan a long section page and perceive its structure at a glance. It is a navigation aid, not decoration, so do not extend the blue to `h1` or body text.

**The Comfortable Measure Rule.** Body copy targets 65 to 75 characters per line. On wide desktop the content column must not let prose run the full width; long unbroken measures are the enemy of a reference read at length.

## 4. Elevation

Mostly flat. The page is white, the content sits directly on it, and structure is conveyed through spacing, hairline rules, and tonal background tints rather than through stacked shadows. There is one deliberate exception: annotation-style callouts.

### Shadow Vocabulary
- **Callout Lift** (`box-shadow: 3px 3px 4px 0 rgba(11,82,185,1)`): The signature offset shadow under `.arc42-help` blocks. A hard, colored, directional drop shadow that makes the callout read like a sticky note pinned onto the page. This is arc42's tactile signature, not a generic Material elevation.
- **Sponsor Lift** (`box-shadow: 3px 3px 4px 0 rgba(156,61,75,1)`): The same offset treatment in maroon, reserved for `.subtle-ad` sponsor blocks so they read as "attached" rather than part of the editorial flow.

### Named Rules
**The Flat-Page, Lifted-Note Rule.** The document itself is flat. The signature offset shadow is reserved exclusively for callout and sponsor blocks, the things that are annotations *on* the page rather than part of it. Never put this shadow on a heading, a table, or an ordinary content container.

## 5. Components

### Buttons
- **Shape:** Gently rounded (0.3em radius), 1px solid border.
- **Default:** Transparent fill, Signal Blue text and border, padding 0.5em 0.75em. Reads as a quiet outlined control.
- **Hover:** Fills with Signal Blue, text flips to Paper white, underline removed. A clear, confident state flip with no ornament.

### Callouts (signature component)
The heart of the system. Two annotation blocks that structure every documentation section.
- **Help block** (`.arc42-help`): Help Blue background (#dcf0ff), deep-blue ink (#002080), 4px radius, Callout Lift shadow, roomy 16px/48px/16px/20px padding, 1.5 line-height, and a `help42.svg` icon pinned top-right (absolutely positioned, not floated, so it never crowds the first line of text). Carries the template's guidance.
- **Example block** (`.arc42-example`): Example Pink background (#fde2e5), same deep-blue ink, 4px radius, same roomy padding and top-right info icon. No shadow, so it reads as lighter than a help block. Carries worked examples.
- **Rule:** Help is blue, example is pink, always. The color pairing is how the reader tells guidance from illustration at a glance.

### Code
- **Inline** (`code`): Near-white background (#fafafa), 1px #ddd border, 3px radius, small horizontal padding. A subtle chip, not a loud highlight.
- **Block** (`pre`): 1px #ccc border, faint gray background, 3px radius, horizontal scroll on overflow. Rouge syntax highlighting.

### Tags
- **Style:** Tag Cyan (#aee3f8) pill, Signal Blue text, 4px radius, 4px 6px padding. Small, secondary, used for post taxonomy.

### Navigation
- **Aside nav:** A vertical list of section links with hairline top/bottom borders per item, roomy 0.5em padding, label-scale type. Collapses behind a toggle below 800px. Quiet and list-like; the current structure of the twelve sections, not a chrome-heavy menu.
- **Masthead:** Sky Tint bar with a circular avatar, Steel Blue title, and a single Coral description line, framed top and bottom by a Steel Blue rule.

### Blockquotes
- **Style:** 5px gray left border (#ddd), Muted text, 0.5em 1em padding. This is a conventional quotation mark, not a colored accent stripe on a card.

## 6. Do's and Don'ts

### Do:
- **Do** keep the page flat and let 50px vertical rhythm and hairline rules do the structuring.
- **Do** use color functionally: Signal Blue for structure and action, Help Blue for guidance, Example Pink for examples, Emerald only for status, Maroon only for sponsor blocks.
- **Do** color `h2` subheads Signal Blue so a reader can scan a long section's skeleton at a glance.
- **Do** cap body measure at 65 to 75 characters; constrain the content column so prose never runs full desktop width.
- **Do** reserve the signature offset shadow for callout and sponsor blocks only, the things that are annotations on the page.
- **Do** distinguish help (blue) from example (pink) callouts by color, every time.

### Don't:
- **Don't** build a **salesy SaaS landing page**: no gradient heroes, no fabricated metrics, no conversion-funnel CTAs, no "sign up now" energy.
- **Don't** drift toward a **heavy enterprise documentation portal**: no dense, cluttered, bureaucratic chrome or deep nested megamenus.
- **Don't** chase **trendy or flashy** looks: no neon, no glassmorphism, no dark-mode-for-cool, no gratuitous animation.
- **Don't** settle for a **sterile generic template**: no anonymous default-framework look with no arc42 identity.
- **Don't** introduce a second competing accent color into editorial content; there is one editorial blue.
- **Don't** put the offset callout shadow on headings, tables, or ordinary content containers.
- **Don't** use `border-left` greater than 1px as a colored accent stripe on cards, list items, or alerts. The gray blockquote rule is the only permitted left border, and it stays gray.
- **Don't** use gradient text or `background-clip: text`. Emphasis comes from weight, size, and the one blue.
