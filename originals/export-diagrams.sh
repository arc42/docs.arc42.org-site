#!/usr/bin/env bash
# Re-export every diagram in originals/ to the SVG the site ships.
#
# Sources live in originals/<NN>-<topic>/ and land in assets/images/sections/<NN>/.
# Both source forms are picked up: a plain .drawio file, and a .drawio.png, which
# is a rendering with the diagram XML embedded so draw.io opens it by double-click.
#
# Two flags are not optional:
#   --embed-svg-fonts false   the default inlines a base64 webfont (25 KB -> 794 KB)
#   --svg-theme light         the default "auto" writes `color-scheme: light dark`,
#                             which makes dark-mode browsers render the diagram inverted
# Note also that draw.io wants the input file BEFORE the flags; the documented
# order fails with "input file/directory not found".
set -euo pipefail

DRAWIO="${DRAWIO:-/Applications/draw.io.app/Contents/MacOS/draw.io}"
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$HERE/.."

shopt -s nullglob
for src in "$HERE"/*/*.drawio.png "$HERE"/*/*.drawio; do
  dir="$(basename "$(dirname "$src")")"   # e.g. 08-concepts
  section="${dir%%-*}"                    # e.g. 08
  name="$(basename "$src" .drawio.png)"; name="${name%.drawio}"
  out="$ROOT/assets/images/sections/$section/$name.svg"
  mkdir -p "$(dirname "$out")"
  "$DRAWIO" "$src" -x -f svg -o "$out" \
    --svg-theme light --embed-svg-fonts false --no-sandbox --disable-gpu >/dev/null
  # draw.io emits bare family names; give them a fallback stack so a diagram does
  # not drop to the browser's default serif on machines without the named font.
  perl -pi -e "s/font-family: 'Mark Pro'/font-family: 'Mark Pro', Helvetica, Arial, sans-serif/g;
               s/font-family: Helvetica(?!,)/font-family: Helvetica, Arial, sans-serif/g" "$out"
  printf '%-46s -> %s (%s bytes)\n' "$dir/$name" "sections/$section/$name.svg" "$(wc -c <"$out" | tr -d ' ')"
done
