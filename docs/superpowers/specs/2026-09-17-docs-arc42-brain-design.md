# docs-arc42-brain — design

Status: phase 1 implemented · 2026-09-17 · branch docs-arc42-brain

## 1. Purpose

docs.arc42.org is a hand-written Jekyll site: twelve section pages, 145 tips, 36
examples, a tag-driven keyword index. It is highly frequented and its URLs are
cited externally. faq.arc42.org holds 136 answers with low traffic.

This design introduces a **second brain** for that content: a Karpathy-style
LLM wiki (`raw/` → `wiki/` → schema) that becomes the single source of truth for
every content page of docs.arc42.org. A deterministic generator turns the wiki
into ordinary Jekyll input. The existing Jekyll layouts, includes, styling and
navigation stay hand-maintained. The FAQ content is merged into the same brain
later and published on docs.arc42.org.

The point of the brain is not storage. It is that content becomes typed and
interlinked, so that "see also" links between tips, examples, sections, terms
and FAQ answers are derived from an explicit vocabulary instead of from memory.

## 2. Decisions already taken (conversation, 2026-09-17)

| # | Decision | Consequence |
|---|---|---|
| D1 | The brain owns **all** content pages: sections (guidance included), tips, examples, later FAQ. `make generate` produces every content file. | No content is hand-edited in `_pages/section-*`, `_posts/`, `_examples/` once a section is cut over. |
| D2 | Layouts, includes, SCSS, `_data/sections.yml`, nav stay hand-maintained in Jekyll. | Generator emits markdown + frontmatter only; it never writes to `_layouts/`, `_includes/`, `_sass/`. The one hand-made addition is `_includes/related.html` plus the line that calls it in the article layout (§4.5). |
| D3 | docs.arc42.org URLs are stable. Tip `/tips/N-M/`, example and section permalinks are emitted byte-identical. | Permalinks live in the brain as data and are covered by the parity check. |
| D4 | faq.arc42.org URLs may be dropped. | FAQ answers get new URLs under docs.arc42.org; no redirects required. |
| D5 | Links: explicit `related:` lists are rendered on the site; computed candidates (shared keywords/terms) are shown only in the dashboard and promoted by human or agent. | Site output is deterministic; discovery is a dashboard job. |
| D6 | Link targets include sections **and subsections**. | Subsections need stable anchors; see §4.3. |
| D7 | Two vocabularies: **terms** (arc42 concepts with definition, aliases, home section) and **keywords** (a small controlled set of navigation facets). | Legacy tags map to one or the other during ingest; the keyword page keeps working from the union. |
| D8 | Issues are pages (`wiki/issues/`), not an external tracker. | Same pattern as etsu and meta.arc42.org. |
| D9 | ~~Dashboard is a generated static site for personal use~~ **Revised 2026-09-18 by D16** in `2026-09-18-docs-arc42-brain-dashboard-design.md`: a Flask server in Docker with presence and a lint-and-generate action. | See the dashboard spec. |
| D10 | Cut-over is per section; hand-written originals are deleted in the same commit that lands the generated files for that section. | Twelve reviewable PRs; the parity check gates each one. |
| D11 | Generator and lint are Python (uv-managed) in `docs-arc42-brain/_system/`, driven from the root Makefile. | Frontmatter/wikilink/graph code can be lifted from etsu and meta tooling. |
| D12 | Bootstrap ingest is audit-style (type, link, flag). Grilling is reserved for new content and the FAQ merge. | 200 existing pages do not get stress-tested one by one. |
| D13 | Natural IDs stay: tip `9-1`, example `09-decision-example-adr`, section `9`, FAQ `A-13`. | IDs never change; filenames derive from IDs. |
| D14 | The brain lives in `docs-arc42-brain/` inside this repo, excluded from the Jekyll build, and is the Obsidian vault root. | One repo, one PR flow. `.obsidian/` is gitignored entirely; sharing vault settings is a later decision. |
| D15 | English throughout. | — |

## 3. Layout

