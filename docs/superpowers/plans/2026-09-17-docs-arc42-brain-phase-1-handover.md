Execute phase 1 of the docs-arc42-brain project, subagent-driven. Use the superpowers:subagent-driven-development skill: one fresh subagent per task, spec review and code-quality review between tasks, then the next task. Do not start phase 2.

## Where things are

- Repo `/Users/gernotstarke/projects/arc42/docs.arc42.org-site`, branch `docs-arc42-brain` is checked out. Stay on it. Do not push unless I ask.
- Spec: `docs/superpowers/specs/2026-09-17-docs-arc42-brain-design.md`. Read §2 (decisions D1–D15, final, do not re-litigate), §3–§5, §8 and Appendix A before dispatching anything.
- Plan: `docs/superpowers/plans/2026-09-17-docs-arc42-brain-phase-1-foundation.md`. Ten tasks with checkbox steps, full code and test content. It is self-contained; subagents get the task text verbatim plus the "Global Constraints" section. Tick the checkboxes as tasks complete and include the plan file in that task's commit.
- Commits so far on the branch: `19eb0ec` spec, `ccef79e` plan. `_config.yml` already excludes `docs` and `docs-arc42-brain` from the Jekyll build.
- `docs-arc42-brain/` exists and is empty.

## Task shape

- Tasks 1–7 are code and schema documents: TDD as written in the plan, one commit per task, explicit `git add <paths>`, never `git add -A`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Task 8 (bootstrap) and Task 9 (pilot ingest of section 9) are content work. The subagent follows `docs-arc42-brain/_system/workflows/bootstrap.md` and `ingest.md`, which Task 7 writes. If the importer chokes on a real page in Task 8, that is a bug in Task 5 or 6: fix it with a failing test first, then rerun the bootstrap step.
- Task 10 runs `make brain-test`, `make brain-lint` and `make check` (Docker Jekyll build; fine to run) and reports the phase exit.

## Constraints that are easy to violate

- Nothing outside `docs-arc42-brain/` and `docs/` changes except one `include` line at the end of the root `Makefile` and a few `.gitignore` lines. Layouts, includes, SCSS, `_data/sections.yml`, `_pages/`, `_posts/`, `_examples/` stay untouched in phase 1.
- No Liquid anywhere under `docs-arc42-brain/wiki/`. Guidance is `> [!arc42-help]` callouts; directives are `%% examples: <category> %%` and `%% examples-link %%`.
- Natural IDs, wikilinks resolve by filename stem, wikilinks in YAML are quoted strings. English. Absolute dates.
- Tooling: `uv` is at `~/.local/bin/uv`; system `python3` is 3.14. The package requires `>=3.12`; if a dependency fails on 3.14, run `uv python pin 3.12` inside `docs-arc42-brain/_system/generate` and note it in the task report.
- Section pages are irregular (spec Appendix A): two help divs under one heading in section 5, a hard-coded image path in section 10, one examples-link for two subsections in section 3, guidance headings at H2 inside subsections in section 10. The importer keeps bodies verbatim apart from the documented rewrites; it does not normalise.

## When done

Report: pages by type, open issues, lint warnings and why each is deliberate, anything the phase-2 plan (generator with parity check on section 9, spec §6) must know first.
