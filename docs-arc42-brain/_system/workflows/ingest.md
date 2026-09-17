# Workflow: Ingest

Turn one raw batch into typed, linked wiki pages. For the bootstrap of
existing site content this is audit-style: type, link, flag. Grilling is
reserved for new content and for the FAQ merge.

1. **Batch.** `make brain-raw SECTION=N WHAT=content` (the section page already
   exists from bootstrap; use `WHAT=all` only when it does not). Confirm the
   batch under `raw/section-N-content/`.
2. **Import.** `make brain-import BATCH=section-N-content`. Every tip and
   example now exists as a draft with `legacy-tags` filled and a `SRC` record.
3. **Read.** Read every imported page. Note near-duplicates, outdated
   statements, dead external links, statements that contradict a section page.
4. **Vocabulary.** For every entry in `legacy-tags` on every page: decide
   keyword or term. Existing page: reference it (`keywords: ["[[lean]]"]`,
   `terms: ["[[decision]]"]`). Missing: create it from the template with a
   real definition and `home`. Ambiguous or near-duplicate of an existing
   term: add it to that term's `legacy-tags`/`aliases` and reference the term;
   when unsure raise an issue. Empty `legacy-tags` when done.
5. **Links.** Fill `related:` on every page. Look for: tips of the same
   section that build on each other, the example that shows what the tip
   says, the subsection the tip elaborates (link by heading), the term the
   tip is about. Add the reverse link on tips, examples and terms; not on
   sections.
6. **Issues.** One `ISS-NNN` page per finding from step 3, `related:` to every
   affected page.
7. **Status.** Set `status: review` on every page whose `legacy-tags` is
   empty and whose `related` is filled.
8. **Bookkeeping.** Update `_system/index.md`; append to `_system/log.md`:
   `## [YYYY-MM-DD] ingest | section N content`, listing pages created,
   terms/keywords created, issues raised. Move the batch to `raw/ingested/`
   and update the `SRC` record's `origin:`.
9. **Gate.** `make brain-lint` must report zero errors. Warnings about
   reciprocity are allowed but should be deliberate.

Quality bar: a section's ingest that creates no term page and raises no
issue has almost certainly under-read the content.
