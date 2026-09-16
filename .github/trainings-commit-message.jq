# Builds the git commit message for the automated "refresh training dates" run.
#
# Invocation (see .github/workflows/refresh-trainings.yml):
#
#   jq -n -r --arg today "$(date -u +%Y-%m-%d)" \
#      --slurpfile old /tmp/old.json \
#      --slurpfile new /tmp/new.json \
#      -f .github/trainings-commit-message.jq
#
# `today` is passed in and `now` is never called here, so the tests can pin the
# date: the ended/removed split below is a comparison against "today" and would
# otherwise be untestable.
#
# Dates are matched by `id` across all courses; a date that moves from one course
# to another would read as removed + added, which is the honest description.
#
# Courses are matched by `id` as well and diffed on everything but `dates`, which
# the date events already cover. Course-level edits are rare but real: upstream
# renamed msa's `short_title` once and the refresh committed it under the generic
# subject, because nothing inside any `dates` array had moved.

# Upstream computes `pricing`, `credits`, `few_seats` and the early-bird block
# against ITS build date, so they change on their own as time passes (an expired
# early bird disappears from the feed entirely). Comparing them would report
# phantom edits, so they are dropped before diffing and the underlying `price`,
# `credit_points` and `seats_limited` are reported instead.
# In the live feed the early bird sits at `price.early_bird`, not at the top
# level - both paths are dropped so either shape stays quiet.
def undecorated:
  delpaths([["pricing"], ["credits"], ["few_seats"], ["early_bird"], ["price", "early_bird"]]);

# A city or course title carrying a newline would break the one-line-per-event
# body, so every value that reaches the output goes through here first.
def clean:
  if . == null then ""
  else tostring
    | gsub("[[:space:]]+"; " ")
    | sub("^ +"; "")
    | sub(" +$"; "")
  end;

def trunc($n):
  if (length > $n) then (.[0:$n - 1] | sub(" +$"; "")) + "…" else . end;

def pad($n):
  if (length < $n) then . + (" " * ($n - length)) else . end;

