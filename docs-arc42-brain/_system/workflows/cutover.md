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
   generate` refuses to overwrite a file without the marker line, so this
   comes before step 4.
4. `make generate`. The files come back at the same paths, each with the
   marker line after the front matter, tips and examples with `related:`.
   Run it twice; the second run must print `0 written, 0 deleted`.
5. `make generate-check SECTION=N`, `make brain-test`, `make check`, `make
   check-links`.
6. Append a `cutover` entry to `_system/log.md`.
7. One commit: status flips, generated files, log. The diff shows per file:
   front-matter changes (tags, `related:`), the marker line, blank lines
   after the front matter — never a body change.
