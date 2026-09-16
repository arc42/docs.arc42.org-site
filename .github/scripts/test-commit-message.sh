#!/bin/sh
# Tests .github/trainings-commit-message.jq against the fixtures next to this
# script. Run it from anywhere; it exits non-zero on the first mismatch.
#
#   .github/scripts/test-commit-message.sh
#
# TODAY is pinned so the ended/removed split (a comparison against today) is
# reproducible - that is why the jq program takes the date as a parameter
# instead of calling `now`.
set -u

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROGRAM="$HERE/../trainings-commit-message.jq"
FIXTURES="$HERE/fixtures"
TODAY=2026-06-01

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT INT TERM

generate() {
  jq -n -r --arg today "$TODAY" \
    --slurpfile old "$FIXTURES/$1-old.json" \
    --slurpfile new "$FIXTURES/$1-new.json" \
    -f "$PROGRAM"
}

fail() {
  printf 'FAIL - %s\n' "$1" >&2
  shift
  printf '%s\n' "$@" >&2
  exit 1
}

# assert_output <name> <fixture prefix> <<'EOF' ... EOF
assert_output() {
  name=$1
  fixture=$2
  cat > "$tmp/expected"
  if ! generate "$fixture" > "$tmp/actual" 2> "$tmp/stderr"; then
    fail "$name" "generator exited non-zero:" "$(cat "$tmp/stderr")"
  fi
  if ! diff -u "$tmp/expected" "$tmp/actual" > "$tmp/diff"; then
    fail "$name" "--- expected / +++ actual" "$(cat "$tmp/diff")"
  fi
  printf 'ok - %s\n' "$name"
}

# The subject is a git subject line: one line, 72 characters at most.
assert_subject_fits() {
  fixture=$1
  generate "$fixture" > "$tmp/message"
  subject=$(head -n 1 "$tmp/message")
  length=$(printf '%s' "$subject" | wc -m | tr -d ' ')
  if [ "$length" -gt 72 ]; then
    fail "subject over budget for fixture $fixture" "got $length: $subject"
  fi
  if [ -n "$(sed -n '2p' "$tmp/message")" ]; then
    fail "subject is not a single line for fixture $fixture" "$(cat "$tmp/message")"
  fi
  printf 'ok - %s\n' "$fixture subject fits: $length chars, one line"
}

assert_output "a new date is announced with its dates, place and language" added <<'EOF'
chore: new date 27-10 ADOC-EN, 2027-10-12

- added    27-10 ADOC-EN (adoc-oct-2027), 2027-10-12 to 2027-10-13, online, en
EOF

assert_output "seats_limited false->true reads as a sentence, not a boolean" seats <<'EOF'
chore: 26-09 Req4Arc — few seats left

- updated  26-09 Req4Arc (req4arc-sep-2026): few seats left
EOF

# The point of the whole exercise: an expired date and a withdrawn one look
# identical in the payload and mean opposite things.
assert_output "an expired date reads 'ended', a withdrawn future date 'removed'" gone <<'EOF'
chore: 2 training changes (MSA)

- removed  27-06 MSA-EN (msa-06-2027)
- ended    25-11 MSA (msa-nov-2025) — past
EOF

gone_output=$(generate gone)
case "$gone_output" in
  *"- removed  27-06 MSA-EN"*) ;;
  *) fail "withdrawn date must not be called 'ended'" "$gone_output" ;;
esac
case "$gone_output" in
  *"- ended    25-11 MSA"*) ;;
  *) fail "expired date must not be called 'removed'" "$gone_output" ;;
esac
printf 'ok - %s\n' "the two words are distinct"

assert_output "several changes across two courses name both courses" multi <<'EOF'
chore: 3 training changes (MSA, ADOC)

- added    28-01 MSA (msa-jan-2028), 2028-01-10 to 2028-01-13, Köln, de
- updated  26-12 MSA (msa-dez-2026): status full
- updated  27-10 ADOC-EN (adoc-oct-2027): moved to 2027-11-02, now ends 2027-11-03
EOF

assert_output "no changes still yields the generic subject, never an empty one" nochange <<'EOF'
chore: refresh training dates from trainings.arc42.org
EOF

# pricing/few_seats/price.early_bird are recomputed upstream against ITS build
# date, so they drift with no editorial change behind them.
assert_output "derived pricing/few_seats/early_bird drift is not a change" derived <<'EOF'
chore: refresh training dates from trainings.arc42.org
EOF

assert_output "more than three changed fields are counted, not listed" rewrite <<'EOF'
chore: 26-12 MSA — 6 fields changed

- updated  26-12 MSA (msa-dez-2026): 6 fields changed
EOF

assert_output "an over-long course list degrades to a count, never a fragment" long <<'EOF'
chore: 4 training changes (Mastering Software Architectures +3)

- added    27-01 Master (msa-x0), 2027-01-05 to 2027-01-07, Frankfurt/Main, de
- added    27-02 IMPROV (improve-x1), 2027-02-05 to 2027-02-07, Frankfurt/Main, de
- added    27-03 Requir (req4arc-x2), 2027-03-05 to 2027-03-07, Frankfurt/Main, de
- added    27-04 AsciiD (adoc-x3), 2027-04-05 to 2027-04-07, Frankfurt/Main, de
EOF

