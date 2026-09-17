# ADR-0001: Record decisions about the brain as ADRs

- **Status:** accepted
- **Date:** 2026-09-17

## Context
The brain's structure (types, fields, conventions, tooling) will change as content is ingested. Decisions about arc42 content itself belong on the site; decisions about the brain need a home too.

## Decision
We record every decision about the brain's own structure as an ADR in `_system/adr/`, numbered, one line each in `_system/index.md`. ADRs are English, terse, and never rewritten; a change is a new ADR that supersedes.

## Consequences
Schema changes are traceable. Agents must read the ADRs before proposing a new field or folder.
