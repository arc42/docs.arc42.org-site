# Workflow: Relations

How links are proposed and promoted (ADR-0004).

- The site renders `related:` only.
- Candidates are computed (dashboard, phase 3) from: shared terms (weight 3),
  same subsection (weight 2), shared keywords (weight 1), same system for
  examples (weight 2). Until the dashboard exists, find them by reading.
- Promote a candidate by adding it to `related:` on the page, and on the
  target when the target is a tip, example, term or FAQ answer.
- Never link a page to itself, to its own section (the section link is
  `section:`), or to more than 8 targets; more than 8 means the page or the
  vocabulary is too coarse.
