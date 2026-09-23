# docs-arc42-brain targets. Included from the root Makefile, so every path
# here is relative to the repo root, which is where make runs.
BRAIN_DIR := $(CURDIR)/docs-arc42-brain
BRAIN_GEN := $(BRAIN_DIR)/_system/generate
# --directory makes uv (and pytest) run inside the package folder, so the
# pyproject there is the project and `tests/` is found; vault/site paths passed
# to braingen are absolute, so the cwd change does not matter to them.
BRAINGEN  := uv run --directory $(BRAIN_GEN) braingen

.PHONY: brain-test brain-lint brain-raw brain-import generate generate-check brain-check-generated \
        brain-approve-edit \
        dashboard dashboard-down dashboard-logs dashboard-test

brain-test: ## Run the braingen unit tests
	uv run --directory $(BRAIN_GEN) pytest -q

brain-lint: ## Validate the brain: schema, links, anchors, images, no Liquid
	$(BRAINGEN) lint $(BRAIN_DIR)

SECTION ?=
WHAT ?= all

brain-raw: ## Copy a section's site files into raw/ (SECTION=9 WHAT=all|page|content)
	@test -n "$(SECTION)" || { echo "usage: make brain-raw SECTION=9 [WHAT=all|page|content]"; exit 2; }
	$(BRAINGEN) raw --site $(CURDIR) --vault $(BRAIN_DIR) --section $(SECTION) --what $(WHAT)

BATCH ?=

brain-import: ## Convert a raw batch into draft wiki pages (BATCH=section-9-all)
	@test -n "$(BATCH)" || { echo "usage: make brain-import BATCH=section-9-all"; exit 2; }
	$(BRAINGEN) import --vault $(BRAIN_DIR) --batch $(BATCH)

PARITY_DIR := $(BRAIN_DIR)/build/parity

generate: ## Write the Jekyll files of all published brain pages (lints first)
	$(BRAINGEN) generate --vault $(BRAIN_DIR) --site $(CURDIR)

generate-check: ## Parity: brain vs. site into build/parity/ (SECTION=9, default: all)
	$(BRAINGEN) generate-check --vault $(BRAIN_DIR) --site $(CURDIR) --out $(PARITY_DIR) $(if $(SECTION),--section $(SECTION))

brain-check-generated: ## Fail if a generated file was hand-edited or is stale
	$(BRAINGEN) check-generated --vault $(BRAIN_DIR) --site $(CURDIR)

REL ?=
ISSUE ?=
REASON ?=
YES ?=

brain-approve-edit: ## Show an edit to a published body as a diff; record it with YES=1 (ADR-0006)
	@test -n "$(REL)" && test -n "$(ISSUE)" && test -n "$(REASON)" || { \
		echo 'usage: make brain-approve-edit REL=<site path> ISSUE=ISS-NNN REASON="one line" [YES=1]'; \
		echo 'e.g.:  make brain-approve-edit REL=_pages/section-9.md ISSUE=ISS-002 REASON="ADR table gains a Date row"'; \
		echo '       ... then re-run the same line with YES=1 to record it'; \
		exit 2; }
	@$(BRAINGEN) approve-edit --vault $(BRAIN_DIR) --rel '$(REL)' --issue '$(ISSUE)' --reason '$(REASON)' $(if $(YES),--yes)

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
