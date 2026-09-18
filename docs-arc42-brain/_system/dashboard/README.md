# docs-arc42-brain dashboard

Status tiles, list/detail pages, lint, link health, and the generate/preview
actions for people curating the brain. Design:
`../../../docs/superpowers/specs/2026-09-18-docs-arc42-brain-dashboard-design.md`.

**Run**: `make dashboard` from the repo root (http://localhost:4211, repo
mounted read-write), then `make dashboard-down`. `make dashboard-logs` tails it.

**Test**: `make dashboard-test` (Docker); on the host,
`~/.local/bin/uv run --directory docs-arc42-brain/_system/dashboard pytest -q`.

**Architecture**: Flask app factory (`app.py`, routes only, <300 lines);
presence/actions/link-check/reload routes split into `routes_live.py`;
`model.py`/`relations.py` build render-ready views over a `braingen`-loaded
vault (no parser of its own); `render.py` turns wiki markdown/wikilinks into
HTML; `actions.py` runs `make lint`/`generate`/`generate-check` as one
locked, logged job at a time; `presence.py` tracks tabs and the facilitator.
