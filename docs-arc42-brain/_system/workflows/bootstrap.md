# Workflow: Bootstrap

Run once on an empty vault. Not grill-gated: the content is already published.

1. For every section N in 1..12: `make brain-raw SECTION=N WHAT=page` then
   `make brain-import BATCH=section-N-page`. This creates the twelve section
   pages as drafts, with callouts and directives, and copies their images.
2. Create the featured keyword pages from `_templates/keyword.md`: `lean`,
   `essential`, `thorough` (`featured: true`), plus `example` and `tooling`
   (`featured: false`). Definitions come from how the site uses them today.
3. Create the system pages from `_templates/system.md`: `htmlsc` (HTML Sanity
   Checker, alias `hsc`), `tpu` (TrafficPursuitUnit), `mama`, `status`. Where
   the meaning of a slug is unclear, raise an issue rather than invent.
4. Move the twelve batches to `raw/ingested/` and set each `SRC` record's
   `origin:` to `raw/ingested/section-N-page/`.
5. Fill `_system/index.md` with one line per page and append a
   `## [YYYY-MM-DD] bootstrap | twelve section pages` entry to `_system/log.md`.
6. `make brain-lint` must pass with zero errors.
