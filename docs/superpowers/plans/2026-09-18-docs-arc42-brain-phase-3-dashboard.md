# docs-arc42-brain phase 3a — dashboard: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A Flask dashboard on port 4211, in Docker, that shows the state of the brain, knows who is connected, and lets the facilitator run lint + generate and the parity preview.

**Architecture:** A flat Python project under `docs-arc42-brain/_system/dashboard/`, managed by uv, with braingen as a path dependency. It reads the vault only through `braingen` (`load_vault`, `lint`, `plan`, `not_ingested`, `section_of`, `tags_for`). Model views are pure functions over a cached `Brain`, and `app.py` holds only the routes. Actions run `make` in a subprocess against the mounted repo. `BRAINGEN` is overridden, so no uv runs inside the container.

**Tech Stack:** Python ≥ 3.12, Flask 3, Python-Markdown (with `tables`, `fenced_code`, `sane_lists`, `md_in_html`), gunicorn (gthread, 1 worker), uv, Docker Compose, cytoscape.js (vendored from eTSU, MIT).

**Spec:** `docs/superpowers/specs/2026-09-18-docs-arc42-brain-dashboard-design.md` (the dashboard spec). It revises the brain spec `docs/superpowers/specs/2026-09-17-docs-arc42-brain-design.md`.

**Scope:** This plan builds the dashboard only (dashboard spec §8, part 1). The ingest and cut-over of the other eleven sections are separate plans.

## Global Constraints

- Branch `docs-arc42-brain`. Never push, never open a PR, never merge.
- Every commit message ends with exactly this line: `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. The rule is literal and holds whatever the model; the user set it. Stage with explicit `git add <paths>`, never `git add -A` or `git add .`. Verify the trailer after each commit: `git log -1 --format=%B | sed '/^$/d' | tail -1`.
- Changes stay under `docs-arc42-brain/` and `docs/`, plus one exception: the root `.gitignore`, which gains the line `docs-arc42-brain/_system/dashboard/.venv/`. `_layouts/`, `_includes/`, `_sass/`, `_data/`, `_pages/`, `_posts/`, `_examples/`, `Makefile`, `Dockerfile` and `docker-compose.yml` are not touched. Root `make help` already lists every `##` target of `brain.mk`.
- No page under `docs-arc42-brain/wiki/` is edited.
- The dashboard itself never commits, pushes or edits a wiki page (D18). It writes only in four ways:
  - through `make generate`;
  - one appended line in `docs-arc42-brain/_system/log.md` per successful generate;
  - files under `docs-arc42-brain/build/dashboard/`;
  - parity output under `docs-arc42-brain/build/parity/`, via `make generate-check`.
- It reads the model only through braingen (D21) and has no parser of its own.
- Port **4211**. No CDN: every script and stylesheet is served from `static/`. Fonts are only named in font stacks (DESIGN.md families with system fallbacks); no font files are added.
- `app.py` holds only routes and stays under 300 lines.
- Tests:
  - on the host: `~/.local/bin/uv run --directory docs-arc42-brain/_system/dashboard pytest -q`;
  - in Docker: `make dashboard-test`;
  - braingen's own suite still passes: `make brain-test`;
  - no browser tests.
- Tools: uv is at `~/.local/bin/uv`, and system `python3` is 3.14. Docker is available.

## File structure

```
docs-arc42-brain/_system/dashboard/
  pyproject.toml     uv project (package = false); deps flask, markdown, gunicorn; braingen as path dep
  uv.lock
  app.py             create_app(): routes only
  model.py           Model (mtime cache) + Brain; tile/list views, readiness, gaps
  relations.py       links in/out, issues naming a page, suggestions, graphs, search
  render.py          markdown → HTML: callouts, directives, wikilinks
  presence.py        Presence: ping/leaving/who, facilitator, nicknames
  actions.py         Job, Runner (lock, generate, preview), log line, run files, parity cache
  linkcheck.py       external_urls, LinkChecker (HEAD, 1-day cache)
  templates/         base.html, one template per page, partials prefixed _
  static/            style.css, app.js, vendor/cytoscape.min.js
  Dockerfile         python 3.12-slim + uv + make + git; deps from uv.lock; code from the mount
  compose.yaml       service brain-dashboard, repo mounted rw at /repo, 4211:4211, restart "no"
  tests/             kit.py (fixture repo), test_*.py
```

Deviation from dashboard spec §6, recorded here: `relations.py`, `render.py` and `linkcheck.py` are split out of `model.py` and `actions.py` so that no file does two jobs.

## The fixture repo (shared by every test task)

`tests/kit.py`'s `build_repo(root) -> Path` builds this repository. All test expectations below depend on it.

| Page | Status | Key fields |
|---|---|---|
| section-9 | published | braingen's vaultkit body: H1 "9. Architecture Decisions", callout with "## Background (on ADRs)", `%% examples: decisions %%`, `%% examples-link %%` |
| section-3 | draft | body `# 3. Context and Scope\n\n## Business Context\n\nText.\n`, posts-dir `03-context`, category `context` |
| tip-9-1 | published | related `[[09-decision-example-x]]`; section `[[section-9#Background (on ADRs)]]`; terms `[[adr]]`; keywords `[[lean]]`; body links https://adr.github.io/ and `[[tip-9-2]]` |
| tip-9-2 | draft | related []; legacy-tags [criteria]; terms `[[adr]]` |
| tip-9-3 | review, updated 2026-09-05 | related []; terms `[[adr]]`, `[[stakeholder]]` |
| 09-decision-example-x | published | system `[[htmlsc]]`, category decisions, related `[[tip-9-1]]` |
| 09-decision-example-y | draft | system "", category orphans (lint error), related [] |
| adr (term) | review, updated 2026-09-01 | legacy-tags [adr, ADRs], home `[[section-9#Background (on ADRs)]]`, body starts with `**Definition.**` |
| stakeholder (term) | draft | legacy [], home "", body without a definition |
| lean (keyword), htmlsc (system "HTML Sanity Checker") | draft | — |
| ISS-001 | open, minor, gap, created 2026-09-02 | related `[[tip-9-1]]` |
| ISS-002 | resolved, major, contradiction, created 2026-09-01 | related `[[tip-9-2]]` |
| ISS-003 | open, major, risk, created 2026-09-03 | related `[[section-3]]` |

Site files are placeholders: `_posts/09-decisions/2016-03-01-t-9-{1,2,3}.md`, `_posts/03-context/2016-01-01-t-3-1.md` and empty `_pages/` and `_examples/`. Lint of the fixture gives 1 error (rule `example-category`, page 09-decision-example-y) and 2 warnings (rule `reciprocity`, pages ISS-001 and ISS-002).

---

### Task 1: braingen — lint findings carry a rule id

**Files:**
- Modify: `docs-arc42-brain/_system/generate/braingen/lint.py`
- Test: `docs-arc42-brain/_system/generate/tests/test_lint.py` (append)

**Interfaces:**
- Produces: `Finding(level, page, message, rule="other")`. `rule` is a short kebab-case id, and `str(Finding)` stays unchanged, so CLI output is the same.

- [ ] **Step 1: Append the failing test** to `tests/test_lint.py`:

```python
def test_findings_carry_rule_ids(tmp_path):
    from braingen.lint import Finding, lint
    from braingen.parse import load_vault
    from tests import vaultkit as vk

    vk.source(tmp_path)
    vk.section(tmp_path)
    vk.tip(tmp_path, "9-1", related=["[[tip-9-2]]", "[[nowhere]]"], status="draft")
    vk.tip(tmp_path, "9-2", status="draft")
    vk.example(tmp_path, "09-decision-example-y", status="draft", **{"example-category": "orphans"})
    rules = {(f.page, f.rule) for f in lint(load_vault(tmp_path))}
    assert ("tip-9-1", "link") in rules
    assert ("tip-9-1", "reciprocity") in rules
    assert ("09-decision-example-y", "example-category") in rules
    assert str(Finding("error", "p", "m", "link")) == "ERROR   p: m"
```

- [ ] **Step 2: Check that it fails.** Run `~/.local/bin/uv run --directory docs-arc42-brain/_system/generate pytest -q tests/test_lint.py`. Expected: FAIL (`Finding` has no `rule`).