```
docs-arc42-brain/                 Obsidian vault root
  CLAUDE.md                       agent schema: types, conventions, workflows
  README.md                       human intro
  raw/                            human-owned inbox (top level = not yet ingested)
    ingested/                     archived originals, unchanged
    sources/                      SRC-NNN provenance records (agent-written)
  wiki/                           agent-owned content
    sections/                     section-1.md … section-12.md
    tips/                         tip-9-1.md …
    examples/                     09-decision-example-adr.md …
    faq/                          faq-a-13.md … (phase 4)
    terms/                        building-block.md …
    keywords/                     lean.md, essential.md, thorough.md …
    systems/                      htmlsc.md, tpu.md, mama.md … (the example systems)
    issues/                       ISS-001-….md
    assets/                       images, owned by the brain; copied by the generator
      sections/NN/…
      examples/…
  _templates/                     one file per type, frontmatter contract
  _system/
    index.md                      catalog, one line per page, grouped by type
    log.md                        append-only run log
    adr/                          decisions about the brain itself
    workflows/                    bootstrap.md, ingest.md, audit.md, relations.md, cutover.md
    generate/                     Python package: parse → model → emit (Jekyll, dashboard)
    dashboard/                    Jinja templates + static assets for the dashboard
    brain.mk                      make targets, included from the root Makefile
  build/                          gitignored: dashboard output, parity scratch
```

Root repo changes: `_config.yml` excludes `docs-arc42-brain` and `docs`;
`Makefile` gains `include docs-arc42-brain/_system/brain.mk`; `.gitignore`
gains `docs-arc42-brain/build/` and `docs-arc42-brain/.obsidian/`.

## 4. Metamodel

### 4.1 Common frontmatter

Every wiki page:

```yaml
id:        string, unique across the wiki, equals the natural ID (D13)
type:      section | tip | example | faq | term | keyword | system | issue
title:     human title
status:    draft | review | published | retired
created:   YYYY-MM-DD
updated:   YYYY-MM-DD
sources:   [ "[[SRC-001-…]]", … ]     provenance; at least one for ingested content
related:   [ "[[…]]", … ]             explicit links, rendered on the site (D5)
```

`status: published` is the only status the generator emits. `draft` and
`review` pages are visible in Obsidian and the dashboard but produce no Jekyll
output. `retired` keeps the page for history and produces nothing.

`related:` entries are Obsidian wikilinks to any page, optionally with a heading
(`[[section-5#5.1 Whitebox Overall System]]`) or a label
(`[[tip-9-1|Document only relevant decisions]]`). Order is meaningful; the
generator keeps it.

### 4.2 Types

| Type | Folder | ID / filename | Type-specific fields | Generates |
|---|---|---|---|---|
| **section** | `wiki/sections/` | `section-N` | `number`, `name` (short nav name), `category` (the legacy `category:` slug, e.g. `decisions`), `posts-dir` (the legacy `_posts/` folder, e.g. `09-decisions`), `permalink`, `order`, `faq-topic` (the human phrase used in "questions related to …") | `_pages/section-N.md` |
| **tip** | `wiki/tips/` | `N-M` → `tip-N-M.md` | `section: "[[section-N]]"`, `subsection` (optional heading anchor), `keywords: []`, `terms: []`, `date` (legacy post date, keeps list order), `permalink` | `_posts/NN-<slug>/YYYY-MM-DD-t-N-M.md` |
| **example** | `wiki/examples/` | legacy filename stem | `section`, `subsection`, `system: "[[htmlsc]]"`, `example-category` (legacy `category:` slug, e.g. `qualitygoals`), `keywords`, `terms`, `permalink` | `_examples/<id>.md` |
| **faq** | `wiki/faq/` | `A-13` → `faq-a-13.md` | `question` (= title), `section` (optional), `keywords`, `terms`, `legacy-permalink`, `legacy-category` | `_faq/<id>.md` (new collection, phase 4) |
| **term** | `wiki/terms/` | slug | `term` (display form), `aliases: []`, `legacy-tags: []` (old tag spellings that map here), `home: "[[section-N]]"` | rows of a generated glossary page; contributes to `tags:` of every page that references it |
| **keyword** | `wiki/keywords/` | slug | `description`, `featured: bool` (`lean`/`essential`/`thorough` are featured today) | contributes to `tags:`; listed on the keyword page |
| **system** | `wiki/systems/` | slug (`htmlsc`, `tpu`, `mama`, `hsc`, `status`) | `name`, `url` (on examples.arc42.org if it exists there) | nothing directly; groups examples in related links and dashboard |
| **issue** | `wiki/issues/` | `ISS-NNN` | `severity`, `kind: question \| contradiction \| gap \| ambiguity \| risk`, `raised-by`, `resolved` | nothing |
| **source** | `raw/sources/` | `SRC-NNN` | `origin` (path under `raw/ingested/` or repo path), `sha256`, `ingested-pages: []` | nothing |

