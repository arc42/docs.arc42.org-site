# Index

One line per page, grouped by type. Updated on every ingest.

## Sections

- [section-1](../wiki/sections/section-1.md) — 1 - Introduction and Goals
- [section-2](../wiki/sections/section-2.md) — 2 - Constraints
- [section-3](../wiki/sections/section-3.md) — 3 - Context and scope
- [section-4](../wiki/sections/section-4.md) — 4 - Solution strategy
- [section-5](../wiki/sections/section-5.md) — 5 - Building block view
- [section-6](../wiki/sections/section-6.md) — 6 - Runtime view
- [section-7](../wiki/sections/section-7.md) — 7 - Deployment view
- [section-8](../wiki/sections/section-8.md) — 8 - Concepts
- [section-9](../wiki/sections/section-9.md) — 9 - Architecture decisions
- [section-10](../wiki/sections/section-10.md) — 10 - Quality
- [section-11](../wiki/sections/section-11.md) — 11 - Risks and technical debt
- [section-12](../wiki/sections/section-12.md) — 12 - Glossary

## Tips

- [tip-2-1](../wiki/tips/tip-2-1.md) — Consider the constraints of other systems within the organization!
- [tip-2-2](../wiki/tips/tip-2-2.md) — Clarify the consequences of constraints!
- [tip-2-3](../wiki/tips/tip-2-3.md) — Document organizational constraints!
- [tip-2-4](../wiki/tips/tip-2-4.md) — Document design and development constraints!
- [tip-2-5](../wiki/tips/tip-2-5.md) — Differentiate different categories of constraints!
- [tip-9-1](../wiki/tips/tip-9-1.md) — Document only architecturally relevant decisions!
- [tip-9-2](../wiki/tips/tip-9-2.md) — Document decision criteria!
- [tip-9-3](../wiki/tips/tip-9-3.md) — Provide reasons for important decisions!
- [tip-9-4](../wiki/tips/tip-9-4.md) — Document decisions as mind-map or as table!
- [tip-9-5](../wiki/tips/tip-9-5.md) — Document decisions as `Architecture Decision Record` (ADR)!
- [tip-9-6](../wiki/tips/tip-9-6.md) — Document rejected alternatives!
- [tip-9-7](../wiki/tips/tip-9-7.md) — Document decisions informally as a blog (RSS-feed)!
- [tip-9-8](../wiki/tips/tip-9-8.md) — Decisions should have a timestamp!
- [tip-9-9](../wiki/tips/tip-9-9.md) — Follow the _suggestions for good ADRs_
- [tip-9-10](../wiki/tips/tip-9-10.md) — Use lightweight tooling to support creation of ADRs

## Examples

- [02-constraint-example-1](../wiki/examples/02-constraint-example-1.md) — HTML Sanity Checker
- [09-decision-example-adr](../wiki/examples/09-decision-example-adr.md) — Use ADRs in Nygard format
- [09-decision-example-htmlsc-1](../wiki/examples/09-decision-example-htmlsc-1.md) — HTML Sanity Checker
- [09-decision-example-tpu-2](../wiki/examples/09-decision-example-tpu-2.md) — TrafficPursuitUnit

## Terms

- [constraint](../wiki/terms/constraint.md) — Constraint
- [architecture-decision](../wiki/terms/architecture-decision.md) — Architecture decision
- [adr](../wiki/terms/adr.md) — Architecture Decision Record (ADR)
- [decision-criteria](../wiki/terms/decision-criteria.md) — Decision criteria
- [stakeholder](../wiki/terms/stakeholder.md) — Stakeholder
- [quality-requirement](../wiki/terms/quality-requirement.md) — Quality requirement

## Keywords

- [lean](../wiki/keywords/lean.md) — The minimal version of a practice: what to do when time is short
- [essential](../wiki/keywords/essential.md) — The practice arc42 considers indispensable for a usable documentation
- [thorough](../wiki/keywords/thorough.md) — The extended version of a practice for teams that can afford rigour
- [example](../wiki/keywords/example.md) — The page shows a worked example rather than guidance
- [tooling](../wiki/keywords/tooling.md) — The page is about tools that support the practice

## Systems

- [htmlsc](../wiki/systems/htmlsc.md) — HTML Sanity Checker
- [tpu](../wiki/systems/tpu.md) — TrafficPursuitUnit
- [mama](../wiki/systems/mama.md) — MaMa
- [status](../wiki/systems/status.md) — status.arc42.org

## Issues