- [ ] **Step 3: Implement.**
  1. Add a fourth dataclass field to `Finding`: `rule: str = "other"`. `__str__` stays unchanged.
  2. Pass `rule=` to every `Finding(...)` in `lint.py`:

  | Where | Message starts with | rule |
  |---|---|---|
  | `lint()` vault errors | (any) | `parse` |
  | `lint()` duplicate id | `duplicate id` | `duplicate-id` |
  | `_schema` | `unknown type` | `type` |
  | `_schema` | `type … belongs in` | `folder` |
  | `_schema` | `missing field` | `required-field` |
  | `_schema` | `invalid status` | `status` |
  | `_schema` | `published without sources` | `sources` |
  | `_schema` | `legacy-tags still present` | `legacy-tags` |
  | `_check_link` | `unresolved link` | `link` |
  | `_check_link` | `heading '…' not found` / `is not unique` | `heading` |
  | `_links` | `related … is not reciprocated` | `reciprocity` |
  | `_body` | `Liquid syntax` | `liquid` |
  | `_body` | `missing image` | `image` |
  | `_body` | `unknown directive` | `directive` |
  | `_example_directives` | both messages | `example-category` |

- [ ] **Step 4: Run it.** Run `make brain-test` (from the repo root). Expected: every test passes, including the new one.

- [ ] **Step 5: Check that lint output is unchanged.** Run `make brain-lint`. Expected: `33 findings, 0 errors, 33 warnings`, the same as before.

- [ ] **Step 6: Commit.**

```bash
git add docs-arc42-brain/_system/generate/braingen/lint.py docs-arc42-brain/_system/generate/tests/test_lint.py
git commit -m "braingen: lint findings carry a rule id (for the dashboard's grouping)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2: dashboard scaffold, fixture repo, Docker runtime, make targets

**Files:**
- Create:
  - `docs-arc42-brain/_system/dashboard/pyproject.toml` and `uv.lock` (generated by `uv lock`);
  - `app.py`, `templates/base.html`, `templates/home.html`, `static/style.css`, `static/app.js` (empty stub);
  - `Dockerfile`, `compose.yaml`, `.dockerignore`;
  - `tests/__init__.py`, `tests/kit.py`, `tests/conftest.py`, `tests/test_kit.py`, `tests/test_app_smoke.py`.
- Modify: `docs-arc42-brain/_system/brain.mk`, root `.gitignore`.

**Interfaces:**
- Produces:
  - `app.create_app(repo: Path | None = None, **services) -> Flask`. `repo` defaults to `Path(os.environ.get("BRAIN_REPO", "."))`. `app.config["REPO"]` is set. `services` accepts later-injected objects (`model`, `presence`, `runner`, `linkchecker`); for now they are stored in `app.extensions["brain"]`, a dict.
  - `tests/kit.py`: `build_repo(root: Path) -> Path` builds the fixture repo from the table above; `DAY = "2026-09-18"`.
  - `tests/conftest.py`: fixtures `repo` (`build_repo(tmp_path)`), `vault_root` (`repo / "docs-arc42-brain"`) and `client` (`create_app(repo).test_client()`).

- [ ] **Step 1: Write `pyproject.toml`.**

```toml
[project]
name = "brain-dashboard"
version = "0.1.0"
description = "Dashboard for docs-arc42-brain (phase 3)"
requires-python = ">=3.12"
dependencies = [
  "flask>=3.0",
  "markdown>=3.6",
  "gunicorn>=22",
  "braingen",
]

[tool.uv]
package = false

[tool.uv.sources]
braingen = { path = "../generate", editable = true }

