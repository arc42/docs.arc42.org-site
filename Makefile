.DEFAULT_GOAL := help

# This site's fixed local dev port. Every arc42 site has its own so their dev
# servers can run side by side; see raw/port-assignment.md in meta.arc42.org.
# Changing it here is not enough: docker-compose.yml and the Dockerfile pass
# the same number to Jekyll so its startup banner names the real port.
SITE_PORT ?= 4210

.PHONY: help dev build stop site check check-links clean install update shell logs

# One group per makefile, targets in file order. awk reads each file itself,
# so no file-name prefix leaks into the output (grep over several files adds one).
HELP_AWK = awk 'BEGIN {FS = ":[^\#]*\#\# "} /^[a-zA-Z_-]+:.*\#\# / {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

help: ## Show this help
	@printf '\nSite (Jekyll, runs in Docker):\n'
	@$(HELP_AWK) Makefile
	@printf '\nBrain (docs-arc42-brain, runs via uv):\n'
	@$(HELP_AWK) docs-arc42-brain/_system/brain.mk
	@echo

dev: ## Start the local Jekyll dev server with live reload (http://localhost:4210)
	@echo "==> Open http://localhost:$(SITE_PORT)  (NOT http://0.0.0.0:$(SITE_PORT) — Firefox refuses to connect to 0.0.0.0)"
	@holder=$$(docker ps --filter "publish=$(SITE_PORT)" --format '{{.Names}}'); \
	if [ -n "$$holder" ]; then \
		echo "==> Port $(SITE_PORT) is already in use by another container: $$holder"; \
		echo "==> That's likely a dev server from a sibling arc42 site repo. Stop it first, e.g.:"; \
		echo "==>   docker stop $$holder"; \
		exit 1; \
	fi
	docker compose up --build

build: ## Build the Docker dev image (docs-arc42-site:latest) from the Gemfile-pinned gems
	docker compose build

stop: ## Stop and remove the running dev container
	docker compose down

site: build ## Generate the static site into _site/
	docker compose run --rm jekyll bundle exec jekyll build

check: brain-lint brain-check-generated ## Lint the brain, check generated files, build the site and run sanity checks
	sh scripts/check-site.sh

check-links: site ## Validate internal links, images, and HTML in the built _site (html-proofer)
	docker compose run --rm jekyll bundle exec htmlproofer ./_site --disable-external --allow-hash-href

clean: ## Remove generated _site AND the Docker cache volumes (a true reset)
	rm -rf _site .sass-cache .jekyll-cache .jekyll-metadata
	@# .jekyll-cache/.sass-cache live in named Docker volumes, not on the host,
	@# so a host rm alone leaves them stale — wipe the volumes too.
	-docker compose down -v --remove-orphans

install: build ## Install/refresh gems into the dev image after editing the Gemfile
	docker compose run --rm jekyll bundle install

update: build ## Update gems to their latest allowed versions (rewrites Gemfile.lock)
	docker compose run --rm jekyll bundle update

shell: build ## Open a shell inside the dev container for debugging
	docker compose run --rm jekyll bash

logs: ## Tail logs from the running dev container
	docker compose logs -f jekyll

# docs-arc42-brain: parser, lint, importer, generator. See docs-arc42-brain/README.md
include docs-arc42-brain/_system/brain.mk
