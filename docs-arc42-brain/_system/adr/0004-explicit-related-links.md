# ADR-0004: The site renders only explicit related links

- **Status:** accepted
- **Date:** 2026-09-17

## Context
Links between tips, examples, sections and terms are the main value of the brain. Computed similarity is cheap but noisy and makes the site change when a tag changes.

## Decision
`related:` on a page is the only source of "see also" links on the generated site. Link targets may be any page, and sections may be addressed by heading (`[[section-5#5.1 Whitebox Overall System]]`); only headings unique on their page are valid targets. The generator computes candidate links from shared terms and keywords and shows them in the dashboard only; a human or an ingest session promotes them. Links to sections need no backlink; other unreciprocated links are lint warnings.

## Consequences
The site is deterministic and reviewable in git. Discovery is a dashboard job.
