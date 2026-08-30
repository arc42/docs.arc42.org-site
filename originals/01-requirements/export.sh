#!/usr/bin/env bash
# Re-export the ISO 25010:2023 diagrams from their .drawio.png sources.
#
# Each source is a draw.io PNG with the diagram XML embedded, so draw.io opens
# it by double-click and this script turns it back into the SVG the site ships.
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
OUT="$HERE/../../assets/images/sections/01"

for name in iso-25010-2023-topics-en iso-25010-2023-tree-en quality-example-loop; do
  "$DRAWIO" "$HERE/$name.drawio.png" -x -f svg -o "$OUT/$name.svg" \
    --svg-theme light --embed-svg-fonts false --no-sandbox --disable-gpu
  # draw.io emits bare family names; give them a fallback stack so the diagram
  # does not drop to the browser's default serif on machines without Mark Pro.
  perl -pi -e "s/font-family: 'Mark Pro'/font-family: 'Mark Pro', Helvetica, Arial, sans-serif/g;
               s/font-family: Helvetica(?!,)/font-family: Helvetica, Arial, sans-serif/g" "$OUT/$name.svg"
  echo "wrote $OUT/$name.svg ($(wc -c <"$OUT/$name.svg" | tr -d ' ') bytes)"
done
