# Log

Append-only. One entry per operation, prefix exact so it stays greppable:
`grep '^## \[' _system/log.md | tail -5`.

<!-- Format:
## [YYYY-MM-DD] <bootstrap|ingest|audit|report> | <subject>
- created: …
- updated: …
- issues: …
-->