# "Never let a city break the format": the live feed has cities like
# "Mannheim / Frankfurt (t.b.d.)", and a multi-line one must not split a body line.
assert_output "a multi-line city stays on one line" messy <<'EOF'
chore: new date 27-05 MSA, 2027-05-03

- added    27-05 MSA (msa-mai-2027), 2027-05-03 to 2027-05-06, Mannheim / Frankfurt (t.b.d.,…, de
EOF

# Course-level fields live outside every `dates` array, so a rename used to slip
# through as "nothing changed". This is the real case, commit 32a2535.
assert_output "a renamed course is reported, not silently committed" rename <<'EOF'
chore: MSA — short title "Mastering SW Architectures" → "MSA"

- course   MSA (msa): short title "Mastering SW Architectures" → "MSA"
EOF

# The renamed course is named by its NEW short_title in the parenthetical: the
# message describes the state after the refresh.
assert_output "a course change and a date change count together" coursemix <<'EOF'
chore: 2 training changes (MSA)

- course   MSA (msa): short title "Mastering SW Architectures" → "MSA"
- updated  26-12 MSA (msa-dez-2026): status full
EOF

# The ended date comes out of the OLD payload, where the course still had its
# old name; listing one course under two names would be nonsense.
assert_output "a renamed course is named once, by its new name" renamemix <<'EOF'
chore: 2 training changes (MSA)

- course   MSA (msa): short title "Mastering SW Architectures" → "MSA"
- ended    25-11 MSA (msa-nov-2025) — past
EOF

assert_output "a new course is announced above its dates" newcourse <<'EOF'
chore: 2 training changes (ADOC)

- course   ADOC (adoc): new course
- added    27-03 ADOC (adoc-mar-2027), 2027-03-08 to 2027-03-09, online, de
EOF

assert_output "a course that disappeared upstream is reported" coursegone <<'EOF'
chore: course ADOC removed

- course   ADOC (adoc): course removed
EOF

# credit_points is an object; it must read as words, never as raw JSON.
assert_output "a credit_points change is spelled out" creditpoints <<'EOF'
chore: ADOC — credit points now 20 methodical, 10 technical

- course   ADOC (adoc): credit points now 20 methodical, 10 technical
EOF

# A quoted rename can overflow the subject. The values are dropped there rather
# than the line being cut through a quote; the body keeps them.
assert_output "an over-long rename loses its values in the subject only" longrename <<'EOF'
chore: MSA Advanced Edition — short title changed

- course   MSA Advanced Edition (msa): short title "Mastering SW Architektur" → "MSA Advanced Edition"
EOF

# `credits` is the course-level counterpart of the derived date keys: upstream
# renders it from credit_points, so it drifts without an editorial change.
assert_output "a change inside dates is no course change" datesonly <<'EOF'
chore: 26-12 MSA — status full

- updated  26-12 MSA (msa-dez-2026): status full
EOF

assert_output "three courses are all named while they fit" courses3 <<'EOF'
chore: 3 training changes (MSA, ADOC, IMPROVE)

- added    27-02 MSA (msa-feb-2027), 2027-02-01 to 2027-02-04, Köln, de
- added    27-03 ADOC (adoc-mar-2027), 2027-03-08 to 2027-03-09, Köln, de
- added    27-04 IMPROVE (improve-apr-2027), 2027-04-19 to 2027-04-20, Köln, de
EOF

# The live short_title of the most frequently edited course is "Mastering SW
# Architectures" - 26 characters - so the budget runs out at the third name.
assert_output "courses that do not fit become +N, not a cut-off name" plusn <<'EOF'
chore: 4 training changes (Mastering SW Architectures, IMPROVE +2)

- added    27-02 MSA (msa-feb-2027), 2027-02-01 to 2027-02-04, Köln, de
- added    27-04 IMPROVE (improve-apr-2027), 2027-04-19 to 2027-04-20, Köln, de
- added    27-05 Req4Arc (req4arc-mai-2027), 2027-05-11 to 2027-05-13, Köln, de
- added    27-03 ADOC (adoc-mar-2027), 2027-03-08 to 2027-03-09, Köln, de
EOF

assert_output "a single name that does not fit drops the parenthetical" overflow <<'EOF'
chore: 2 training changes

- added    27-02 MSA (msa-feb-2027), 2027-02-01 to 2027-02-04, Köln, de
- added    27-07 MSA (msa-jul-2027), 2027-07-05 to 2027-07-08, Köln, de
EOF

for fixture in added seats gone multi nochange derived rewrite long messy courses3 plusn overflow rename coursemix newcourse coursegone creditpoints datesonly longrename renamemix; do
  assert_subject_fits "$fixture"
done

# Every fixture must produce a non-empty subject; the workflow falls back to the
# generic message on empty output, and a silent fallback would hide a bug here.
for fixture in added seats gone multi nochange derived rewrite long messy courses3 plusn overflow rename coursemix newcourse coursegone creditpoints datesonly longrename renamemix; do
  if [ -z "$(generate "$fixture" | head -n 1)" ]; then
    fail "empty subject for fixture $fixture" ""
  fi
done
printf 'ok - %s\n' "no fixture produces an empty subject"

printf '\nAll commit-message tests passed.\n'