def dates_of($payload):
  [ $payload.courses[]?
    | . as $course
    | ($course.dates[]? | select(type == "object" and .id != null))
    | { id: (.id | tostring),
        course_id: ($course.id | tostring),
        course: (($course.short_title // $course.title // $course.id) | clean),
        d: . } ];

# `dates` is dropped here: those are diffed separately, and keeping them would
# report every date change a second time as a change to its course.
def courses_of($payload):
  [ $payload.courses[]?
    | select(type == "object" and .id != null)
    | { id: (.id | tostring),
        course: ((.short_title // .title // .id) | clean),
        c: del(.dates) } ];

def by_id:
  reduce .[] as $entry ({}; .[$entry.id] = $entry);

# Fields whose change is worth naming, most newsworthy first; everything else
# sorts after them alphabetically so the output stays deterministic. Date fields
# first, then course fields - the two never occur on the same object, so one
# shared list holds both orderings.
def field_order:
  ["status", "seats_limited", "start", "end", "city", "country", "price", "format", "language", "trainers",
   "short_title", "title", "certification", "credit_points", "blurb", "url", "url_en"];

def changed_fields($x; $y):
  [ (($x | keys) + ($y | keys)) | unique | .[] | select($x[.] != $y[.]) ]
  | sort_by(. as $f | [(field_order | index($f)) // 99, $f]);

def readable($field): ($field | clean | gsub("_"; " "));

# Quoting both values is the clearest way to show a rename, but only while they
# fit on one line; past that the label alone says enough and the reader has the
# diff.
def renamed($field; $a; $b):
  ($a | clean) as $x
  | ($b | clean) as $y
  | if $y == "" then readable($field) + " dropped"
    elif $x == "" then readable($field) + " set to \"" + ($y | trunc(40)) + "\""
    elif (($x | length) + ($y | length)) <= 44
    then readable($field) + " \"" + $x + "\" → \"" + $y + "\""
    else readable($field) + " changed"
    end;

# credit_points is an object ({"methodical": 20, "technical": 10}); dumped raw it
# would put JSON in a commit subject.
def credit_points_phrase($value):
  if ($value | type) == "object" and ($value | length) > 0 then
    "credit points now "
    + ($value | to_entries | map((.value | tostring) + " " + (.key | clean)) | join(", "))
  elif $value == null then "credit points dropped"
  else "credit points changed"
  end;

def course_phrase($field; $x; $y):
  if $field == "credit_points" then credit_points_phrase($y.credit_points)
  elif $field == "trainers" then "trainers changed"
  elif (["short_title", "title", "certification"] | index($field)) != null then
    renamed($field; $x[$field]; $y[$field])
  else readable($field) + " changed"
  end;

def phrase($field; $x; $y):
  if $field == "seats_limited" then
    (if $y.seats_limited == true then "few seats left" else "no longer short of seats" end)
  elif $field == "status" then "status " + ($y.status | clean | trunc(20))
  elif $field == "start" then "moved to " + ($y.start | clean | trunc(20))
  elif $field == "end" then "now ends " + ($y.end | clean | trunc(20))
  elif $field == "city" then
    (if ($y.city | clean) == "" then "city dropped" else "now in " + ($y.city | clean | trunc(30)) end)
  elif $field == "format" then "format now " + ($y.format | clean | trunc(20))
  elif $field == "language" then "language now " + ($y.language | clean | trunc(20))
  elif $field == "price" then
    (if ($y.price.amount != null and $x.price.amount != $y.price.amount)
     then "price now " + ($y.price.amount | tostring) + " " + (($y.price.currency // "EUR") | clean | trunc(8))
     else "price changed" end)
  elif $field == "trainers" then "trainers changed"
  else readable($field | trunc(20)) + " changed"
  end;

def code_of($entry): (($entry.d.code // $entry.id) | clean | trunc(40));

def name_of($entry): (if ($entry.course | length) > 0 then $entry.course else $entry.id end | trunc(40));

def place_of($d):
  if ($d.format // "") == "online" then "online"
  else (($d.city // $d.country // "t.b.d.") | clean | trunc(30))
  end;

# More than three changes at once is a rewrite, not an edit; listing them all
# would bury the interesting ones.
def summary_from($changes):
  if ($changes | length) > 3
  then (($changes | length) | tostring) + " fields changed"
  else ($changes | join(", "))
  end;

# `word` rather than `kind`, so the three course kinds all show as "course" and
# cannot be read as a date: a date line carries a booking code, a course line the
# course name.
def line_of($event):
  "- " + ($event.word | pad(9))
  + (if $event.word == "course" then
       name_of($event.entry) + " (" + $event.entry.id + ")"
       + (if $event.kind == "course-new" then ": new course"
          elif $event.kind == "course-gone" then ": course removed"
          else ": " + summary_from($event.changes)
          end)
     else
       code_of($event.entry) + " (" + $event.entry.id + ")"
       + (if $event.kind == "added" then
            ", " + ($event.entry.d.start | clean) + " to " + ($event.entry.d.end | clean)
            + ", " + place_of($event.entry.d) + ", " + ($event.entry.d.language | clean)
          elif $event.kind == "updated" then ": " + summary_from($event.changes)
          elif $event.kind == "ended" then " — past"
          else ""
          end)
     end);

# The course list must degrade, not get sliced: truncating it mid-name drops
# courses silently and cuts a word in half, which tells the reader less than a
# plain count would. So names are only ever added while the whole subject still
# fits in 72 characters; the rest become "+N", and if not even the first name
# fits, the parenthetical goes away entirely. The body lists every event in
# full, so nothing is actually lost here.
def counted_subject($events; $courses):
  ("chore: " + (($events | length) | tostring) + " training changes") as $base
  | [ range(1; ($courses | length) + 1) as $k
      | (($courses | length) - $k) as $rest
      | $base + " (" + ($courses[0:$k] | join(", "))
        + (if $rest > 0 then " +" + ($rest | tostring) else "" end) + ")"
      | select(length <= 72) ] as $fitting
  | if ($fitting | length) > 0 then $fitting[-1] else $base end;

def subject_from($event; $changes):
  if $event.kind == "added" then
    "chore: new date " + code_of($event.entry) + ", " + ($event.entry.d.start | clean)
  elif $event.kind == "updated" then
    "chore: " + code_of($event.entry) + " — " + summary_from($changes)
  elif $event.kind == "removed" then
    "chore: " + code_of($event.entry) + " withdrawn"
  elif $event.kind == "ended" then
    "chore: " + code_of($event.entry) + " has ended"
  elif $event.kind == "course-new" then
    "chore: new course " + name_of($event.entry)
  elif $event.kind == "course-gone" then
    "chore: course " + name_of($event.entry) + " removed"
  else
    "chore: " + name_of($event.entry) + " — " + summary_from($changes)
  end;

# Each updated event carries a terse set of change phrases beside the rich one.
# A quoted rename or a long city can push the subject past the budget, and losing
# the values is a better degradation than a line cut mid-quote.
def subject_of($event):
  subject_from($event; $event.changes) as $rich
  | if ($rich | length) <= 72 then $rich else subject_from($event; $event.terse) end;

($old[0] // {}) as $o
| ($new[0] // {}) as $n
| (dates_of($o)) as $old_dates
| (dates_of($n)) as $new_dates
| ($old_dates | by_id) as $old_by_id
| ($new_dates | by_id) as $new_by_id
| [ $new_dates[] | select($old_by_id[.id] == null)
    | {kind: "added", word: "added", entry: ., changes: [], terse: []} ] as $added
| [ $new_dates[]
    | . as $entry
    | ($old_by_id[$entry.id]) as $before
    | select($before != null)
    | ($before.d | undecorated) as $x
    | ($entry.d | undecorated) as $y
    | select($x != $y)
    | (changed_fields($x; $y)) as $fields
    | {kind: "updated", word: "updated", entry: $entry,
       changes: [$fields[] | phrase(.; $x; $y)],
       terse: [$fields[] | readable(.) + " changed"]} ] as $updated
| [ $old_dates[] | select($new_by_id[.id] == null) ] as $gone
# A date vanishes for two completely different reasons: the workflow's expiry
# filter dropped it because it is over (routine), or somebody withdrew it
# upstream while it was still to come (news). The end date is what tells them
# apart, and calling the first one "removed" would read like a cancellation.
| [ $gone[] | select((.d.end // "9999-12-31") >= $today)
    | {kind: "removed", word: "removed", entry: ., changes: [], terse: []} ] as $removed
| [ $gone[] | select((.d.end // "9999-12-31") < $today)
    | {kind: "ended", word: "ended", entry: ., changes: [], terse: []} ] as $ended
| (courses_of($o)) as $old_courses
| (courses_of($n)) as $new_courses
| ($old_courses | by_id) as $old_course_by_id
| ($new_courses | by_id) as $new_course_by_id
| [ $new_courses[] | select($old_course_by_id[.id] == null)
    | {kind: "course-new", word: "course", entry: ., changes: [], terse: []} ] as $course_new
# A renamed course is named by its NEW short_title here and in the subject: the
# message describes the state after the refresh, and that is the name a reader
# searching the history later will have in hand. The old name is not lost - the
# body line quotes both sides of the rename.
| [ $new_courses[]
    | . as $entry
    | ($old_course_by_id[$entry.id]) as $before
    | select($before != null)
    | ($before.c | undecorated) as $x
    | ($entry.c | undecorated) as $y
    | select($x != $y)
    | (changed_fields($x; $y)) as $fields
    | {kind: "course-updated", word: "course", entry: $entry,
       changes: [$fields[] | course_phrase(.; $x; $y)],
       terse: [$fields[] | readable(.) + " changed"]} ] as $course_updated
| [ $old_courses[] | select($new_course_by_id[.id] == null)
    | {kind: "course-gone", word: "course", entry: ., changes: [], terse: []} ] as $course_gone
# Course events lead: a rename or a new course is the context for the date lines
# under it.
| ($course_new + $course_updated + $course_gone + $added + $updated + $removed + $ended) as $raw_events
# Events taken from the old payload (ended, removed, a dropped course) carry the
# course name as it was. After a rename that would list one course twice, under
# both names, so every event is renamed to the course's current name; the rename
# phrase itself still quotes both sides.
| (reduce (($old_courses + $new_courses)[]) as $c ({}; .[$c.id] = $c.course)) as $course_names
| [ $raw_events[]
    | .entry.course = ($course_names[.entry.course_id // .entry.id] // .entry.course) ] as $events
| ([ $events[].entry.course | select(. != "") ] | reduce .[] as $c ([]; if index($c) == null then . + [$c] else . end)) as $courses
| (if ($events | length) == 0 then
     "chore: refresh training dates from trainings.arc42.org"
   elif ($events | length) == 1 then
     subject_of($events[0])
   else
     counted_subject($events; $courses)
   end) as $raw_subject
| ($raw_subject | trunc(72)) as $subject
| if ($events | length) == 0 then $subject
  else $subject + "\n\n" + ([$events[] | line_of(.)] | join("\n"))
  end
