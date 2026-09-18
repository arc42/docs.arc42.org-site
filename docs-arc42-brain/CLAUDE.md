# docs-arc42-brain — agent schema

You maintain the **second brain of docs.arc42.org**: every content page of the
site (sections with their guidance, tips, examples, later FAQ answers) lives
here as a typed, interlinked wiki page. A generator (`_system/generate/`,
phase 2) turns `wiki/` into the Jekyll input of the site one directory up.
Layouts, includes, styling and navigation stay in Jekyll; the brain owns
content only.

Design spec: `../docs/superpowers/specs/2026-09-17-docs-arc42-brain-design.md`.

## Three layers (Karpathy LLM-wiki pattern)

1. **`raw/`** — human-owned, immutable. Top level is the inbox of not-yet-ingested
   batches (`raw/section-9-all/`, written by `make brain-raw`). After ingest a
   batch moves to `raw/ingested/`. `raw/sources/` holds the `SRC-NNN` provenance
   records you write. Never edit a raw file.
2. **`wiki/`** — agent-owned content, one typed page per file, Obsidian wikilinks.
3. **Schema** — this file, `_templates/`, `_system/adr/`. Changing the schema
   needs an ADR.

## Content types

| Type | Folder | Slug (= filename stem) | Notes |
|---|---|---|---|
| section | `wiki/sections/` | `section-N` | one page per arc42 section, guidance as `> [!arc42-help]` callouts |
| tip | `wiki/tips/` | `tip-N-M` | `id: N-M`; `permalink` is a public URL and never changes |
| example | `wiki/examples/` | legacy filename stem | `example-category` is the legacy Jekyll category |
| faq | `wiki/faq/` | `faq-a-13` | phase 4 |
| term | `wiki/terms/` | kebab slug | arc42 vocabulary: definition, `aliases`, `legacy-tags`, `home` section |
| keyword | `wiki/keywords/` | kebab slug | small controlled navigation facets (`lean`, `essential`, `thorough`, …) |
| system | `wiki/systems/` | `htmlsc`, `tpu`, `mama`, `status` | the example systems |
| issue | `wiki/issues/` | `ISS-NNN-kebab` | open question, contradiction, gap, ambiguity, risk |
| source | `raw/sources/` | `SRC-NNN-<batch>` | provenance record |

Required fields per type are enforced by `make brain-lint`; the templates in
`_templates/` are the contract. Do not invent fields.

## Conventions

- **Language**: English.
- **Wikilinks**: `[[slug]]`, `[[slug#Heading text]]`, `[[slug|label]]`. In YAML
  always quoted: `related: ["[[tip-9-2]]"]`. Every cross-reference is a link;
  no bare prose references.
- **Links to subsections** use the heading text exactly as written on the
  target page: `[[section-5#5.1 Whitebox Overall System]]`. Only headings that
  are unique on their page are valid targets; `Content`, `Motivation`, `Form`
  are not.
- **Vocabulary**: a tip references `keywords:` (facets) and `terms:` (arc42
  concepts). Legacy site tags arrive in `legacy-tags:` from the importer and
  must be emptied by mapping each one to a keyword or a term before the page
  leaves `draft`. Create the term or keyword page if it does not exist; when a
  tag is ambiguous, raise an issue instead of guessing.
- **`related:`** is the only source of "see also" links on the site. Add links
  deliberately, at both ends where it makes sense. Links to sections need no
  backlink.
- **No Liquid** anywhere in `wiki/`. Images are vault-relative
  (`../assets/sections/09/x.png`). Directives are Obsidian comments:
  `%% examples: <category> %%`, `%% examples-link %%`.
- **Status**: `draft → review → published → retired`. Only `published` pages
  reach the site. Issues: `open → in-progress → resolved | wontfix`.
- **Provenance**: every page derived from a source links it in `sources:`.
- **Contradictions and doubts become issues**, never silent edits.
- **Dates** absolute, `YYYY-MM-DD`.

## Workflows (`_system/workflows/`)

| When | Read |
|---|---|
| empty vault | `bootstrap.md` |
| a batch appears in `raw/` | `ingest.md` |
| a section is fully ingested | `cutover.md` (phase 2) |
| on request | `audit.md`, `relations.md` |

Every run appends one entry to `_system/log.md` and updates `_system/index.md`.

## Commands

```
make brain-lint                      validate the vault (must pass before every commit)
make brain-raw SECTION=9 WHAT=all    copy site files into raw/section-9-all/
make brain-import BATCH=section-9-all  convert the batch into draft pages
make brain-test                      unit tests of the tooling
make generate-check SECTION=9        parity: generate into build/parity/ and compare with the site
make generate                        write the Jekyll files of every published page
make brain-check-generated           fail if a generated file was hand-edited (runs in make check)
make dashboard                       start the curator dashboard in Docker (http://localhost:4211)
make dashboard-down                  stop the dashboard
```

Generated files (`_pages/section-N.md`, `_posts/…`, `_examples/…` whose front
matter ends with the YAML comment `# generated from docs-arc42-brain/… — do not edit`)
are never edited by hand: edit the brain page and run `make generate`. The marker
sits inside the front matter on purpose: as a body line it would become the Jekyll
excerpt and blank the page's meta description.
