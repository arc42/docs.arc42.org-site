# Workflow: Audit

On request or after a batch of ingests. Read-only except for issues and the log.

Check and raise an issue for each finding:
- pages in `review` for longer than 30 days;
- terms without a definition sentence, or without `home`;
- keywords referenced by fewer than 2 pages;
- tips with an empty `related`;
- `legacy-tags` still present anywhere;
- headings inside guidance that differ from the house pattern
  (`Content` / `Motivation` / `Form`) — record, do not fix, until the section is
  cut over and parity no longer applies;
- external links that no longer resolve (check with `curl -sI`).

Append `## [YYYY-MM-DD] audit | <scope>` to `_system/log.md`.
