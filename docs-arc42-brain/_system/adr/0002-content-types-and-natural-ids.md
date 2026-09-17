# ADR-0002: Nine content types with natural IDs

- **Status:** accepted
- **Date:** 2026-09-17

## Context
docs.arc42.org URLs are cited externally and must not change. The site already has natural identifiers: tip `9-1`, example filename stems, section numbers, FAQ `A-13`.

## Decision
Types: section, tip, example, faq, term, keyword, system, issue, source. IDs are the natural ones; filenames derive from them (`tip-9-1.md`, `section-9.md`, `<example-stem>.md`, `faq-a-13.md`). Wikilinks resolve by filename stem, which is unique across the vault. `permalink` is stored on every page that has a public URL and is never derived.

## Consequences
No ID registry is needed. Renaming a page is forbidden; retiring it is `status: retired`.
