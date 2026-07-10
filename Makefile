.PHONY: help clean dev check

help: ## Show available targets
	@printf "Available targets:\n"
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z_-]+:.*## / { printf "  %-8s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

clean: ## Remove generated _site directory
	rm -rf _site

dev: ## Start the local Jekyll dev server via Docker on port 4000
	docker compose up

check: ## Build the site and run verbose sanity checks
	sh scripts/check-site.sh
