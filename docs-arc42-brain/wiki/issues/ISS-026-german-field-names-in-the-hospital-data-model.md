---
id: ISS-026
type: issue
title: The hospital data model in tip 8-7 mixes German field names into an English example
status: open
created: '2026-09-21'
updated: '2026-09-21'
sources:
- '[[SRC-020-section-8-content]]'
related:
- '[[tip-8-7]]'
severity: minor
kind: gap
raised-by: agent
resolved: null
---

**What's unresolved.** [[tip-8-7]] shows a hospital data model and prints its full PlantUML source
— about sixty lines. The classes and most attributes are English, but five attributes are German:
`aufgenommen`, `allergie` and `aktuelleDiagnose` on `Patient`, `fachrichtung` and `approbation` on
`MedicalStaff`. Since the source is printed for the reader to reuse, the mixture is copied along
with it, and the tip sits in the section that documents the [[domain]] model — the one place where
consistent naming is the actual subject.

**Affects.** [[tip-8-7]].

**Evidence.** From the fenced PlantUML block: `class Patient { id: String {id} / name: String /
aufgenommen: Date / allergie: String[] / aktuelleDiagnose: Diagnosis[] }` and
`class MedicalStaff { fachrichtung: String[] / approbation: Boolean }`. Everything around them —
`Person`, `Hospital`, `Department`, `Contract`, `monthSalary`, `isUnlimited` — is English. The
diagram image is generated from this source, so the rendered picture carries the German words too.

**Options.**
1. Translate the five attributes (`admitted`, `allergies`, `currentDiagnosis`, `speciality`,
   `licenceToPractise`) at cut-over. The image would then have to be regenerated from the
   corrected source, which is exactly what the tip claims is easy — a useful demonstration that
   the claim holds.
2. Leave them: the model is illustrative, and `approbation` has no short English equivalent.
3. Keep the German and say so, since a German-speaking hospital domain is a legitimate choice —
   but then `Person`, `Staff` and `Contract` should be German too.

**Resolution.** Open. Option 1 is more work than a typo fix because of the image, which is why
this is its own issue rather than a line in
[[ISS-027-section-8-bodies-carry-editorial-defects|ISS-027]]. Related in spirit to
[[ISS-013-section-2-tip-bodies-carry-editorial-defects|ISS-013]]'s en-GB/en-US mixture, one level
up: not a spelling variant but two languages in one artefact.
