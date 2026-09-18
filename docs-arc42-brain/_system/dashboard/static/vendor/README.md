# Vendored third-party assets

Served as a static file so `/graph` renders **offline** (no CDN at runtime,
per the dashboard's no-CDN rule).

## cytoscape.min.js
- **Library:** Cytoscape.js (graph rendering) — <https://js.cytoscape.org>
- **Version:** 3.30.3
- **Build:** minified UMD/IIFE; exposes `globalThis.cytoscape`, loaded via a
  classic `<script>` in `templates/graph.html` (before `static/graph.js`).
- **License:** MIT (© 2016-2024, The Cytoscape Consortium). License header
  kept intact at the top of the file.
- **Source:** copied from `eTSU/_system/apps/dashboard/static/vendor/cytoscape.min.js`,
  itself originally fetched from `cdnjs.cloudflare.com/ajax/libs/cytoscape/3.30.3/cytoscape.min.js`.
- **Used by:** `static/graph.js`, the link/term graph on `/graph`. Layout is
  Cytoscape's built-in `cose` (no extra layout plugin vendored).

To update: fetch the same minified build for the desired pinned version,
check the license header is still present, and bump the version above.