Section 10 is the one place where a tip category (`quality`) and an example
category (`quality`, `qualitygoals`) collide by name; the `example-category`
field on examples exists so the generator never has to guess.

### 4.3 Sections and subsections

A section page in the brain is one markdown file. Its body is the ordered
sequence of what the site renders today:

- `## 5.1 Whitebox Overall System` — a real subsection heading. The generator
  emits it unchanged. Its anchor is the heading id the site produces
  (`51-whitebox-overall-system`), computed by the generator with the rules of
  kramdown's **GFM** parser — the site runs kramdown with `input: GFM` — which
  are GitHub's, not kramdown's own: take the rendered heading text, downcase,
  delete every character that is not a word character, hyphen or space, then
  turn each space into one hyphen, so the leading number survives. This is what
  `[[section-5#5.1 Whitebox Overall System]]` resolves to on the site:
  `/section-5/#51-whitebox-overall-system`.
- Guidance is an Obsidian callout: `> [!arc42-help]` followed by the markdown
  that today sits inside `<div class="arc42-help" markdown="1">`. Obsidian
  renders it as a callout; the generator emits the div. Inner headings
  (`### Content`, `### Motivation`, `### Form`) stay markdown inside the callout.
- Example lists are a directive line inside the callout:
  `%% examples: decisions %%` (an Obsidian comment, invisible in preview). The
  generator replaces it with `{% include example.md category="decisions" %}`.
  The category string is the `example-category` of the examples that belong
  here, so the lint checks that every example's `example-category` is
  referenced by exactly one directive.
- Template placeholders (`### _<insert overview diagram>_`) are ordinary
  markdown and pass through.
- The one-sentence pointer to examples.arc42.org
  (`{% include examples-link.html variant="inline" %}`) sits in the body at a
  position that varies per section (after the first callout in most sections,
  after subsection 1.1 in section 1, after 3.1 in section 3). It is a second
  directive, `%% examples-link %%`, placed where the include is today.
- Callouts are position-based, not heading-based. Section 5 has two callouts
  under one heading and callouts under H3 headings; section 10 has H2
  guidance headings inside a subsection. All of that passes through unchanged.
- Raw HTML that exists today inside guidance (`<a target="_blank" …>`,
  `<br>`, markdown tables, HTML comments) passes through. Ingest may clean
  obvious leftovers (a stray `****` in section 7, a doubled comment in
  section 8) and must raise an issue when it does, because that breaks parity
  on purpose.
- The page's foot (`further-info.md`) is **not** in the brain. The generator
  appends it from the section's `category` and `faq-topic` fields. Once FAQ
  moves in (phase 4) the `faqlink` argument becomes a docs-internal URL and
  the include is edited by hand, once.

Rendered sections therefore consist of brain content plus a fixed, generated
foot. Nothing in the brain contains Liquid.

Anchors: only numbered subsection headings (`5.1 …`, `10.2 …`) and named
guidance headings that are unique on their page (`Background (on ADRs)`) are
valid link targets. Headings that repeat on a page (`Content`, `Motivation`,
`Form`) get kramdown suffixes (`content-1`) and are not addressable; the lint
rejects a `[[section-N#heading]]` whose heading is not unique on that page.
Placeholder headings (`6.1 _<Runtime Scenario 1>_`) are not link targets.

