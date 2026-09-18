Plan and execute phase 2 of the docs-arc42-brain project, subagent-driven. First write the plan with the superpowers:writing-plans skill, let me review it, then execute it with superpowers:subagent-driven-development: one fresh subagent per task, spec review and code-quality review between tasks, a whole-branch review at the end. Do not start the dashboard (phase 3) in this session.

## Where things are

- Repo `/Users/gernotstarke/projects/arc42/docs.arc42.org-site`, branch `docs-arc42-brain` is checked out. Stay on it. Do not push unless I ask.
- Read first: `docs/superpowers/plans/2026-09-18-docs-arc42-brain-next-session-handover.md`. It lists the phase-1 state, the seven things phase 2 must respect (GFM anchors, synthetic headings, expected parity differences, `faqlink`, subsection links in `section:`, lint L13, fixtures first), and the execution conventions that worked.
- Brain spec: `docs/superpowers/specs/2026-09-17-docs-arc42-brain-design.md`. §2 decisions D1–D15 are final (D9 is revised by the dashboard spec, which is not this session's concern). Phase 2 is §6 (generator, emitters, parity check), §4.3–§4.5 (what the generator must emit, including `_includes/related.html` and its call in the article layout, the one hand-made site change allowed), §9 (make targets `generate`, `generate-check`), §10 (testing), §11 phase 2 exit: parity green on section 9, cut-over of section 9 ready to merge, live site unchanged except the related-links block and any tag consolidation the lint reports.
- Dashboard spec `docs/superpowers/specs/2026-09-18-docs-arc42-brain-dashboard-design.md`: read D19 and §4 only, so the generate and preview targets you build are the ones the dashboard will call later.
- Phase 1 is implemented: `braingen` package under `docs-arc42-brain/_system/generate/` (parse, lint, raw, import; 53 tests), twelve section pages as drafts, section 9 ingested with `status: review`. `make brain-test`, `make brain-lint`, `make check` are green.

## Plan shape I expect

- The first task adds real-page fixtures (sections 5, 10, 11) and a round-trip test importer → emitter → original, before any emitter exists (TDD at the integration level).
- Then: emitters for sections, tips, examples, assets; the generated-file marker; idempotent `make generate` that deletes stale generated files it owns; `make generate-check SECTION=N` parity with the documented expected differences; `_includes/related.html` plus the layout call; `make check` extended to run `brain-lint` and to fail on hand-edited generated files.
- Last: flip section 9's pages to `published`, generate, delete the hand-written originals of section 9, run `make check` and `make check-links`, and report what the PR diff will show. Do not open the PR or push; I decide that.
- Every task self-contained with full code and tests, checkboxes, global constraints section, one commit per task, plan file included in the commit.

## Constraints that are easy to violate

- Nothing outside `docs-arc42-brain/` and `docs/` changes except: `_includes/related.html` (new), one include line in the article layout, `brain-lint` in `make check`, and in the final task the generated files plus the deleted originals of section 9. Nothing else in `_layouts/`, `_includes/`, `_sass/`, `_data/`.
- No Liquid under `docs-arc42-brain/wiki/`; the generator introduces every `{% %}` and `{{ }}`.
- Generated files carry the marker comment after the front matter; `make generate` never touches files without it.
- Permalinks byte-identical (D3). Tags compared as sets after alias normalisation, differences printed, not failed.
- Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>` literally, whatever model the subagent runs as; implementers verify with `git log -1 --format=%B`. Explicit `git add <paths>`, never `git add -A`.
- Tooling: `uv` at `~/.local/bin/uv`; system python3 is 3.14, the package requires >=3.12. Docker is available for `make check`.

## Models

Plan and reviews on Opus. Implementers: Haiku when the plan text contains the complete code, Sonnet for integration tasks, Opus only for the cut-over task. Give every subagent the task brief file, the global-constraints file and a report path; never the whole plan.

## When done

Report: parity result per section (9 green; the expected differences on 7, 10, 11 confirmed as expected), what the section-9 PR diff contains, tag changes the lint reported, open issues, and what the dashboard plan (phase 3) must know first.