[dependency-groups]
dev = ["pytest>=8.0"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

Run `~/.local/bin/uv lock --directory docs-arc42-brain/_system/dashboard`. Add `docs-arc42-brain/_system/dashboard/.venv/` to the root `.gitignore`, under the `# docs-arc42-brain` block.

- [ ] **Step 2: Write `tests/kit.py`.** Build every page with `braingen.importer.write_page(path, meta, body)`. Common fields: id, type, title, status, created (`DAY` unless stated), updated (`DAY` unless stated), `sources: ["[[SRC-001-test]]"]`, related.
  - Pages: exactly the fixture table above.
  - Section 9's body is braingen's `tests/vaultkit.SECTION_BODY`, copied verbatim; do not import across projects.
  - Section front matter: `number, name, category, posts-dir, permalink, order, faq-topic`, as in vaultkit's `section()`. Section 3 uses name "Context and Scope", category `context`, posts-dir `03-context`, permalink `/section-3/`, order 7.
  - Tips: `section, keywords, terms, legacy-tags, date: "2016-03-01", permalink /tips/<id>/`. Tip-9-2 and tip-9-3 use `section: "[[section-9]]"`.
  - Examples: `section: "[[section-9]]", system, example-category, keywords: [], terms: [], legacy-tags: [], permalink /examples/<slug>/`.
  - Terms: `term, aliases: [], legacy-tags, home`.
  - Keyword: `description: "A facet.", featured: False`.
  - System: `name`.
  - Issues: `severity, kind, raised-by: agent, resolved: null`, status as in the table, and `created` as in the table (`updated` = `created`).
  - Source `raw/sources/SRC-001-test.md`: type source, status ingested, `origin: raw/test/`, `files: []`.
  - `_system/log.md`: the header and format comment of the real log, then six entries:

    ```
    ## [2026-09-10] bootstrap | one
    ## [2026-09-11] ingest | two
    ## [2026-09-12] ingest | three
    ## [2026-09-13] audit | four
    ## [2026-09-14] cutover | five
    ## [2026-09-15] generate | six
    ```

    Each entry has one `- notes: x` line and a blank line after it.
  - `_system/workflows/ingest.md`: a verbatim copy of the real `docs-arc42-brain/_system/workflows/ingest.md`, embedded as a string constant.
  - Site placeholders, each with the content `---\ntitle: x\n---\n`:
    - `_posts/09-decisions/2016-03-01-t-9-1.md`, `…-t-9-2.md`, `…-t-9-3.md`;
    - `_posts/03-context/2016-01-01-t-3-1.md`.

    Create `_pages/` and `_examples/` as empty directories.

- [ ] **Step 3: Write `tests/test_kit.py`.** It pins the fixture to its documented lint result:

```python
from braingen.lint import lint
from braingen.parse import load_vault


def test_fixture_lint_matches_the_plan(vault_root):
    findings = lint(load_vault(vault_root))
    errors = sorted((f.rule, f.page) for f in findings if f.level == "error")
    warnings = sorted((f.rule, f.page) for f in findings if f.level == "warning")
    assert errors == [("example-category", "09-decision-example-y")]
    assert warnings == [("reciprocity", "ISS-001"), ("reciprocity", "ISS-002")]
```

- [ ] **Step 4: Write `tests/test_app_smoke.py`.**

```python
def test_home_renders_with_title_and_nav(client):
    r = client.get("/")
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert "<title>docs-arc42-brain</title>" in html
    assert 'href="/static/style.css' in html
    assert "cdn" not in html.lower()
```

- [ ] **Step 5: Implement `app.py`, `base.html`, `home.html` and `style.css`.**
  - `base.html`:
    - head `<title>{% block title %}docs-arc42-brain{% endblock %}</title>`, loading `/static/style.css` and `/static/app.js` (defer);
    - a masthead with the brand "docs-arc42-brain" and a nav placeholder block;
    - `<main>{% block main %}{% endblock %}</main>`;
    - a footer with `<span id="presence-count"></span>`.
  - `home.html` extends it with a heading.
  - `style.css` holds the tokens only, as CSS custom properties from `DESIGN.md`:
    - colors signal-blue, deep-blue, header-tint, help-bg/help-ink, example-bg/example-ink, tag-bg, emerald, coral, ink, paper, muted, surface-1, surface-2, hairline, amber, maroon;
    - spacing `--s1: 4px … --s8: 64px`: 4, 8, 12, 16, 24, 32, 48, 64;
    - `--radius: 4px`, `--radius-pill: 999px`;
    - fonts: `--font-display: 'Libre Caslon Text', Georgia, serif`, `--font-body: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', system-ui, sans-serif`, `--font-code: ui-monospace, 'SF Mono', Menlo, Consolas, monospace`;
    - dark theme: the same tokens redefined under `@media (prefers-color-scheme: dark)`, with ink/paper inverted and the deep-blue masthead kept;
    - `body` gets an explicit background and color.

    Later tasks add components.
  - `app.py`:
    - `create_app` registers `/`, which renders `home.html`;
    - module-level `app = None`; the Docker command calls `create_app()` through gunicorn's `app:create_app()` factory syntax.

- [ ] **Step 6: Run the tests.** Run `~/.local/bin/uv run --directory docs-arc42-brain/_system/dashboard pytest -q`. Expected: 2 passed.

- [ ] **Step 7: Write the Dockerfile.** The build context is `docs-arc42-brain/_system`, so the build can see `generate/` and `dashboard/`. At runtime all code comes from the mounted repo, so an edit needs only a container restart, not a rebuild.

```dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends make git \
    && rm -rf /var/lib/apt/lists/* \
    && git config --system --add safe.directory /repo
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /usr/local/bin/uv
WORKDIR /build
COPY generate/pyproject.toml generate/pyproject.toml
COPY generate/braingen generate/braingen
COPY dashboard/pyproject.toml dashboard/uv.lock dashboard/
# Third-party deps only; braingen and the dashboard are imported from the mount.
RUN cd dashboard && uv export --frozen --no-hashes --no-emit-project --no-emit-package braingen -o /tmp/req.txt \
    && uv pip install --system --no-cache -r /tmp/req.txt
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    BRAIN_REPO=/repo \
    PYTHONPATH=/repo/docs-arc42-brain/_system/dashboard:/repo/docs-arc42-brain/_system/generate
WORKDIR /repo/docs-arc42-brain/_system/dashboard
EXPOSE 4211
CMD ["gunicorn", "--bind", "0.0.0.0:4211", "--worker-class", "gthread", "--workers", "1", "--threads", "8", "app:create_app()"]
```

The export must include pytest as well (the dev group is on by default in `uv export`), because `make dashboard-test` runs pytest in this image. If `uv export` rejects a flag, adjust it and say so in the report. What must hold: only third-party packages are installed, and braingen comes from the mount.

`.dockerignore` sits in `docs-arc42-brain/_system/`, because that is the context. Its lines are `**/.venv`, `**/__pycache__` and `**/.pytest_cache`.

- [ ] **Step 8: Write `compose.yaml`.**

```yaml
# The project name keeps this container apart from the docs site's (docs-arc42-site).
name: docs-arc42-brain

services:
  brain-dashboard:
    build:
      context: ..
      dockerfile: dashboard/Dockerfile
    image: docs-arc42-brain-dashboard:latest
    init: true
    # Host uid/gid, so generated files belong to the user on Linux hosts too.
    user: "${DASH_UID:-1000}:${DASH_GID:-1000}"
    environment:
      HOME: /tmp
      TZ: "${TZ:-UTC}"
    volumes:
      - "${REPO_DIR:-../../..}:/repo"
    ports:
      - "4211:4211"
    # On-demand tool: `make dashboard-down` stops it and it stays down.
    restart: "no"
```

- [ ] **Step 9: Add the make targets** to `brain.mk`. Add the new targets to `.PHONY` as well.

```make
DASH_DIR     := $(BRAIN_DIR)/_system/dashboard
DASH_COMPOSE := REPO_DIR=$(CURDIR) DASH_UID=$$(id -u) DASH_GID=$$(id -g) docker compose -f $(DASH_DIR)/compose.yaml

dashboard: ## Start the brain dashboard in Docker (http://localhost:4211)
	$(DASH_COMPOSE) up --build -d
	@lan=$$(ipconfig getifaddr en0 2>/dev/null || hostname -I 2>/dev/null | awk '{print $$1}'); \
	echo "==> http://localhost:4211"; test -z "$$lan" || echo "==> LAN: http://$$lan:4211"

dashboard-down: ## Stop the brain dashboard
	$(DASH_COMPOSE) down

dashboard-logs: ## Follow the brain dashboard's logs
	$(DASH_COMPOSE) logs -f brain-dashboard

dashboard-test: ## Run the dashboard tests inside its Docker image
	$(DASH_COMPOSE) run --rm --build --no-deps brain-dashboard python -m pytest -q -p no:cacheprovider
```

- [ ] **Step 10: Verify Docker.**
  1. Run `make dashboard-test`. Expected: 2 passed, inside the container.
  2. Run `make dashboard`, then `curl -s localhost:4211/ | grep -c docs-arc42-brain`. Expected: ≥ 1.
  3. Run `make dashboard-down`.
  4. Run `make help`. Expected: the four dashboard targets appear in the Brain group.
  5. Run `git status --short`. Expected: no stray files (no `.venv`, no `__pycache__`, nothing root-owned).

- [ ] **Step 11: Commit** with explicit paths:
  - the `dashboard/` files listed above, including `uv.lock` and `tests/`;
  - `docs-arc42-brain/_system/.dockerignore`, `brain.mk` and `.gitignore`.

  Message: `dashboard: scaffold, fixture repo, Docker runtime on 4211, make targets`, with the trailer.

---

### Task 3: presence

**Files:**
- Create: `dashboard/presence.py`, `dashboard/tests/test_presence.py`
- Modify: `dashboard/app.py`, `dashboard/static/app.js`, `dashboard/templates/base.html`, and a new `templates/who.html`

**Interfaces:**
- Produces:
  - `Presence(clock=time.monotonic, live_after=90.0, leave_grace=5.0)`, with these methods:
    - `.ping(cid) -> dict` returns `{"nickname", "is_facilitator", "count"}`;
    - `.leaving(cid) -> None`;
    - `.live() -> list[str]`, ordered by first_seen;
    - `.facilitator() -> str | None`;
    - `.is_facilitator(cid) -> bool`;
    - `.who() -> list[dict]` returns `{"nickname", "is_facilitator", "connected_seconds"}`, facilitator first.
  - `nickname(cid) -> str`.
  - `client_id(request) -> str`, from the JSON body `client_id`, capped at 64 characters, default `"anon"`.
  - Routes: `POST /ping` (JSON), `POST /leaving` (204), `GET /who`.
  - `app.extensions["brain"]["presence"]`.

- [ ] **Step 1: Write the failing tests.**

```python
from presence import Presence, nickname


class Clock:
    def __init__(self): self.t = 1000.0
    def __call__(self): return self.t


def test_first_live_tab_is_facilitator_and_role_passes_on():
    c = Clock(); p = Presence(clock=c)
    assert p.ping("a")["is_facilitator"] is True
    c.t += 1; assert p.ping("b")["is_facilitator"] is False
    assert p.live() == ["a", "b"]
    c.t += 60; p.ping("b")            # a silent for 61 s: still live (limit 90 s)
    assert p.facilitator() == "a"
    c.t += 40; p.ping("b")            # a silent for 101 s: gone
    assert p.live() == ["b"] and p.facilitator() == "b"


def test_leaving_then_ping_keeps_first_seen_navigation():
    c = Clock(); p = Presence(clock=c)
    p.ping("a"); c.t += 1; p.ping("b")
    p.leaving("a"); c.t += 2; p.ping("a")   # next page of the same tab
    assert p.facilitator() == "a"


def test_leaving_without_return_drops_after_grace():
    c = Clock(); p = Presence(clock=c)
    p.ping("a"); c.t += 1; p.ping("b")
    p.leaving("a"); c.t += 6
    assert p.live() == ["b"] and p.is_facilitator("b")


def test_count_and_who():
    c = Clock(); p = Presence(clock=c)
    p.ping("a"); c.t += 5
    r = p.ping("b")
    assert r["count"] == 2 and r["nickname"] == nickname("b")
    who = p.who()
    assert [w["is_facilitator"] for w in who] == [True, False]
    assert who[0]["connected_seconds"] == 5


def test_nickname_is_stable_and_two_words():
    assert nickname("x1") == nickname("x1") and len(nickname("x1").split()) == 2


def test_routes(client):
    r = client.post("/ping", json={"client_id": "tab-1"})
    assert r.get_json()["is_facilitator"] is True
    assert client.post("/leaving", json={"client_id": "tab-1"}).status_code == 204
    assert "connected" in client.get("/who").get_data(as_text=True)
```

- [ ] **Step 2: Check that they fail.** Run the dashboard tests. Expected: ImportError on `presence`.

- [ ] **Step 3: Implement `presence.py`.**
  - State is three dicts: `_last`, `_first` and `_leaving` (cid → time), guarded by one `threading.Lock`.
  - Eviction runs at the start of every public call. A cid is dropped when either holds:
    - `now - _last[cid] > live_after`;
    - `cid in _leaving and now - _leaving[cid] > leave_grace`.
  - `ping`:
    - sets `_first` only when the cid is not known yet;
    - updates `_last` and removes the cid from `_leaving`;
    - `count` is the number of live cids.
  - Facilitator: the live cid with the smallest `_first`.
  - Nicknames: `zlib.crc32`. The adjective and animal lists are copied from eTSU's `app.py` (`_NICKNAME_ADJECTIVES`, `_NICKNAME_ANIMALS`, 12 each). Index them as eTSU does.
  - Nothing is persisted.

- [ ] **Step 4: Routes and front end.**
  - Routes in `app.py`: `/ping` returns `presence.ping(client_id(request))`; `/leaving`; `/who` renders `who.html`, a table of nickname, role and connected time.
  - `static/app.js`:
    - The client id lives in `sessionStorage["brain-client-id"]` (`crypto.randomUUID()` on first use). It is exposed as `window.brainClientId`.
    - It calls `ping()` on load and every 20 s.
    - A ping sets `#presence-count` to "N connected" and toggles `document.body.dataset.facilitator = "yes"|"no"`. It also dispatches a `brain:presence` event with the response.
    - On `pagehide` it calls `navigator.sendBeacon("/leaving", new Blob([JSON.stringify({client_id})], {type: "application/json"}))`.
  - The base footer links to `/who`.

- [ ] **Step 5: Run the tests.** Expected: all pass.

- [ ] **Step 6: Commit.** Message: `dashboard: presence — ping, leaving, who, facilitator (lifted from eTSU)`, with the trailer.

---

### Task 4: model — cache and tile views

**Files:**
- Create: `dashboard/model.py`, `dashboard/tests/test_model.py`

**Interfaces:**
- Consumes:
  - `braingen.parse.load_vault`, `braingen.lint.lint` / `Finding.rule`;
  - `braingen.emit.section_of`;
  - `braingen.generate.plan`;
  - `braingen.parity.not_ingested`, `PARITY_STATUSES`.
- Produces:

```python
@dataclass
class Brain:
    repo: Path            # repo root (the Jekyll site)
    vault: Vault          # braingen Vault of repo/"docs-arc42-brain"
    findings: list[Finding]

class Model:
    def __init__(self, repo: Path): ...
    def stamp(self) -> float          # newest mtime under wiki/, raw/sources/, and of _system/log.md
    def get(self) -> Brain            # reloads when stamp() changed since the last load
    def clear(self) -> None           # forget the cache (POST /reload)

STATUSES = ("draft", "review", "published", "retired")
def status_counts(pages) -> dict[str, int]                 # only statuses that occur
def section_number(b: Brain, page) -> int | None           # section of a section/tip/example; None otherwise
def open_issues(b: Brain) -> list[Page]                    # status open|in-progress, oldest created first
def issue_targets(b: Brain, issue) -> set[str]             # slugs in related + body links
def sections_view(b, parity: dict[str, str]) -> dict       # {"counts", "rows": [{number, slug, title, status, tips, examples, terms, open_issues, parity}]} rows by number
def tips_view(b) -> dict                                   # {"counts", "without_related": [slugs], "legacy": [slugs]}
def examples_view(b) -> dict                               # {"counts", "by_system": {name: n}, "orphan_categories": [cat]}
def faq_view(b) -> dict                                    # {"count": n, "note": str | None}
def tags_view(b) -> dict                                   # {"terms": [(slug, uses)], "keywords": [(slug, uses)], "incomplete_terms": [slug], "legacy": [(legacy, term)]}
def issues_view(b) -> dict                                 # {"open": [Page], "by_severity": {}, "by_kind": {}}
def lint_view(b) -> dict                                   # {"errors": {rule: [Finding]}, "warnings": {rule: [Finding]}}
def log_entries(b, n=5) -> list[dict]                      # newest first: {date, kind, subject}
def git_log(repo: Path, n=10) -> list[dict]                # {hash, date, subject}; [] when git fails
def review_queue(b) -> dict                                # {"pages": [Page oldest updated first], "checklist": [(label, text)]}
def readiness(b, parity) -> dict                           # {"rows": [...], "next": int | None}
def gaps(b) -> dict                                        # see test
```

Rules the views follow:
- **Section of a page:** for a tip or example, `section_of(vault, p)` (catch `ValueError` → None). For a term, the target of `home`, when it is a section page. A section's number is `int(meta["number"])`.
- **Open issues per section:** open issues whose targets include the section's slug or any page whose section number is that section.
- **Term and keyword usage:** the number of non-issue pages whose `terms:` (or `keywords:`) links name the slug.
- **Incomplete term:** the body has no `**Definition.**`, or `home` has no link.
- **Legacy tags:** for each term, `(legacy_tag, term_slug)` for every legacy tag that differs from the slug. These tags disappear from the site at cut-over.
- **Issues view:** `by_severity` and `by_kind` count open issues only.
- **Orphan categories:** example categories that no section `%% examples: X %%` directive names.
- **Parity cache:** a dict from section number as a string to "PASS" or "FAIL". A missing entry means unknown and renders as "—".
- **Review queue checklist:** the numbered items of `_system/workflows/ingest.md` whose bold label is one of Read, Vocabulary, Links, Issues, Status. `label` is the word without its dot; `text` is the rest of the item with its continuation lines joined by single spaces.
- **Readiness rows**, one per section:
  - `{number, slug, cut_over, ingested, lint_clean, parity, related, ready}`;
  - `cut_over`: status is published;
  - `ingested`: `not_ingested(vault, repo, n, generated)` is empty, where `generated` = the rels of `plan(vault, PARITY_STATUSES, section=n).outputs`. If plan raises, `ingested` = False;
  - `lint_clean`: no error finding whose page is the section or has that section number;
  - `parity`: from the cache, "PASS" / "FAIL" / None;
  - `related`: every non-retired tip and example of the section has a non-empty `related`, vacuously true;
  - `ready`: not cut_over and ingested and lint_clean and parity == "PASS" and related;
  - `next`: the smallest number with `ready`, or None.
- **Gaps:**
  - `tips_without_example`: tips whose `related` names no example;
  - `examples_without_tip`: examples whose `related` names no tip;
  - `unlinked_subsections`: for every non-synthetic heading of level ≥ 2 on a section page, `(section_slug, heading_text)`, when no link on any page (all front-matter link fields and body) targets that slug with that heading;
  - `sections_without_related`: sections whose own `related` is empty and whose slug is in no other non-issue page's `related`.

  Sorting: slugs alphabetical, sections by number.

- [ ] **Step 1: Write the failing tests** in `tests/test_model.py`:

```python
import os
import time

from model import (Model, examples_view, faq_view, gaps, issues_view, lint_view, log_entries,
                   readiness, review_queue, sections_view, tags_view, tips_view)


def brain(repo):
    return Model(repo).get()


def test_cache_reloads_on_change(repo):
    m = Model(repo)
    b1 = m.get(); assert m.get() is b1
    f = repo / "docs-arc42-brain/wiki/tips/tip-9-3.md"
    later = time.time() + 5
    os.utime(f, (later, later))
    assert m.get() is not b1
    m.clear(); assert m.get() is not None


def test_sections_view(repo):
    v = sections_view(brain(repo), {"9": "PASS"})
    assert v["counts"] == {"draft": 1, "published": 1}
    rows = {r["number"]: r for r in v["rows"]}
    assert [r["number"] for r in v["rows"]] == [3, 9]
    assert (rows[9]["tips"], rows[9]["examples"], rows[9]["terms"], rows[9]["open_issues"]) == (3, 2, 1, 1)
    assert rows[9]["parity"] == "PASS" and rows[3]["parity"] is None
    assert rows[3]["open_issues"] == 1


def test_tips_examples_faq(repo):
    b = brain(repo)
    t = tips_view(b)
    assert t["counts"] == {"draft": 1, "review": 1, "published": 1}
    assert t["without_related"] == ["tip-9-2", "tip-9-3"] and t["legacy"] == ["tip-9-2"]
    e = examples_view(b)
    assert e["by_system"] == {"(none)": 1, "HTML Sanity Checker": 1}
    assert e["orphan_categories"] == ["orphans"]
    f = faq_view(b)
    assert f["count"] == 0 and "136" in f["note"]


def test_tags_view(repo):
    v = tags_view(brain(repo))
    assert v["terms"] == [("adr", 3), ("stakeholder", 1)]
    assert v["keywords"] == [("lean", 1)]
    assert v["incomplete_terms"] == ["stakeholder"]
    assert v["legacy"] == [("ADRs", "adr")]


def test_issues_and_lint(repo):
    b = brain(repo)
    i = issues_view(b)
    assert [p.slug for p in i["open"]] == ["ISS-001", "ISS-003"]
    assert i["by_severity"] == {"major": 1, "minor": 1} and i["by_kind"] == {"gap": 1, "risk": 1}
    l = lint_view(b)
    assert list(l["errors"]) == ["example-category"] and len(l["warnings"]["reciprocity"]) == 2


def test_log_entries_newest_first(repo):
    e = log_entries(brain(repo))
    assert [x["subject"] for x in e] == ["six", "five", "four", "three", "two"]
    assert e[0] == {"date": "2026-09-15", "kind": "generate", "subject": "six"}


def test_review_queue(repo):
    q = review_queue(brain(repo))
    assert [p.slug for p in q["pages"]] == ["adr", "tip-9-3"]
    assert [label for label, _ in q["checklist"]] == ["Read", "Vocabulary", "Links", "Issues", "Status"]


def test_readiness(repo):
    r = readiness(brain(repo), {"9": "PASS", "3": "PASS"})
    rows = {x["number"]: x for x in r["rows"]}
    assert rows[9]["cut_over"] is True and rows[9]["ingested"] is True
    assert rows[9]["lint_clean"] is False and rows[9]["related"] is False
    assert rows[3]["ingested"] is False and rows[3]["lint_clean"] is True and rows[3]["related"] is True
    assert r["next"] is None


def test_readiness_next_when_ready(repo):
    (repo / "_posts/03-context/2016-01-01-t-3-1.md").unlink()
    r = readiness(brain(repo), {"3": "PASS"})
    assert r["next"] == 3


def test_gaps(repo):
    g = gaps(brain(repo))
    assert g["tips_without_example"] == ["tip-9-2", "tip-9-3"]
    assert g["examples_without_tip"] == ["09-decision-example-y"]
    assert g["unlinked_subsections"] == [("section-3", "Business Context")]
    assert g["sections_without_related"] == ["section-3", "section-9"]
```

- [ ] **Step 2: Check that they fail.** Expected: ImportError.

- [ ] **Step 3: Implement `model.py`.**
  - `git_log` runs `git -C <repo> log -<n> --date=short --format=%h%x1f%ad%x1f%s -- docs-arc42-brain/` with `subprocess.run(..., capture_output=True, text=True, timeout=10)`. It returns [] on any failure.
  - `log_entries` parses `^## \[(\d{4}-\d{2}-\d{2})\] ([\w-]+) \| (.*)$`.

- [ ] **Step 4: Run the tests.** Expected: all pass.

- [ ] **Step 5: Commit.** Message: `dashboard: model — mtime cache and tile views (sections, tips, tags, issues, lint, review, readiness, gaps)`, with the trailer.

---

### Task 5: relations and rendering

**Files:**
- Create: `dashboard/relations.py`, `dashboard/render.py`, `dashboard/tests/test_relations.py`, `dashboard/tests/test_render.py`

**Interfaces:**
- Consumes: `model.Brain`, braingen `Page`, `WikiLink`, `parse_wikilinks`.
- Produces:

```python
# relations.py
LINK_KEYS = ("related", "section", "sources", "home", "system", "terms", "keywords", "ingested-pages")
WEIGHTS = {"term": 3, "subsection": 2, "keyword": 1, "system": 2}   # _system/workflows/relations.md
def links_out(b, slug) -> list[tuple[str, str]]     # (target_slug, via) via = key name or "body"; unique, in order
def links_in(b, slug) -> list[tuple[str, str]]      # (source_slug, via), sorted
def issues_naming(b, slug) -> list[str]             # issue slugs whose related/body links name slug, sorted
def suggestions(b) -> dict[str, list[dict]]         # page slug -> [{"target", "score", "reasons"}], score desc then target
def link_graph(b) -> dict                           # {"nodes": [{"id","label","type","status"}], "edges": [{"source","target","kind"}]}
def term_graph(b) -> dict                           # nodes = terms; edges {"source","target","weight"} = pages carrying both
def search(b, q, limit=50) -> list[dict]            # {"slug","type","title","snippet"}; case-insensitive in title or body
def obsidian_url(b, page) -> str                    # obsidian://open?vault=docs-arc42-brain&file=<quoted rel path without .md>

# render.py
def render(body: str, known: set[str]) -> str       # markdown → HTML
```

Suggestion rules:
- Candidates are unordered pairs of tips and examples (non-retired), excluding pairs already related in either direction.
- Scores:
  - shared terms: 3 each, reason `shared term <slug> (3)`;
  - same subsection: 2 when both `section:` links carry the same heading and target, reason `same subsection <heading> (2)`;
  - shared keywords: 1 each, reason `shared keyword <slug> (1)`;
  - same system: 2, examples only, when both system links name the same system, reason `same system <slug> (2)`.
- Score > 0 lists the pair under both pages.

`link_graph`:
- nodes: every page except type issue and source;
- edges: `related` (kind `related`) and `section` (kind `section`) between those nodes, deduplicated as unordered pairs per kind.

`render`:
1. Callouts. The marker line itself is dropped. A block that starts with a line matching `^>\s*\[!([\w-]+)\]` runs until the first line that does not start with `>`. It becomes `<div class="callout {type}" markdown="1">` + the inner lines with one `> ` / `>` prefix stripped + `</div>`, with blank lines around it.
2. Directive lines `%% name: arg %%` / `%% name %%` (use braingen's `DIRECTIVE_RE`) become `<p class="directive">name: arg</p>`.
3. Wikilinks are replaced before markdown runs:
   - a known target becomes `<a class="wikilink" href="/page/{target}">{label or target#heading or target}</a>`;
   - an unknown one becomes `<span class="wikilink broken">…</span>`.
4. `markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "md_in_html"])`.

- [ ] **Step 1: Write the failing tests.**

```python
# tests/test_relations.py
from model import Model
from relations import (issues_naming, link_graph, links_in, links_out, obsidian_url, search,
                       suggestions, term_graph)


def b(repo):
    return Model(repo).get()


def test_links_out_and_in(repo):
    br = b(repo)
    out = links_out(br, "tip-9-1")
    for pair in [("09-decision-example-x", "related"), ("section-9", "section"), ("adr", "terms"),
                 ("lean", "keywords"), ("SRC-001-test", "sources"), ("tip-9-2", "body")]:
        assert pair in out
    assert links_in(br, "tip-9-1") == [("09-decision-example-x", "related"), ("ISS-001", "related")]
    assert issues_naming(br, "tip-9-1") == ["ISS-001"]


def test_suggestions(repo):
    s = suggestions(b(repo))
    first = s["tip-9-1"][0]
    assert first["score"] == 3 and first["reasons"] == ["shared term adr (3)"]
    assert {x["target"] for x in s["tip-9-1"]} == {"tip-9-2", "tip-9-3"}
    assert s["tip-9-3"][0]["target"] in {"tip-9-1", "tip-9-2"}
    assert "09-decision-example-x" not in {x["target"] for x in s.get("tip-9-1", [])}


def test_graphs(repo):
    br = b(repo)
    g = link_graph(br)
    ids = {n["id"] for n in g["nodes"]}
    assert "tip-9-1" in ids and "ISS-001" not in ids and "SRC-001-test" not in ids
    rel = [e for e in g["edges"] if e["kind"] == "related"
           and {e["source"], e["target"]} == {"tip-9-1", "09-decision-example-x"}]
    assert len(rel) == 1
    t = term_graph(br)
    assert {n["id"] for n in t["nodes"]} == {"adr", "stakeholder"}
    assert t["edges"] == [{"source": "adr", "target": "stakeholder", "weight": 1}]


def test_search_and_obsidian(repo):
    br = b(repo)
    assert [r["slug"] for r in search(br, "ADR.GITHUB")] == ["tip-9-1"]
    assert obsidian_url(br, br.vault.pages["tip-9-1"]) == \
        "obsidian://open?vault=docs-arc42-brain&file=wiki%2Ftips%2Ftip-9-1"
```

```python
# tests/test_render.py
from render import render


def test_callout_directive_wikilinks():
    body = ("> [!arc42-help]\n> ## Hello\n> Some *text*.\n\n"
            "%% examples: decisions %%\n\n"
            "See [[tip-9-1|the tip]] and [[nowhere]].\n")
    html = render(body, {"tip-9-1"})
    assert '<div class="callout arc42-help">' in html
    assert "<h2" in html and "<em>text</em>" in html
    assert '<p class="directive">examples: decisions</p>' in html
    assert '<a class="wikilink" href="/page/tip-9-1">the tip</a>' in html
    assert '<span class="wikilink broken">nowhere</span>' in html


def test_table():
    assert "<table>" in render("| a | b |\n|---|---|\n| 1 | 2 |\n", set())
```

- [ ] **Step 2: Check that they fail.** Expected: ImportError.

- [ ] **Step 3: Implement.** Snippets: at most 160 characters around the first match, with newlines collapsed.

- [ ] **Step 4: Run the tests.** Expected: all pass.

- [ ] **Step 5: Commit.** Message: `dashboard: relations (links in/out, suggestions, graphs, search) and markdown rendering`, with the trailer.

---

### Task 6: actions — generate, preview, run log

**Files:**
- Create: `dashboard/actions.py`, `dashboard/tests/test_actions.py`, `dashboard/tests/fake_make.py`

**Interfaces:**
- Produces:

```python
GENERATED_PATHS = ["_pages", "_posts", "_examples", "assets/images",
                   "docs-arc42-brain/_system/generated-assets.txt"]

@dataclass
class Job:
    kind: str                     # "generate" | "preview"
    started: str                  # ISO timestamp (local time, seconds)
    lines: list[str] = field(default_factory=list)
    finished: str | None = None
    exit_code: int | None = None
    stage: str | None = None      # "lint" | "generate" | "preview" — the step that decided the outcome
    summary: dict = field(default_factory=dict)
    def to_dict(self) -> dict     # all fields; lines trimmed to the last 200 as "tail"

class Runner:
    def __init__(self, repo: Path, make: str = "make",
                 braingen: str = f"{sys.executable} -m braingen.cli",
                 now=datetime.now): ...
    lock: threading.Lock
    current: Job | None           # running job
    last: Job | None              # most recent finished job
    def start(self, kind) -> tuple[Job, bool]   # (job, started); returns (current, False) when the lock is held; runs in a daemon thread
    def run(self, kind) -> Job                  # synchronous body used by the thread and by tests; caller holds no lock
    def parity(self) -> dict[str, str]          # cached result, {} if none
```

Behaviour:
- Commands run through `subprocess.run([...], cwd=repo, capture_output=True, text=True)`. Each command's output is appended to `job.lines`: first `$ <command>`, then stdout, then stderr.
- The make argv is `[make, "-C", str(repo), <target>, f"BRAINGEN={braingen}"]`.
- **generate:**
  1. Run `brain-lint`. If it exits non-zero: `stage = "lint"`, `exit_code` = its code, stop. There is no log line.
  2. Run `generate`. If it exits non-zero: `stage = "generate"`, the code, stop. There is no log line.
  3. Parse `(\d+) written, (\d+) deleted` from the output. `changed` = written + deleted, or 0 when absent. Put `summary["changed"] = changed`.
  4. Append to `docs-arc42-brain/_system/log.md`: first add newlines so the file ends with exactly one blank line, then `## [YYYY-MM-DD] generate | dashboard, N files changed\n`, with the date from `now()`.
  5. Put `summary["git_status"]` = stdout of `git -C repo status --short -- <GENERATED_PATHS>`, and `summary["git_diff_stat"]` = stdout of `git -C repo diff --stat -- <GENERATED_PATHS>`. Git failures leave the stderr text there.
  6. `exit_code = 0`, `stage = "generate"`.
- **preview:**
  1. Run `generate-check`, `stage = "preview"`, `exit_code` = its code.
  2. Parse `^section (\d+): (PASS|FAIL)` from the output into `{number: result}`.
  3. Write `docs-arc42-brain/build/dashboard/parity.json` as `{"at": iso, "sections": {...}}`. `summary["sections"]` gets the same dict.
  4. No log line.
- **Every job:** the full `lines` go to `docs-arc42-brain/build/dashboard/runs/<YYYYmmdd-HHMMSS>-<kind>.log`, and `summary["run_file"]` holds its repo-relative path. `finished` is set.
- **`start()`:**
  - If `lock.acquire(blocking=False)` fails, return `(self.current, False)`.
  - Otherwise create the Job, set `current`, and start a thread that calls the run body and in `finally` sets `last`, clears `current` and releases the lock.
  - Structure the code so the thread's body and `run()` share one implementation.

`tests/fake_make.py` provides `install(tmp_path, monkeypatch) -> Path` (the record file). It writes an executable `make` script into `tmp_path/"bin"` and prepends that directory to `PATH`.
- The script is a Python script with `#!` + `sys.executable`.
- It appends `json.dumps(sys.argv[1:])` as one line to the record file.
- The target is `argv[3]`.
- `brain-lint` prints `0 findings` and exits with `int(os.environ.get("FAKE_LINT_EXIT", 0))`. With a non-zero code it first prints `ERROR   x: boom`.
- `generate` prints `FAKE_GEN_LINES` (default 1) lines `wrote   f<i>.md`, then `2 written, 1 deleted, 5 unchanged`, and exits with `FAKE_GEN_EXIT`.
- `generate-check` prints `section 3: PASS (0 files compared)` and `section 9: FAIL (6 files compared)`, then exits 1.

- [ ] **Step 1: Write the failing tests.**

```python
import json
from datetime import datetime

import pytest

import fake_make
from actions import Runner

NOW = lambda: datetime(2026, 9, 18, 10, 30, 0)


@pytest.fixture
def runner(repo, tmp_path, monkeypatch):
    rec = fake_make.install(tmp_path, monkeypatch)
    r = Runner(repo, braingen="BG", now=NOW)
    r.record = rec
    return r


def calls(r):
    return [json.loads(l) for l in r.record.read_text().splitlines()]


def log_text(repo):
    return (repo / "docs-arc42-brain/_system/log.md").read_text()


def test_generate_success(runner, repo):
    job = runner.run("generate")
    assert [c[2] for c in calls(runner)] == ["brain-lint", "generate"]
    assert calls(runner)[0] == ["-C", str(repo), "brain-lint", "BRAINGEN=BG"]
    assert job.exit_code == 0 and job.stage == "generate" and job.summary["changed"] == 3
    assert log_text(repo).endswith("\n\n## [2026-09-18] generate | dashboard, 3 files changed\n")
    run_file = repo / job.summary["run_file"]
    assert run_file.name == "20260918-103000-generate.log" and "2 written" in run_file.read_text()


def test_lint_gates_generate(runner, repo, monkeypatch):
    monkeypatch.setenv("FAKE_LINT_EXIT", "1")
    before = log_text(repo)
    job = runner.run("generate")
    assert [c[2] for c in calls(runner)] == ["brain-lint"]
    assert job.stage == "lint" and job.exit_code == 1
    assert log_text(repo) == before


def test_failure_shape(runner, repo, monkeypatch):
    monkeypatch.setenv("FAKE_GEN_EXIT", "2")
    monkeypatch.setenv("FAKE_GEN_LINES", "300")
    before = log_text(repo)
    job = runner.run("generate")
    d = job.to_dict()
    assert d["exit_code"] == 2 and d["stage"] == "generate" and len(d["tail"]) == 200
    assert log_text(repo) == before
    assert "wrote   f0.md" in (repo / job.summary["run_file"]).read_text()


def test_preview_caches_parity_without_log(runner, repo):
    before = log_text(repo)
    job = runner.run("preview")
    assert job.summary["sections"] == {"3": "PASS", "9": "FAIL"}
    assert runner.parity() == {"3": "PASS", "9": "FAIL"}
    assert json.loads((repo / "docs-arc42-brain/build/dashboard/parity.json").read_text())["sections"]["9"] == "FAIL"
    assert log_text(repo) == before


def test_one_job_at_a_time(runner):
    runner.lock.acquire()
    try:
        from actions import Job
        runner.current = Job("generate", "t")
        job, started = runner.start("preview")
        assert started is False and job is runner.current
    finally:
        runner.lock.release()


def test_start_runs_in_background_and_releases(runner):
    job, started = runner.start("preview")
    assert started is True
    for _ in range(100):
        if runner.current is None:
            break
        import time; time.sleep(0.05)
    assert runner.current is None and runner.last.kind == "preview" and not runner.lock.locked()
```

- [ ] **Step 2: Check that they fail.** Expected: ImportError.

- [ ] **Step 3: Implement** `actions.py` and `tests/fake_make.py`.

- [ ] **Step 4: Run the tests.** Expected: all pass.

- [ ] **Step 5: Commit.** Message: `dashboard: actions — lint-gated generate, preview with parity cache, run files, log line`, with the trailer.

---

### Task 7: link check

**Files:**
- Create: `dashboard/linkcheck.py`, `dashboard/tests/test_linkcheck.py`

**Interfaces:**
- Produces:

```python
URL_RE = re.compile(r"https?://[^\s)<>\]\"'`|]+")
def external_urls(b) -> dict[str, list[str]]     # url (trailing .,;: stripped) -> sorted slugs; from bodies and string meta values
def head_status(url, timeout=10.0) -> dict       # {"status": int|None, "location": str|None, "error": str|None}; HEAD, no redirects followed
class LinkChecker:
    def __init__(self, cache_file: Path, fetch=head_status, clock=time.time, ttl=86400.0): ...
    running: bool
    def check(self, urls: dict[str, list[str]]) -> list[dict]  # synchronous; uses cache entries younger than ttl, fetches others (ThreadPoolExecutor, 8 workers); writes cache; returns results
    def start(self, urls) -> bool                              # background thread; False if already running
    def results(self) -> list[dict]                            # last results from the cache file, sorted
```

- **Result row:** `{"url", "status", "location", "error", "checked" (epoch float), "pages"}`.
- **Sort order:**
  1. failures: status None or ≥ 400;
  2. redirects: 3xx;
  3. the rest.

  Within each group, sort by url.
- **Cache file:** JSON `{url: {"status", "location", "error", "checked"}}`.
- **`head_status`:** `urllib.request` with a redirect handler that does not follow redirects. A 3xx comes back as its status and the `Location` header. Some servers reject HEAD with 405 or 403; on those, retry once with GET. Set `User-Agent: docs-arc42-brain-linkcheck`.

- [ ] **Step 1: Write the failing tests.**

```python
from linkcheck import LinkChecker, external_urls
from model import Model


def test_external_urls(repo):
    assert external_urls(Model(repo).get()) == {"https://adr.github.io/": ["tip-9-1"]}


def test_check_uses_cache_and_sorts(tmp_path):
    t = [1000.0]
    seen = []
    def fetch(url):
        seen.append(url)
        return {"https://ok": {"status": 200, "location": None, "error": None},
                "https://moved": {"status": 301, "location": "https://new", "error": None},
                "https://dead": {"status": None, "location": None, "error": "timeout"}}[url]
    lc = LinkChecker(tmp_path / "links.json", fetch=fetch, clock=lambda: t[0])
    urls = {"https://ok": ["a"], "https://moved": ["b"], "https://dead": ["c"]}
    rows = lc.check(urls)
    assert [r["url"] for r in rows] == ["https://dead", "https://moved", "https://ok"]
    assert rows[0]["pages"] == ["c"]
    t[0] += 3600; seen.clear(); lc.check(urls)
    assert seen == []
    t[0] += 86400; lc.check(urls)
    assert sorted(seen) == ["https://dead", "https://moved", "https://ok"]
```

- [ ] **Step 2: Check that they fail.** Then implement.
- [ ] **Step 3: Run the tests.** Expected: all pass.
- [ ] **Step 4: Commit.** Message: `dashboard: on-demand external link check with a one-day cache`, with the trailer.

---

### Task 8: pages — home tiles, lists, detail and the review pages

**Files:**
- Modify: `dashboard/app.py`, `dashboard/templates/base.html`, `dashboard/static/style.css`
- Create:
  - `templates/`: `_macros.html` (status bar, count, tile), `home.html` (replace), `sections.html`, `list.html` (tips/examples/terms/keywords/systems/faq), `page.html` (detail), `tags.html`, `issues.html`, `lint.html`, `log.html`, `review.html`, `cutover.html`, `gaps.html`;
  - `tests/test_pages.py`.

**Interfaces:**
- Consumes: Tasks 3–7. `create_app` builds these defaults unless they are injected:
  - `Model(repo)`;
  - `Presence()`;
  - `Runner(repo)`;
  - `LinkChecker(repo/"docs-arc42-brain/build/dashboard/links.json")`.

  All are stored in `app.extensions["brain"]`.
- Produces the routes listed in the test below. List pages accept query filters `status`, `section` (number) and `system` (slug).

Home tiles, in the order of dashboard spec §3.1:
- Sections, Tips, Examples, FAQ, Tags, Issues, Lint, Latest changes, Generate, Review queue, Cut-over readiness, Gaps, Link health.
- Each tile has a title linking to its page (FAQ has no link while it has zero pages), a primary count, and a status bar. The status bar is a stacked `<div class="bar">` with one `<span class="seg {status}" style="flex: N">` per status.
- Each tile has an open-issues flag where the spec asks for one.
- The Generate tile shows the last job's stage and exit code, plus a link to `/actions`.
- The Link health tile shows "not run yet" or the counts of failures, redirects and ok.

Styling:
- DESIGN.md tokens throughout: hairline panels, `--radius`, the deep-blue masthead, Signal Blue links, and `.callout.arc42-help` styled like the site's help box (help-bg / help-ink).
- Tiles sit in a CSS grid (`repeat(auto-fill, minmax(18rem, 1fr))`).
- Status colors: draft = muted, review = amber, published = emerald, retired = maroon.
- Layout works at phone width.

The detail page `/page/<slug>` shows:
- title, type, status;
- the front matter as a definition list;
- `render(body, set(vault.pages))`;
- links out and links in (with `via`);
- sources and issues naming the page;
- the obsidian link.

An unknown slug returns 404.

- [ ] **Step 1: Write the failing tests.**

```python
import pytest

PAGES = ["/", "/sections", "/tips", "/examples", "/faq", "/terms", "/keywords", "/systems", "/tags",
         "/issues", "/lint", "/log", "/review", "/cutover", "/gaps", "/page/tip-9-1", "/page/section-9"]


@pytest.mark.parametrize("path", PAGES)
def test_page_renders(client, path):
    assert client.get(path).status_code == 200


def test_home_has_every_tile(client):
    html = client.get("/").get_data(as_text=True)
    for title in ["Sections", "Tips", "Examples", "FAQ", "Tags", "Issues", "Lint", "Latest changes",
                  "Generate", "Review queue", "Cut-over readiness", "Gaps", "Link health"]:
        assert f">{title}<" in html, title
    assert "136 answers in faq.arc42.org, not yet ingested" in html


def test_list_filters(client):
    html = client.get("/tips?status=draft").get_data(as_text=True)
    assert "tip-9-2" in html and "tip-9-1" not in html


def test_detail(client):
    html = client.get("/page/tip-9-1").get_data(as_text=True)
    assert "ISS-001" in html and "obsidian://open?vault=docs-arc42-brain" in html
    assert 'href="/page/09-decision-example-x"' in html
    assert client.get("/page/nope").status_code == 404


def test_section_detail_renders_callout(client):
    html = client.get("/page/section-9").get_data(as_text=True)
    assert 'class="callout arc42-help"' in html and 'class="directive"' in html
```

- [ ] **Step 2: Check that they fail.** Then implement. Keep `app.py` to routes only (under 300 lines); the view data comes from `model` / `relations`.

- [ ] **Step 3: Run the tests.** Expected: all pass. Also run `wc -l app.py`. Expected: < 300.

- [ ] **Step 4: Commit.** Message: `dashboard: home tiles, list and detail pages, review/cut-over/gaps/lint/log/tags/issues pages`, with the trailer.

---

### Task 9: pages — actions, link health, suggestions, graph, search, reload

**Files:**
- Modify: `dashboard/app.py`, `dashboard/static/app.js`, `dashboard/static/style.css`, `dashboard/templates/base.html` (nav + search form)
- Create:
  - `templates/`: `actions.html`, `links.html`, `suggestions.html`, `graph.html`, `search.html`;
  - `static/graph.js`, `static/vendor/cytoscape.min.js` (copied from `/Users/gernotstarke/projects/arc42/eTSU/_system/apps/dashboard/static/vendor/cytoscape.min.js`, license header intact), `static/vendor/README.md` (source, version, MIT license);
  - `tests/test_actions_routes.py`.

**Interfaces:**
- Routes:
  - `GET /actions`: the page, showing:
    - buttons "Lint + generate" and "Preview (parity)";
    - the current or last job;
    - lint groups from `lint_view` when `stage == "lint"`;
    - `git_status` / `git_diff_stat`;
    - the parity table.
  - `POST /actions/generate` and `POST /actions/preview`, JSON `{client_id}`:
    - 403 `{"error": "only the facilitator can generate"}` unless `presence.is_facilitator(cid)`;
    - otherwise `runner.start(kind)` → 202 `{"started": bool, "job": job.to_dict()}`;
    - after a job that ends, the model cache is cleared (the Runner gets an `on_finish` callback, default None; `create_app` passes `model.clear`).
  - `GET /actions/job` → `{"current": dict|None, "last": dict|None}`.
  - `POST /actions/linkcheck` (anyone) → 202 `{"started": bool}`; `GET /links` renders the results.
  - `GET /suggestions`, `GET /graph?kind=links|terms`, `GET /graph.json?kind=links|terms`, `GET /search?q=`.
  - `POST /reload` → `model.clear()`, then redirect to the referrer or `/`.
- Front end:
  - Buttons carry `data-action="generate|preview"` and are disabled unless `document.body.dataset.facilitator === "yes"`. Beside them: "only the facilitator can generate".
  - Clicking one posts JSON with `window.brainClientId`, then polls `/actions/job` every second until `current` is null, and then reloads the page.
  - The graph page loads `vendor/cytoscape.min.js` and `graph.js`, fetches `/graph.json?kind=…` and draws it with layout `cose`. There is a filter by type (checkboxes) and edge width = weight for terms. Node colors by type come from the tokens.
- Nav in `base.html`:
  - links: Home, Sections, Tips, Examples, Tags, Issues, Review, Cut-over, Gaps, Suggestions, Graph, Actions, Links;
  - a search form (`GET /search`, input `q`);
  - a reload button (`POST /reload`).

- [ ] **Step 1: Write the failing tests** (`tests/test_actions_routes.py`). They use a stub runner.

```python
import pytest

from app import create_app
from actions import Job


class StubRunner:
    def __init__(self): self.current = None; self.last = None; self.started = []; self.on_finish = None
    def start(self, kind):
        self.started.append(kind); job = Job(kind, "t"); return job, True
    def parity(self): return {"9": "PASS"}


@pytest.fixture
def app_(repo):
    return create_app(repo, runner=StubRunner())


def test_generate_needs_facilitator(app_):
    c1, c2 = app_.test_client(), app_.test_client()
    c1.post("/ping", json={"client_id": "first"})
    c2.post("/ping", json={"client_id": "second"})
    r = c2.post("/actions/generate", json={"client_id": "second"})
    assert r.status_code == 403 and "facilitator" in r.get_json()["error"]
    r = c1.post("/actions/generate", json={"client_id": "first"})
    assert r.status_code == 202 and r.get_json()["started"] is True
    assert app_.extensions["brain"]["runner"].started == ["generate"]


def test_preview_and_job_status(app_):
    c = app_.test_client()
    c.post("/ping", json={"client_id": "f"})
    assert c.post("/actions/preview", json={"client_id": "f"}).status_code == 202
    assert c.get("/actions/job").get_json() == {"current": None, "last": None}


@pytest.mark.parametrize("path", ["/actions", "/links", "/suggestions", "/graph", "/graph?kind=terms",
                                  "/search?q=adr"])
def test_pages(app_, path):
    assert app_.test_client().get(path).status_code == 200


def test_graph_json_and_search(app_):
    c = app_.test_client()
    assert c.get("/graph.json?kind=terms").get_json()["edges"][0]["weight"] == 1
    assert "tip-9-1" in c.get("/search?q=adr.github").get_data(as_text=True)


def test_reload_and_linkcheck(app_, monkeypatch):
    c = app_.test_client()
    assert c.post("/reload").status_code in (302, 303)
    lc = app_.extensions["brain"]["linkchecker"]
    monkeypatch.setattr(lc, "start", lambda urls: True)
    assert c.post("/actions/linkcheck", json={}).get_json() == {"started": True}


def test_no_cdn_anywhere(app_):
    c = app_.test_client()
    for path in ["/", "/graph", "/actions"]:
        html = c.get(path).get_data(as_text=True)
        assert "https://" not in "".join(l for l in html.splitlines() if "<script" in l or "<link" in l)
```

- [ ] **Step 2: Check that they fail.** Then implement. `app.py` stays under 300 lines; move helpers into `model.py`/`relations.py` if needed.

- [ ] **Step 3: Run the full dashboard suite and `make brain-test`.** Expected: all pass.

- [ ] **Step 4: Commit.** Message: `dashboard: actions page (facilitator-gated generate/preview), link health, suggestions, graph, search, reload`, with the trailer.

---

### Task 10: end-to-end in Docker, docs, and the log

**Files:**
- Modify:
  - `docs-arc42-brain/README.md` and `docs-arc42-brain/CLAUDE.md` (commands);
  - `docs-arc42-brain/_system/index.md`, if it lists tooling;
  - `docs-arc42-brain/_system/log.md`: one entry `## [2026-09-18] report | dashboard (phase 3a)`, where the `report` kind notes a tooling milestone;
  - `docs/superpowers/specs/2026-09-18-docs-arc42-brain-dashboard-design.md`: status line → "implemented (phase 3a)", plus a short "Deviations" list: the module split from §6; the `BRAINGEN` override instead of uv inside the container; log line only on successful generate; `Finding.rule` in braingen.
- Create: `docs-arc42-brain/_system/dashboard/README.md` (run, test, architecture in ten lines).

- [ ] **Step 1: Run end to end against the real repo, in Docker.**
  1. `make dashboard-test` → all pass in the image.
  2. `make dashboard`, then:
     - `curl -sf localhost:4211/` and `/sections`, `/cutover`, `/lint`, `/graph.json` all return 200;
     - `curl -s -X POST -H 'content-type: application/json' -d '{"client_id":"e2e"}' localhost:4211/ping` shows `is_facilitator: true`;
     - `curl -s -X POST -H 'content-type: application/json' -d '{"client_id":"e2e"}' localhost:4211/actions/preview` → 202;
     - poll `/actions/job` until `current` is null → `last.summary.sections` has 12 entries, all "PASS".
  3. POST `/actions/generate` the same way and poll. Then:
     - `last.exit_code == 0` and `summary.changed == 0`, since section 9 is already generated;
     - `git status --short` shows exactly one change: `docs-arc42-brain/_system/log.md`, with the new generate line;
     - generated files are unchanged and owned by the host user.
  4. Revert that log line with `git checkout -- docs-arc42-brain/_system/log.md`. It came from the test run, not from real work.
  5. `make dashboard-down`.
  6. `make brain-test`, `make brain-lint`, `make brain-check-generated` → green.
- [ ] **Step 2: Write the docs** listed above.
- [ ] **Step 3: Commit.** Message: `dashboard: docs, spec status and deviations, log entry`, with the trailer.

Port 4211 must also be registered in `../meta.arc42.org/raw/port-assignment.md`. That is a different repository, so this plan does not do it; the final report lists it as an open item for the user.
