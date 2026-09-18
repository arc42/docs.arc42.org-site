// Renders the /graph page with the vendored Cytoscape.js (no CDN, see
// static/vendor/README.md). Reads #graph-canvas[data-kind], fetches
// /graph.json?kind=..., and wires the type-filter checkboxes and legend.
// Node/edge colors are read from the design tokens in style.css (:root
// custom properties), never hardcoded, so a palette change here stays in
// one place.
(function () {
  "use strict";

  var TYPE_LABELS = {
    section: "Section", tip: "Tip", example: "Example", faq: "FAQ",
    term: "Term", keyword: "Keyword", system: "System",
  };
  var TYPE_TOKENS = {
    section: "--deep-blue", tip: "--signal-blue", example: "--example-ink",
    faq: "--coral", term: "--emerald", keyword: "--amber", system: "--muted",
  };
  var STATUS_TOKENS = {
    draft: "--muted", review: "--amber", published: "--emerald", retired: "--maroon",
  };

  function token(name, fallback) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name);
    v = (v || "").trim();
    return v || fallback || "#5e6975";
  }

  function typeColor(type) {
    return token(TYPE_TOKENS[type], "#5e6975");
  }

  function buildStyle() {
    var style = [
      { selector: "node", style: {
          "label": "data(label)", "font-size": 10, "font-family": "var(--font-body)",
          "color": token("--ink"), "text-valign": "bottom", "text-margin-y": 4,
          "text-wrap": "wrap", "text-max-width": 90,
          "width": 20, "height": 20, "border-width": 2, "border-color": token("--paper"),
      } },
      { selector: "edge", style: {
          "width": 1.4, "line-color": token("--hairline"), "curve-style": "bezier",
          "opacity": 0.85,
      } },
      { selector: "edge[weight]", style: { "width": "mapData(weight, 1, 6, 1.5, 7)" } },
      { selector: ".graph-hidden", style: { "display": "none" } },
    ];
    Object.keys(TYPE_TOKENS).forEach(function (type) {
      style.push({ selector: 'node[type="' + type + '"]',
                   style: { "background-color": typeColor(type) } });
    });
    Object.keys(STATUS_TOKENS).forEach(function (status) {
      style.push({ selector: 'node[status="' + status + '"]',
                   style: { "border-color": token(STATUS_TOKENS[status]) } });
    });
    return style;
  }

  function renderLegend(types) {
    var el = document.getElementById("graph-legend");
    if (!el) { return; }
    el.innerHTML = "";
    types.forEach(function (type) {
      var item = document.createElement("div");
      item.className = "graph-legend-item";
      var swatch = document.createElement("span");
      swatch.className = "graph-legend-swatch";
      swatch.style.background = typeColor(type);
      item.appendChild(swatch);
      item.appendChild(document.createTextNode(TYPE_LABELS[type] || type));
      el.appendChild(item);
    });
  }

  function renderFilters(cy, types) {
    var el = document.getElementById("graph-type-filters");
    if (!el) { return; }
    el.innerHTML = "";
    types.forEach(function (type) {
      var label = document.createElement("label");
      label.className = "graph-filter";
      var box = document.createElement("input");
      box.type = "checkbox";
      box.checked = true;
      box.addEventListener("change", function () {
        var nodes = cy.nodes('[type="' + type + '"]');
        nodes[box.checked ? "removeClass" : "addClass"]("graph-hidden");
        cy.edges().forEach(function (edge) {
          var hide = edge.source().hasClass("graph-hidden") || edge.target().hasClass("graph-hidden");
          edge[hide ? "addClass" : "removeClass"]("graph-hidden");
        });
      });
      label.appendChild(box);
      label.appendChild(document.createTextNode(" " + (TYPE_LABELS[type] || type)));
      el.appendChild(label);
    });
  }

  var canvas = document.getElementById("graph-canvas");
  if (!canvas || !window.cytoscape) { return; }
  var kind = canvas.dataset.kind || "links";

  fetch("/graph.json?kind=" + encodeURIComponent(kind))
    .then(function (r) { return r.json(); })
    .then(function (data) {
      var cy = window.cytoscape({
        container: canvas,
        elements: {
          nodes: data.nodes.map(function (n) { return { data: n }; }),
          edges: data.edges.map(function (e, i) {
            var d = { id: "e" + i, source: e.source, target: e.target };
            if (e.kind !== undefined) { d.kind = e.kind; }
            if (e.weight !== undefined) { d.weight = e.weight; }
            return { data: d };
          }),
        },
        style: buildStyle(),
        layout: { name: "cose", animate: false, nodeRepulsion: 6000, idealEdgeLength: 80, padding: 24 },
        wheelSensitivity: 0.2,
      });
      cy.on("tap", "node", function (evt) {
        window.location = "/page/" + evt.target.id();
      });
      var types = Array.from(new Set(data.nodes.map(function (n) { return n.type; }))).sort();
      renderLegend(types);
      renderFilters(cy, types);
    })
    .catch(function () {
      canvas.textContent = "Could not load the graph.";
    });
})();
