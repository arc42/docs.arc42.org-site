# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jekyll-based static documentation site for the **arc42 software architecture template**. Published at https://docs.arc42.org via GitHub Pages. Content is written in Markdown with Liquid templates; styling uses SCSS.

## Build & Serve

```bash
make dev        # Start local dev server via Docker (port 4000)
make clean      # Remove generated _site directory
```

Alternative without Make: `docker compose up` (uses `bretfisher/jekyll-serve` image).

Native Ruby: `bundle install && bundle exec jekyll serve`.

Production deployment is automatic via GitHub Pages on push to `main`.

## Architecture

- **`_pages/`** — 12 arc42 documentation sections (`section-1.md` through `section-12.md`) plus meta pages (home, examples, contact). Layout: `arc42-doc-section`.
- **`_posts/`** — Tips and best practices, organized in subdirectories by section number (`01-requirements/`, `02-constraints/`, etc.). Filename pattern: `YYYY-MM-DD-t-[section]-[number].md`.
- **`_examples/`** — A Jekyll collection (`output: true` in `_config.yml`). Examples are named `[section-number]-[type]-example-[name].md` and dynamically included in section pages via `{% include example.md category="..." %}`.
- **`_layouts/`** — `default.html` is the main shell; `arc42-doc-section.html` wraps documentation sections.
- **`_includes/`** — Reusable fragments. `example.md` filters `site.examples` by category for dynamic inclusion.
- **`_sass/`** — SCSS partials compiled via `assets/css/style.scss`.
- **`images/`** — Content images referenced via `{{ site.imageurl }}` or `{{ site.exampleimages }}` (defined in `_config.yml`).
- **`originals/`** — Source diagram files (PlantUML, etc.), excluded from build.

## Content Conventions

- Section pages use `<div class="arc42-help">` for arc42 guidance blocks and `<div class="arc42-example">` for example blocks.
- Front matter fields: `layout`, `title`, `category`, `permalink`, `order` (nav ordering), `tags`.
- Image paths follow `images/[section-number]-[descriptive-name].png`.
- Interactive collapsible sections use Nutshell.js (`assets/js/nutshell.js`).

## Key Config

`_config.yml` uses `permalink: pretty`, kramdown with GFM input, and plugins: `jemoji`, `jekyll-sitemap`, `jekyll-seo-tag`, `jekyll-github-metadata`. The `_examples` collection has `output: true`.

## License

Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).
