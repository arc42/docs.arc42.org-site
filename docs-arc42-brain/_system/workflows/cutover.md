# Workflow: Cut-over

One section per PR (D10). Preconditions: the section page, every tip in its
`posts-dir` and every example its directives name have brain pages; `make
brain-lint` reports 0 errors.

1. `make generate-check SECTION=N` must print `PASS` and no `not ingested`
   note. Read every note: tag changes per page and `keyword page loses/gains
   tags` go into the PR description; any other difference is a bug in the
   brain page or the generator, never something to accept.
2. Set `status: published` and `updated:` to today on the section page, its
   tips and its examples. Terms, keywords and systems keep their status; they
   are not pages on the site.
3. Delete the hand-written originals: `_pages/section-N.md`,
   `_posts/<posts-dir>/*.md`, and the section's `_examples/*.md`. `make
   generate` refuses to overwrite a file whose front matter does not end
   with the marker comment, so this comes before step 4.
4. `make generate`. The files come back at the same paths, each with the
   marker (`# generated from docs-arc42-brain/… — do not edit`) as the last
   front-matter line, tips and examples with `related:`.
   Run it twice; the second run must print `0 written, 0 deleted`. The first
   run records the section's URLs in `_system/published-permalinks.txt`
   (`recorded N new permalinks`); commit that file with the cut-over.
5. `make generate-check SECTION=N`, `make brain-test`, `make check`, `make
   check-links`. After cut-over, `make generate-check SECTION=N` only compares
   the generated files with themselves (brain and site now match by
   construction); the regression guard for the emitters is the pytest
   integration test against `raw/ingested/` (`tests/test_parity.py`
   `test_parity_against_the_ingested_originals`). It needs nothing from you:
   the parametrisation is discovered from the `section-N-content` batches, so
   an ingested section is covered from the moment its batch lands in
   `raw/ingested/`, and the expected file count is read from the batch
   manifests. If it fails for a section you did not touch, an emitter changed
   and the diff it prints is the regression.
6. Append a `cutover` entry to `_system/log.md`.
7. One commit: status flips, generated files, log. The diff shows per file:
   front-matter changes (tags, `related:`, the marker comment as the last
   front-matter line), blank lines after the front matter — no marker in the
   body, never a body change.

## After cut-over: URLs are permanent

`_system/published-permalinks.txt` lists every URL `make generate` has
published; it is append-only. `make generate` stops, and `make check` fails,
when a recorded URL would no longer be served — a page set back to `draft`,
retired, or given a different `permalink`. The site has no redirect plugin, so
a dropped URL is a 404 for everyone who cited it. If a URL really has to go,
add `<permalink><TAB><reason>` to `_system/retired-permalinks.txt` (the reason
names the issue that decided it) in the same commit.
