#!/bin/sh

set -eu

SITE_DIR="_site"
FAILURES=0
STARTED_JEKYLL=0

section() {
    printf '\n==> %s\n' "$1"
}

pass() {
    printf 'PASS %s\n' "$1"
}

fail() {
    printf 'FAIL %s\n' "$1"
    FAILURES=$((FAILURES + 1))
}

cleanup() {
    if [ "$STARTED_JEKYLL" -eq 1 ]; then
        section "Stop temporary Docker service"
        printf 'Running: docker compose stop jekyll\n'
        docker compose stop jekyll >/dev/null
        pass "Stopped temporary jekyll service."
    fi
}

trap cleanup EXIT

section "Build site with Docker"
if docker compose ps --status running --services 2>/dev/null | rg -x 'jekyll' >/dev/null 2>&1; then
    pass "Reusing already running jekyll service."
else
    printf 'Running: docker compose up -d jekyll\n'
    docker compose up -d jekyll
    STARTED_JEKYLL=1
    pass "Started temporary jekyll service."
fi

printf 'Running: docker compose exec -T jekyll bundle exec jekyll build\n'
if docker compose exec -T jekyll bundle exec jekyll build; then
    pass "Jekyll build completed successfully."
else
    fail "Jekyll build failed."
    exit 1
fi

section "Check required top-level pages"
for page in \
    "$SITE_DIR/index.html" \
    "$SITE_DIR/examples/index.html" \
    "$SITE_DIR/keywords/index.html" \
    "$SITE_DIR/contact/index.html" \
    "$SITE_DIR/imprint/index.html"
do
    if [ -f "$page" ]; then
        pass "Found $page"
    else
        fail "Missing $page"
    fi
done

section "Check arc42 section pages"
i=1
while [ "$i" -le 12 ]; do
    page="$SITE_DIR/section-$i/index.html"
    if [ -f "$page" ]; then
        pass "Found $page"
    else
        fail "Missing $page"
    fi
    i=$((i + 1))
done

section "Check rail navigation items"
# The rail, and read off a SECTION page rather than /home/: the rail is
# deliberately not rendered on the home page (_layouts/default.html, the
# `unless is_home` guard), so there is nothing to scrape there. The version of
# this check that preceded the rail rewrite looked for class="page-link" in
# _site/home/index.html — markup inherited from the faq.arc42.org copy that the
# rewrite removed — and so reported every item missing on every run.
#
# The expected list is literal on purpose. Deriving it from _data/sections.yml
# would make a renamed section pass silently, and a renamed section is exactly
# the change worth being told about. The twelve sections come from that file;
# the "More" group is every page carrying `group: meta`, ordered by `order`.
# Add a section or a meta page, and this list wants the same edit.
nav_page="$SITE_DIR/section-1/index.html"
expected_nav_file=$(mktemp)
actual_nav_file=$(mktemp)

cat <<'EOF' > "$expected_nav_file"
Introduction and Goals
Constraints
Context and Scope
Solution Strategy
Building Block View
Runtime View
Deployment View
Crosscutting Concepts
Architecture Decisions
Quality Requirements
Risks and Technical Debt
Glossary
Examples
Keywords
Contact
EOF

# Scoped to the <aside class="rail"> block. `class="label"` is generic enough
# that a component added elsewhere on the page could otherwise join the list and
# fail this check for no reason. The range ends at the first </aside>, which is
# the rail's own.
sed -n '/<aside class="rail">/,/<\/aside>/p' "$nav_page" \
    | rg -o 'class="label">[^<]*' \
    | sed -E 's/^class="label">//' > "$actual_nav_file"

expected_count=$(wc -l < "$expected_nav_file" | tr -d ' ')
actual_count=$(wc -l < "$actual_nav_file" | tr -d ' ')

if [ "$actual_count" -ne "$expected_count" ]; then
    fail "Rail contains $actual_count items, expected $expected_count."
fi

line_no=1
while IFS= read -r expected_item; do
    actual_item=$(sed -n "${line_no}p" "$actual_nav_file")
    if [ "$actual_item" = "$expected_item" ]; then
        pass "Rail item $line_no matches: $expected_item"
    else
        fail "Rail item $line_no mismatch. Expected '$expected_item', got '${actual_item:-<missing>}'"
    fi
    line_no=$((line_no + 1))
done < "$expected_nav_file"

if ! cmp -s "$expected_nav_file" "$actual_nav_file"; then
    printf 'Expected rail items:\n'
    cat "$expected_nav_file"
    printf 'Actual rail items:\n'
    cat "$actual_nav_file"
fi

rm -f "$expected_nav_file" "$actual_nav_file"

section "Check for unresolved Liquid tags in generated HTML/XML"
if rg -n '\{\{|\{%' "$SITE_DIR" --glob '*.html' --glob '*.xml'; then
    fail "Generated output still contains unresolved Liquid markup."
else
    pass "No unresolved Liquid tags found in generated HTML/XML."
fi

section "Check generated HTML for broken local href/src targets"
local_refs=$(
    rg -o --no-filename '(href|src)="/[^"#?:][^"]*"' "$SITE_DIR" --glob '*.html' \
        | sed -E 's/^(href|src)="([^"]*)"$/\2/' \
        | sort -u
)

if [ -z "$local_refs" ]; then
    fail "No local href/src targets were found in generated HTML."
else
    checked_refs=0
    missing_refs=0
    for ref in $local_refs; do
        target=${ref%%\#*}
        target=${target%%\?*}

        if [ "$target" = "/" ]; then
            resolved="$SITE_DIR/index.html"
        elif [ -f "$SITE_DIR$target" ]; then
            resolved="$SITE_DIR$target"
        elif [ -f "$SITE_DIR$target/index.html" ]; then
            resolved="$SITE_DIR$target/index.html"
        else
            resolved=""
        fi

        checked_refs=$((checked_refs + 1))

        if [ -n "$resolved" ]; then
            pass "$ref -> $resolved"
        else
            fail "$ref does not resolve inside $SITE_DIR"
            missing_refs=$((missing_refs + 1))
        fi
    done

    if [ "$missing_refs" -eq 0 ]; then
        pass "Resolved all $checked_refs local href/src targets."
    else
        fail "$missing_refs of $checked_refs local href/src targets are missing."
    fi
fi

section "Summary"
if [ "$FAILURES" -eq 0 ]; then
    printf 'All sanity checks passed.\n'
else
    printf 'Sanity checks finished with %s failure(s).\n' "$FAILURES"
    exit 1
fi