Headings the includes inject count as headings of the page even though no line
of the brain contains them: `example.md` emits `### Examples` at every
`%% examples: … %%` position, and the foot emits `## Practical Tips`,
`### Related Questions` and `### Complete Examples`. The parser carries them as
synthetic headings on section pages, so anchors are numbered as the site
numbers them (section 10's own `## Examples` really is `examples-1`) and
`[[section-N#Practical Tips]]` resolves. The generator must not write them into
the body — the includes already do.

### 4.4 Liquid and images policy

- **No Liquid in the brain.** The generator introduces every `{% … %}` and
  `{{ … }}`.
- Images are referenced with vault-relative paths so Obsidian renders them:
  `![alt](../assets/sections/09/adr-flow.png)`. The generator rewrites
  `assets/sections/…` to `{{ site.imageurl }}/…` and `assets/examples/…` to
  `{{ site.exampleimages }}/…`, and copies the files to
  `assets/images/sections/` and `assets/images/examples/` in the site.
- External links are plain markdown links. The site today writes them as
  `<a target="_blank" rel="noopener noreferrer nofollow">`; the generator
  rewrites every absolute `http(s)://` markdown link to that form so the
  bootstrap parity holds and future content does not have to remember the
  attributes. Existing raw `<a>` tags in bodies pass through.
- Anything that genuinely needs Liquid gets an issue and, if it recurs, an ADR
  that adds a directive. None is expected from the inventory (the only Liquid
  in 145 tips is `site.imageurl`; in 36 examples, `site.exampleimages`).

### 4.5 Links and tags on the generated site

For each generated tip, example (and later FAQ) the generator emits:

```yaml
tags: <keywords + the display tag of every term, in the page's declared order>
related:            # structured, rendered by a new hand-maintained include
  - kind: tip        # section | subsection | tip | example | faq | term
    title: …
    url: /tips/9-2/
```

A new `_includes/related.html` (hand-maintained, D2) renders `page.related`
grouped by kind at the foot of the article. Body markdown stays free of
generated link lists, which keeps the parity check meaningful.

A term's display tag is the term slug; `legacy-tags` are **not** emitted.
Consolidating `scenario` into `quality-scenario` therefore changes the tag on
the affected tips and the anchor on `/keywords/`. This is accepted (D3 covers
page URLs, not keyword-page anchors); the lint reports every tag that
disappears from the site so the reviewer sees it in the PR.

## 5. Workflows (`_system/workflows/`)

**bootstrap.md** — once. Creates the twelve section pages from the current
`_pages/section-*.md`, the keyword pages for the featured tags, the system
pages, `_system/index.md`, `log.md`, ADR-0001. Not grill-gated (D12). Output:
a brain that lints clean and generates nothing yet (all `status: draft`).

**ingest.md** — per section, per session. Steps:

1. `make brain-raw SECTION=9` copies the section's tips, examples and section
   page into `raw/` (or the human copies files by hand). Create `SRC-NNN` with
   sha256 per file.
2. For the section page: convert help divs to callouts, includes to
   directives, images to vault paths. Set `status: review`.
3. For each tip and example: create the typed page. Map every legacy tag to a
   keyword or a term; create term/keyword pages as needed; unknown or
   ambiguous tags raise an `ISS`. Set `section`, `subsection`, `system`.
4. Run `make brain-suggest SECTION=9` and promote good candidates into
   `related:` on both ends. Add links to sections/subsections where the tip
   text clearly refers to one.
5. Raise issues for contradictions, outdated statements, dead external links,
   near-duplicate tips.
6. Update `_system/index.md`, append to `_system/log.md`, move raw files to
   `raw/ingested/`.
7. `make brain-lint` and `make generate-check SECTION=9` must pass.

**cutover.md** — per section, after ingest. Flip the section's pages to
`status: published`, run `make generate`, delete the hand-written originals,
run `make check` and `make check-links`, open the PR. The PR diff shows exactly:
brain pages added, originals deleted, generated files added, and the
`related:` frontmatter as the only body-external change.

**audit.md** — on request. Orphan pages, broken wikilinks, terms without
definition, tags never mapped, pages without `sources`, issues open longer
than N days, sections with zero related links.

**relations.md** — the promotion rule of D5 in writing: how candidates are
computed (shared terms weigh more than shared keywords; same subsection;
same system), and that the site renders only `related:`.

## 6. Generator (`_system/generate/`)

Python 3.12+, `uv`-managed, dependencies: `python-frontmatter`, `PyYAML`,
`Jinja2`, `markdown-it-py` (for link/image rewriting on the token stream, not
by regex), `pytest`.

Pipeline: **parse** (every `wiki/**/*.md` → typed dataclass, wikilinks resolved
to IDs) → **validate** (the lint, §8) → **emit**.

Emitters, each a Jinja template plus a small mapping function:

| Emitter | Reads | Writes |
|---|---|---|
| `sections` | `wiki/sections/*` with `status: published` | `_pages/section-N.md` |
| `tips` | tips with published status | `_posts/<NN-dir>/<date>-t-N-M.md`; the directory name is taken from the section's legacy folder (`09-decisions`), recorded once in the section page as `posts-dir` |
| `examples` | published examples | `_examples/<id>.md` |
| `faq` | published FAQ answers | `_faq/<id>.md` (phase 4) |
| `glossary` | terms | `_pages/glossary.md` (a new page; phase 3 or later, not part of parity) |
| `assets` | `wiki/assets/**` | `assets/images/sections/`, `assets/images/examples/` |
| `dashboard` | everything, including drafts and issues | `build/dashboard/` (§7) |

Every generated file starts with a comment line
`<!-- generated from docs-arc42-brain/wiki/tips/tip-9-1.md — do not edit -->`
placed after the frontmatter, so Jekyll ignores it and a reader sees it.

`make generate` is idempotent and complete: it deletes generated files whose
brain page no longer exists or is no longer published, and it never touches
files it did not generate (it knows its own by the marker comment).

**Parity check** (`make generate-check SECTION=N`): generate into
`build/parity/`, then compare with the current tree for that section. Pass
condition: body identical after normalising trailing whitespace; every
frontmatter key that exists in the original has an identical value; new keys
(`related`) are allowed; `tags` are compared as sets after alias
normalisation and every difference is printed, not failed. The check runs on
sections that are ingested but not yet published, which is the only time both
versions exist.

## 7. Dashboard (`_system/dashboard/`)

> Superseded on 2026-09-18 by `2026-09-18-docs-arc42-brain-dashboard-design.md`
> (D16–D23). The page list below is kept for history; the dashboard is a
> Flask server in Docker, not a static export.

Static HTML, emitted by the generator into `build/dashboard/`, opened with
`make dashboard`. Reads the parsed model, so drafts and issues appear. Pages:

- **Home**: coverage per section (tips, examples, terms, issues; ingested vs
  published), last log entries, lint summary.
- **Issues**: open issues by severity and kind, each with its `related:` pages.
- **Terms**: the vocabulary with definitions, aliases, legacy tags, home
  section, usage counts; a force graph of term co-occurrence (lifted from
  etsu's cytoscape setup).
- **Keywords**: the controlled list with counts.
- **Suggestions**: computed link candidates not yet in `related:`, grouped by
  page, with a one-line reason ("shares terms quality-scenario, stimulus").
  This is the promotion queue of D5.
- **Graph**: full link graph, filter by type.
- **Page detail**: rendered page with its links in and out, sources, issues.

Visual identity: the arc42 family tokens from this site's `DESIGN.md`. No
server, no self-shutdown logic, no QR code; those were workshop features.

## 8. Lint (`make brain-lint`)

Fails the build on: unknown type; missing required field for the type;
duplicate ID; wikilink that does not resolve; `related:` entry that is not
reciprocated (warning, not failure, until relations.md decides); example whose
`example-category` is not referenced by a section directive; tip whose
`section` does not match its legacy `category`; published page without
`sources`; image path that does not exist under `wiki/assets/`; Liquid syntax
anywhere in `wiki/`.

## 9. Make targets (`_system/brain.mk`, included from the root Makefile)

| Target | Does |
|---|---|
| `brain-raw SECTION=N` | copy that section's current site files into `raw/` |
| `brain-lint` | schema and link validation |
| `brain-suggest [SECTION=N]` | print link candidates (the dashboard's Suggestions page as text) |
| `generate` | brain → Jekyll input + assets |
| `generate-check SECTION=N` | parity check, §6 |
| `dashboard` | generate the dashboard and open it |
| `brain-test` | pytest for the generator |

`make check` (existing) is extended to run `brain-lint` and to fail if any
generated file has been hand-edited (marker present but content differs from
a fresh generate).

## 10. Testing

- Unit tests for the parser (frontmatter, wikilinks with headings and labels,
  callout and directive extraction), the kramdown anchor function, the link and
  image rewriters, and each emitter's mapping, with fixture pages under
  `_system/generate/tests/fixtures/`.
- The parity check as an integration test on section 9, kept as a fixture
  after cut-over so the emitters cannot regress silently.
- `make check` and `make check-links` after every generate.

## 11. Phasing

Each phase gets its own implementation plan.

1. **Foundation**: layout, CLAUDE.md, templates, workflows, ADR-0001,
   bootstrap, Makefile wiring, lint. Pilot ingest of section 9 (10 tips,
   3 examples). Exit: `make brain-lint` passes on the pilot.
2. **Generator**: emitters for sections, tips, examples, assets; parity check
   green on section 9; cut-over of section 9 merged to `main`. Exit: the live
   site is unchanged except for the new related-links block on section 9 pages
   and any tag consolidation the lint reported in the PR.
3. **Dashboard**: static dashboard with the seven pages; ingest and cut over
   the remaining eleven sections, one PR each. Exit: no hand-written content
   left in `_pages/section-*`, `_posts/`, `_examples/`.
4. **FAQ merge**: `faq` type, grill-gated ingest of the 136 answers from
   `../faq.arc42.org-site`, a new `_faq` collection (one `collections:`
   entry in `_config.yml`) with hand-made category pages on docs.arc42.org,
   the glossary page, retire faq.arc42.org.

## 12. Non-goals

- No change to layouts, navigation, styling, search, or `_data/sections.yml`
  beyond the `related.html` include, its call in the article layout, and the
  `docs`/`docs-arc42-brain` excludes in `_config.yml`.
- No Jekyll plugin, no build-time reading of the brain; the site builds from
  committed generated files exactly as today.
- No open-source packaging of the dashboard.
- No redirects for faq.arc42.org URLs.
- No translation, no multi-language content.

## 13. Open points to raise as issues at bootstrap

- Whether `related:` must be reciprocal (etsu says yes for same-concept pages;
  here a tip→section link rarely wants a section→tip backlink).
- Whether to normalise Content/Contents, heading levels and the section 7
  placeholder names after cut-over (Appendix A lists them); each is a
  deliberate parity break and gets its own small PR.
- Whether the six "glossary" tips (section 12) should become the seed of the
  terms vocabulary or stay tips.
- The `date` field on tips is a legacy ordering artefact; decide whether
  `order` on the tip replaces it after cut-over.

## Appendix A. Inventory of the current section pages

Survey of `_pages/section-1.md` … `section-12.md`, 2026-09-17. Front matter
is identical in shape on all twelve: `layout`, `title`, `permalink`,
`number`, `order`. Every page ends with `further-info.md`; every page has one
`examples-link.html variant="inline"` in its body (section 3 has one for two
subsections).

| Sec | Numbered subsections | Help divs | example.md categories | further-info category | Irregular |
|---|---|---|---|---|---|
| 1 | 1.1, 1.2, 1.3 (H2) | 4 | overview, qualitygoals | requirements | "Contents" plural in 1.1; top div has no Content/Motivation/Form; 1.3 has no example include; stakeholder table outside the div |
| 2 | none | 1 | constraints | constraints | Content/Motivation/Form at H2 |
| 3 | 3.1, 3.2 (H2) | 3 | business-context, technical-context | context | extra "## Examples" in top div; "Contents" plural in 3.2; one examples-link for two subsections |
| 4 | none | 1 | solutionstrategy | solution-strategy | "Contents" plural; example category has no hyphen while post category has one |
| 5 | 5.1–5.3 (H2), 5.2.x, 5.3.x (H3) | 8 | building-block | building-block | two divs under 5.1; divs under H3 headings; placeholder italics inconsistent |
| 6 | 6.1, 6.2, 6.n (H3) | 1 | runtime | runtime | subsections at H3; literal `### ...` placeholder |
| 7 | 7.1, 7.2 (H3), 7.2.x (H4) | 3 | deployment | deployment | lowercase "view"; H4 sub-subheadings; duplicated placeholder name; stray `****` |
| 8 | none | 1 | concepts | concepts | "Structure of this section" and "Background" inside one div; doubled HTML comment |
| 9 | none | 1 | decisions | decisions | "Background (on ADRs)"; real H3 "Our proposal concerning decisions" inside the div |
| 10 | 10.1, 10.2 (H2) | 3 | quality | quality | "Further Information" instead of "Form"; nested guidance headings at H2; no Motivation in 10.2; "See also" outside any div; hard-coded image path; raw `<a>` |
| 11 | none | 1 | risks | risks | no blank line after front matter; raw `<a>` in blockquote |
| 12 | none | 1 | glossary | glossary | illustrative table inside the div |

Fourteen example categories exist: overview, qualitygoals, constraints,
business-context, technical-context, solutionstrategy, building-block,
runtime, deployment, concepts, decisions, quality, risks, glossary. Four
images are referenced from section pages (sections 1, 5, 8, 10); the one in
section 10 uses a hard-coded `/assets/images/sections/10/…` path instead of
`{{ site.imageurl }}`, which ingest normalises and the parity check will
report as the expected single-line difference.

Consequences for the design, already folded into §4.3: the examples-link
directive; position-based callouts; pass-through of raw HTML; uniqueness rule
for anchors. The Content/Contents and H2/H3 inconsistencies are kept verbatim
for parity and become audit issues after cut-over, which is the first
concrete payoff of having the content typed.
