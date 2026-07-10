.DEFAULT_GOAL := help

.PHONY: help dev build stop site check check-links clean install update shell logs

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

dev: ## Start the local Jekyll dev server with live reload (http://localhost:4000)
	@echo "==> Open http://localhost:4000  (NOT http://0.0.0.0:4000 — Firefox refuses to connect to 0.0.0.0)"
	docker compose up --build

build: ## Build the Docker dev image (docs-arc42-site:latest) from the Gemfile-pinned gems
	docker compose build

stop: ## Stop and remove the running dev container
	docker compose down

site: build ## Generate the static site into _site/
	docker compose run --rm jekyll bundle exec jekyll build

check: ## Build the site (via the running dev server) and run project sanity checks
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
