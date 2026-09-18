# docs-arc42-brain — handover for the next session

Written 2026-09-18 on branch `docs-arc42-brain` (unpushed). Read this first,
then the two specs, then decide which plan to write.

## State

- **Phase 1 is implemented and reviewed** (commits 7a62574..b87489c). Exit:
  53 tests, `make brain-lint` 0 errors / 33 deliberate warnings, `make check`
  green. Twelve section pages as drafts, section 9 ingested (10 tips, 3
  examples, 5 terms, 10 issues). Phase-1 report with rulings is in the chat
  history of the session that ran it; everything load-bearing is in commit
  messages, `_system/log.md`, and the `braingen.anchors` docstring.
- **Dashboard spec approved** in conversation on 2026-09-18:
  `docs/superpowers/specs/2026-09-18-docs-arc42-brain-dashboard-design.md`
  (D16–D23). It revises D9 of the brain spec.
- **Phase 2 is next** (generator with parity check on section 9, cut-over of
  section 9): brain spec §6, §11. No plan exists yet.
- Memory notes for Claude: `docs-arc42-brain-project` (phase-2 must-knows),
  `user-prefers-docker-no-local-installs`.

## What phase 2's plan must take into account (learned in phase 1)

1. Heading ids follow kramdown's **GFM** parser (`51-whitebox-overall-system`),
   implemented in `braingen.anchors.gfm_heading_id`; brain spec §4.3 was
   corrected. Include-injected headings (`Examples` at each `%% examples %%`
   directive; `Practical Tips`, `Related Questions`, `Complete Examples` at the
   foot) are `Heading(synthetic=True)` on section pages and must not be
   emitted.
2. Expected parity differences the check must accept, not fail on: section
   10's image path (`../assets/sections/10/…` back to `{{ site.imageurl }}`
   form), section 11's missing blank line after the front matter, section 7's
   duplicate `motivation` id (kramdown does not descend into `markdown="1"`
   divs; braingen keeps one global counter).
3. `faqlink` is not stored in the brain; it is
   `https://faq.arc42.org/category_c/#c-sec-N`. The foot is
   `{% include further-info.md category=… topic=… faqlink=… %}` from the
   section's `category` and `faq-topic`.
4. Subsection links live in `section:` with a heading
   (`[[section-9#Background (on ADRs)]]`), never in `related:`; the
   related-links renderer must render that link too.
5. Lint L13 (`legacy-tags` must be empty past draft) exempts type `term`.
6. First commit of phase 2: real-page fixtures (sections 5, 10, 11) under
   `_system/generate/tests/fixtures/` and a round-trip test importer → emitter
   → original. The final reviewer's throwaway inverter reproduced all twelve
   pages byte-for-byte; the emitter is that inverter made real.
7. Parked minors (all can wait): unscoped `__pycache__`/`.pytest_cache` in
   `.gitignore`; importer source-id `[:7]` fallback; lint has no guard for a
   leading-slash image path; `_posts_dir` required even for `WHAT=page`; no
   cleanup of a half-written raw batch; `wiki/systems/status.md` uses `url`
   for the homepage while the template says examples.arc42.org page; term
   back-links partial on `decision-criteria`, `stakeholder`,
   `quality-requirement`; exempting issue-typed sources from lint L9 is a
   `relations.md` decision.

## Execution conventions that worked

- Subagent-driven: one fresh implementer per task (Haiku for verbatim
  transcription tasks, Sonnet for integration, Opus for content judgment),
  Sonnet reviewers, Opus for the final whole-branch review.
- Every commit trailer literally `Co-Authored-By: Claude Fable 5.1
  <noreply@anthropic.com>` regardless of the subagent's model; two commits
  had to be amended for this. Put it in the constraints file and have
  implementers verify with `git log -1 --format=%B`.
- Tick plan checkboxes only within the task's own heading range; a bulk
  replace once ticked other tasks' steps.
- Explicit `git add <paths>`, never `-A`. Nothing outside `docs-arc42-brain/`
  and `docs/` changes.

## Suggested next steps

1. Push the branch or merge phase 1 to `main` (human decision; nothing has
   been pushed).
2. Write the phase-2 plan (writing-plans skill) from brain spec §6 plus the
   seven points above.
3. Execute it subagent-driven.
4. Then write the dashboard plan from the dashboard spec (D19) and execute
   it; register port 4211 in `meta.arc42.org/raw/port-assignment.md`.
