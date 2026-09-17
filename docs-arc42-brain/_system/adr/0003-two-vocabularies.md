# ADR-0003: Terms and keywords are separate vocabularies

- **Status:** accepted
- **Date:** 2026-09-17

## Context
The site's flat tag list mixes reading facets (`lean`, `essential`, `thorough`) with arc42 concepts (`building-block`, `quality-scenario`) and contains near-duplicates.

## Decision
`wiki/terms/` holds arc42 concepts with a definition, aliases, `legacy-tags` and a home section. `wiki/keywords/` holds a small controlled list of navigation facets. Tips, examples and FAQ answers reference both. The importer parks old tags in `legacy-tags`; a page may not leave `draft` until that list is empty. Consolidating tags may change tag names on the site's keyword page; page URLs never change.

## Consequences
The keyword page is generated from the union. Tag cleanup is an explicit, reviewable act per page.