- [ISS-001](../wiki/issues/ISS-001-quality-tag-on-tips-9-1-and-9-4.md) — open, ambiguity: does the legacy tag `quality` on tips 9-1 and 9-4 mean the arc42 quality requirement?
- [ISS-002](../wiki/issues/ISS-002-adr-structure-omits-timestamp-and-criteria.md) — open, contradiction: the ADR structure proposed in section 9 omits timestamp and decision criteria
- [ISS-003](../wiki/issues/ISS-003-pugh-matrix-link-leads-to-unrelated-site.md) — open, risk: the Pugh matrix link in tip 9-2 now leads to an unrelated site
- [ISS-004](../wiki/issues/ISS-004-external-links-redirect.md) — open, risk: three external links in the section 9 content redirect
- [ISS-005](../wiki/issues/ISS-005-tip-9-2-table-markup-broken.md) — open, gap: the second criteria table in tip 9-2 has an invalid separator row
- [ISS-006](../wiki/issues/ISS-006-cross-tip-references-are-hard-coded-urls.md) — open, gap: tips reference other tips by hard-coded site URL (sections 9 and 2)
- [ISS-007](../wiki/issues/ISS-007-legacy-raw-html-in-imported-bodies.md) — open, gap: imported bodies carry legacy raw HTML (sections 9 and 2)
- [ISS-008](../wiki/issues/ISS-008-tips-9-8-and-9-9-overlap-on-timestamps.md) — open, question: tip 9-8 is contained in the quotation of tip 9-9
- [ISS-009](../wiki/issues/ISS-009-examples-start-at-different-heading-levels.md) — open, gap: the three decision examples start at different heading levels
- [ISS-010](../wiki/issues/ISS-010-terms-cannot-leave-draft-with-legacy-tags.md) — resolved 2026-09-17, contradiction: term pages cannot leave draft because the lint forbids legacy-tags — L13 now exempts type `term`
- [ISS-011](../wiki/issues/ISS-011-external-link-rewrite-deferred.md) — open, contradiction: the generator does not rewrite external markdown links (spec §4.4) because section 9's parity depends on them staying plain
- [ISS-012](../wiki/issues/ISS-012-section-2-asks-for-tables-but-the-example-is-a-list.md) — open, contradiction: section 2 asks for tables of constraints while its only example is a plain bullet list
- [ISS-013](../wiki/issues/ISS-013-section-2-tip-bodies-carry-editorial-defects.md) — open, gap: the section 2 tip bodies carry a typo and mix British and American spelling
- [ISS-014](../wiki/issues/ISS-014-no-example-for-organizational-constraints.md) — open, gap: section 2 has no example of organizational or political constraints

## Sources

- [SRC-001](../raw/sources/SRC-001-section-1-page.md) — section-1-page
- [SRC-002](../raw/sources/SRC-002-section-2-page.md) — section-2-page
- [SRC-003](../raw/sources/SRC-003-section-3-page.md) — section-3-page
- [SRC-004](../raw/sources/SRC-004-section-4-page.md) — section-4-page
- [SRC-005](../raw/sources/SRC-005-section-5-page.md) — section-5-page
- [SRC-006](../raw/sources/SRC-006-section-6-page.md) — section-6-page
- [SRC-007](../raw/sources/SRC-007-section-7-page.md) — section-7-page
- [SRC-008](../raw/sources/SRC-008-section-8-page.md) — section-8-page
- [SRC-009](../raw/sources/SRC-009-section-9-page.md) — section-9-page
- [SRC-010](../raw/sources/SRC-010-section-10-page.md) — section-10-page
- [SRC-011](../raw/sources/SRC-011-section-11-page.md) — section-11-page
- [SRC-012](../raw/sources/SRC-012-section-12-page.md) — section-12-page
- [SRC-013](../raw/sources/SRC-013-section-9-content.md) — section-9-content
- [SRC-014](../raw/sources/SRC-014-section-2-content.md) — section-2-content

## Architecture Decisions (ADR)
- [ADR-0001](adr/0001-record-architecture-decisions.md) — Record decisions about the brain as ADRs
- [ADR-0002](adr/0002-content-types-and-natural-ids.md) — Nine content types with natural IDs
- [ADR-0003](adr/0003-two-vocabularies.md) — Terms and keywords are separate vocabularies
- [ADR-0004](adr/0004-explicit-related-links.md) — The site renders only explicit related links
- [ADR-0005](adr/0005-no-liquid-callouts-and-directives.md) — No Liquid in the brain; callouts and directives instead
