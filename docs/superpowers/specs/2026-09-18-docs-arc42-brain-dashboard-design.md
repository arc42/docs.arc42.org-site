# docs-arc42-brain dashboard — design

Status: draft for review · 2026-09-18 · branch `docs-arc42-brain`

Supersedes §7 and revises D9 of
`2026-09-17-docs-arc42-brain-design.md` (the brain spec). Everything else in
the brain spec stands; terms used here (types, statuses, `related:`, lint
rules, `make generate`, `make generate-check`) are defined there.

## 1. Purpose

A dashboard for the people who write and curate arc42 content: it shows the
state of the brain (what is ingested, reviewed, published, broken, unlinked),
lets several people look at it at once, and runs the one tooling step that a
content session ends with — lint, then generate. Editing stays in Obsidian and
Claude Code; committing stays in git.

## 2. Decisions (2026-09-18)

| # | Decision | Consequence |
|---|---|---|
| D16 | **Revises D9.** The dashboard is a Flask server, not a static export. | It can host presence and run actions. `make dashboard` starts a container. |
| D17 | Multi-user means eTSU-style **presence**: several tabs at once, the earliest tab is the facilitator, no identity, nothing persisted. | No accounts, no roles, no per-user data. Lifted from eTSU's `/ping`, `/leaving`, `/who`. |
| D18 | The only actions are **lint and generate** (plus a preview into `build/parity/`). Nothing commits, nothing pushes, nothing edits a wiki page. | The dashboard never writes to git history. What it writes to the tree, git shows. |
| D19 | The dashboard is built **after phase 2**, so the generate button runs a real generator on day one. | It is phase 3's first deliverable; the remaining eleven ingests follow in the same phase. |
| D20 | Runtime is **Docker Compose**, repo mounted read-write, image built from the repo's own Dockerfile. No host install beyond Docker. | Same on every machine. `make` and `git` run inside the container. |
| D21 | The dashboard reads the model through **braingen** (`load_vault`, `lint`), never through its own parser. | Dashboard and lint cannot disagree. |
| D22 | Not lifted from eTSU: QR join page, self-shutdown watchdog. | `make dashboard-down` stops the container. |
| D23 | Port **4211**, registered in meta.arc42.org's `raw/port-assignment.md` (separate commit in that repo). | Next to the docs site's 4210. |

## 3. Pages

### 3.1 Home: tiles

One tile per concern, each with a count, a status bar (draft / review /
published) and an open-issues flag; each links to its list page.

| Tile | Shows | Links to |
|---|---|---|
| Sections | 12 by status; per section: tips, examples, terms, open issues, parity status (last `generate-check` result, cached) | `/sections` |
| Tips | total by status; tips without `related`; tips still carrying `legacy-tags` | `/tips` |
| Examples | total by system; examples whose `example-category` no section directive references | `/examples` |
| FAQ | until phase 4: "136 answers in faq.arc42.org, not yet ingested", no link; afterwards a normal type tile | `/faq` |
| Tags | terms and keywords with usage counts; terms without a definition sentence or `home`; the legacy tags that disappear from the site on cut-over (brain spec §4.5) | `/tags` |
| Issues | open by severity and kind, oldest first | `/issues` |
| Lint | last run: errors and warnings grouped by rule | `/lint` |
| Latest changes | last five entries of `_system/log.md`; last ten commits touching `docs-arc42-brain/` | `/log` |
| Generate | the action tile, §4 | `/actions` |
| Review queue | pages in `review`, oldest `updated` first, with ingest.md's checklist inline | `/review` |
| Cut-over readiness | per section: ingested, lint clean, parity green, related links present; the next section whose PR can be opened is highlighted | `/cutover` |
| Gaps | tips without an example, examples without a tip, subsections nobody links to, sections with zero related links | `/gaps` |
| Link health | last on-demand external link check: unique URLs with HTTP status, redirects and failures first | `/links` |

### 3.2 List and detail pages

