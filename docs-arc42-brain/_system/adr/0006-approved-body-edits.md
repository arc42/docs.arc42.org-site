# ADR-0006: Corrections to published bodies are approved one at a time, against a diff

- **Status:** accepted
- **Date:** 2026-09-23

## Context
The brain exists so that the project owns its content and can fix it. Until now it could not
fix a single word.

`tests/test_parity.py::test_parity_against_the_ingested_originals` compares every ingested
section against the immutable copy in `raw/ingested/`. Its own docstring says why it matters:
"This is the only guard that survives cut-over. Once a section is published, `make
generate-check` compares the generated site files with themselves and passes whatever the
emitters do; the raw batch is the last copy of the hand-written original outside git history."

That guard cannot tell a deliberate correction from an emitter regression — both are "the body
no longer matches the original". So every queued content fix was blocked by it:
ISS-002 (the ADR table), ISS-035 (a link to the wrong section), ISS-036 (a published TODO and
an untranslated paragraph), ISS-041 (a sequence diagram that contradicts itself), and the
roughly ninety editorial corrections of ISS-044. Deleting or weakening the guard would unblock
them at the price of the only thing standing between a future emitter bug and the site's text.

## Decision
A body edit to a page the brain publishes is **approved one change at a time, by a human who
has seen the diff**, and the approval is recorded in `_system/approved-body-edits.tsv`:

```
<site path>	<sha256 of the normalised new body>	<ISS-NNN>	<date>	<reason>
```

The file is append-only, like `_system/published-permalinks.txt` and
`_system/retired-permalinks.txt`, and is never edited by hand. Approvals are granted by

```
make brain-approve-edit REL=_pages/section-9.md ISSUE=ISS-002 REASON="…"      # shows the diff
make brain-approve-edit REL=… ISSUE=… REASON="…" YES=1                        # records it
```

Without `YES=1` the command prints the unified diff from the ingested original to the body that
would be published, and records nothing. The comparison then reports an approved difference as
a note naming the issue, instead of failing.

**The fingerprint is what makes this per-change rather than per-file.** A line exempts one
version of one page. A later edit to the same page produces a different body, so its
fingerprint no longer matches and the guard fails again until that edit is approved in its
turn. Front matter, tags, the further-info foot and every other page are still compared
exactly as before; only the one approved body is excused, and only while it stays that body.

The fingerprint is taken after the same normalisation the comparison applies — foot removed,
trailing whitespace and leading/trailing blank lines normalised — so reflowing a paragraph does
not force a re-approval for a change no reader sees.

## Consequences
The brain can correct its own content, which is what it was built for, and the guard keeps
working for everything else. Approvals accumulate: the register is a reviewable list of every
deliberate change made to published text since ingest, each naming the issue that decided it,
which is a record the project did not have before.

The cost is one command per correction. A large pass such as ISS-044's would produce one
register line per edited page — which is the right granularity, because the register is then
exactly the list of pages whose text the project has changed, and re-reading it is how a
reviewer checks that pass without re-reading the whole vault.

Rejected alternatives: dropping the body comparison after cut-over (loses the only guard that
survives cut-over); re-snapshotting `raw/ingested/` on every edit (destroys the last copy of
the hand-written original, and `raw/` is immutable by ADR-0002's three-layer split).
