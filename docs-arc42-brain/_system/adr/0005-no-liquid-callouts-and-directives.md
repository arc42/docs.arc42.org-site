# ADR-0005: No Liquid in the brain; callouts and directives instead

- **Status:** accepted
- **Date:** 2026-09-17

## Context
Section pages today mix markdown with Jekyll includes and `<div class="arc42-help">` blocks. Obsidian renders neither.

## Decision
`wiki/` contains no Liquid. Guidance is an Obsidian callout `> [!arc42-help]`. The example list is the directive `%% examples: <category> %%`; the pointer to examples.arc42.org is `%% examples-link %%`; both are Obsidian comments. The page foot (`further-info.md`) is generated from the section's `category` and `faq-topic`. Images use vault-relative paths; the generator rewrites them. A case that truly needs Liquid gets an issue and, if it recurs, a new directive by ADR.

## Consequences
Pages render in Obsidian. The importer and the generator are inverses of each other, which is what the parity check relies on.