- One list page per type with filters by status, section and system.
- Detail page per wiki page: rendered markdown (callouts rendered as the
  site's help boxes, directives shown as labels), frontmatter, links in and
  out, sources, issues that name the page, and an `obsidian://open?vault=…`
  link.
- **Suggestions** (brain spec §7, D5): computed link candidates not yet in
  `related:`, grouped by page, with the one-line reason and the weights from
  `_system/workflows/relations.md`. Read-only: promotion happens in the vault.
- **Graph**: cytoscape force graph of the link graph, filter by type; the term
  co-occurrence graph is the same page with a different edge source.
- **Search** in the top nav, not a tile.

### 3.3 Not in

Editing pages, commits, pushes, user accounts, analytics, stale-content
reports.

## 4. Actions

### 4.1 Generate

`POST /actions/generate` runs `make brain-lint && make generate` in a
subprocess in the mounted repo.

- **Facilitator only.** The server compares the caller's client id with the
  earliest-seen live tab (D17). Other tabs see the button disabled with "only
  the facilitator can generate".
- **One job at a time.** A process-wide lock. A second request while a job
  runs returns that job's log; it does not queue.
- **Lint gates generate.** Lint errors stop the run; the tile shows them
  grouped by rule. Warnings do not stop it.
- **Nothing commits.** After the run the tile shows the log, `git status
  --short` and `git diff --stat` restricted to the generated paths.
- **Run record.** Each generate run appends one line to `_system/log.md`:
  `## [YYYY-MM-DD] generate | dashboard, N files changed`. Lint-only runs and
  previews are not logged. The full output goes to
  `build/dashboard/runs/<timestamp>.log` (gitignored).
- **Failure shape.** Non-zero exit shows the exit code and the last 200 lines;
  the run file keeps everything.

### 4.2 Preview

`POST /actions/preview` runs the parity generator into `build/parity/` (brain
spec §6) and shows the per-section diff summary. Same lock, same facilitator
rule, no log entry.

### 4.3 Link check

`POST /actions/linkcheck` requests `HEAD` for every unique external URL in
`wiki/`, with a cache keyed by URL and a one-day TTL under
`build/dashboard/links.json`. Any viewer may start it. Results feed the Link
health tile; raising an issue for a dead link is a human step.

### 4.4 Reload

`POST /reload` clears the model cache, as in eTSU, for when the vault changed
underneath a running dashboard.

## 5. Presence

Lifted from eTSU (`_system/adr/0022`, addendum of 2026-09-07):

- Each tab generates a random client id in `sessionStorage`, sends `/ping`
  every 20 seconds and a `/leaving` beacon on `pagehide`.
- The server keeps `{client_id: (first_seen, last_seen)}` in memory; a tab is
  live if its last ping is younger than 90 seconds.
- The facilitator is the live tab with the earliest `first_seen`, computed
  server-side on every request that needs it.
- `/who` lists live tabs with eTSU's nicknames; the footer shows "N connected".
- Nothing is persisted; a restart forgets everyone.

## 6. Runtime and layout

```
docs-arc42-brain/_system/dashboard/
  app.py            Flask app: routes only, under 300 lines
  model.py          views over braingen: tiles, lists, gaps, readiness
  presence.py       client map, facilitator, ping/leaving/who
  actions.py        Job dataclass, lock, generate/preview/linkcheck runners
  templates/        base.html + one template per page, partials prefixed _
  static/           style.css (tokens from this repo's DESIGN.md), app.js,
                    vendor/cytoscape*.js (vendored, no CDN)
  Dockerfile        python 3.12, uv, make, git; installs braingen from
                    _system/generate; gunicorn
  compose.yaml      service brain-dashboard, repo mounted rw at /repo,
                    ports 4211:4211, restart: no
  tests/            test_model.py, test_actions.py (fake make),
                    test_presence.py (fake clock), fixture vault
```

Make targets in `_system/brain.mk`: `dashboard` (compose up, prints the LAN
URL), `dashboard-down`, `dashboard-logs`, `dashboard-test`.

The model is loaded through `braingen.parse.load_vault` and
`braingen.lint.lint`, cached by the newest mtime under `wiki/`,
`raw/sources/` and `_system/log.md`.

Visual identity: colors and type from this repo's `DESIGN.md`; eTSU's token
structure (spacing and type scales, hairline panels, dual theme) is the
pattern, not its palette.

## 7. Testing

- `model.py` against a fixture vault of a few pages per type, asserting tile
  counts, gaps and readiness rules.
- `actions.py` against a fake `make` on `PATH` that records its arguments and
  exits with a chosen code; asserts the lock, the lint gate, the log line and
  the failure shape.
- `presence.py` with an injected clock; asserts liveness and facilitator
  selection.
- `make dashboard-test` runs them inside the image.
- No browser tests.

## 8. Phasing

Phase 3 of the brain plan becomes: (1) this dashboard, (2) ingest and cut over
the remaining eleven sections using it. The dashboard's own plan is written
after phase 2 lands, because §4.1 and §4.2 call phase 2's targets.

## 9. Open points

- Whether "mark published" becomes a dashboard action once cut-over exists
  (would be D18's first exception; needs its own decision).
- Whether presence should survive a container restart (a file under
  `build/`); not needed until someone misses it.
- Whether the Suggestions page gets a "promote" button that edits `related:`
  on both pages (would break "editing stays in the vault"; decide with the
  first real promotion session).
