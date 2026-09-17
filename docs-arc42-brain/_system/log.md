# Log

Append-only. One entry per operation, prefix exact so it stays greppable:
`grep '^## \[' _system/log.md | tail -5`.

<!-- Format:
## [YYYY-MM-DD] <bootstrap|ingest|audit|report> | <subject>
- created: …
- updated: …
- issues: …
-->

## [2026-09-17] bootstrap | twelve section pages, keywords, systems
- created: section-1 … section-12 (draft, from raw/ingested/section-N-page), SRC-001 … SRC-012
- created: keywords lean, essential, thorough, example, tooling; systems htmlsc, tpu, mama (+ status or ISS-001)
- notes: section 10 image path normalised from a hard-coded /assets/images path; all other bodies verbatim
