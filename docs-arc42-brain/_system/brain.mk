# docs-arc42-brain targets. Included from the root Makefile, so every path
# here is relative to the repo root, which is where make runs.
BRAIN_DIR := $(CURDIR)/docs-arc42-brain
BRAIN_GEN := $(BRAIN_DIR)/_system/generate
# --directory makes uv (and pytest) run inside the package folder, so the
# pyproject there is the project and `tests/` is found; vault/site paths passed
# to braingen are absolute, so the cwd change does not matter to them.
BRAINGEN  := uv run --directory $(BRAIN_GEN) braingen

.PHONY: brain-test brain-lint

brain-test: ## Run the braingen unit tests
	uv run --directory $(BRAIN_GEN) pytest -q

brain-lint: ## Validate the brain: schema, links, anchors, images, no Liquid
	$(BRAINGEN) lint $(BRAIN_DIR)
