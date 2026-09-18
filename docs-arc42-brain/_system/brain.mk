# docs-arc42-brain targets. Included from the root Makefile, so every path
# here is relative to the repo root, which is where make runs.
BRAIN_DIR := $(CURDIR)/docs-arc42-brain
BRAIN_GEN := $(BRAIN_DIR)/_system/generate
# --directory makes uv (and pytest) run inside the package folder, so the
# pyproject there is the project and `tests/` is found; vault/site paths passed
# to braingen are absolute, so the cwd change does not matter to them.
BRAINGEN  := uv run --directory $(BRAIN_GEN) braingen

.PHONY: brain-test brain-lint brain-raw brain-import generate generate-check brain-check-generated

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
