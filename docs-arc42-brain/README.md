# docs-arc42-brain

The content of docs.arc42.org as a Karpathy-style LLM wiki: `raw/` holds
immutable sources, `wiki/` holds typed, interlinked pages, and the schema
(`CLAUDE.md`, `_templates/`, `_system/adr/`) evolves with the content.

Open this folder in Obsidian as a vault to browse and graph it. Point Claude
Code at it and it reads `CLAUDE.md`. All make targets run from the repo root:
`make help` lists the `brain-*` ones.

Design: `../docs/superpowers/specs/2026-09-17-docs-arc42-brain-design.md`.
