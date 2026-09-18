// Dashboard client script: presence heartbeat (ping/leaving) and the
// facilitator/connected-count footer. Ported from eTSU's base.html
// heartbeat script; see presence.py for the server side. No CDN, no build
// step: this file is served as-is from /static/app.js.
(function () {
  "use strict";

  function makeClientId() {
    try {
      var id = sessionStorage.getItem("brain-client-id");
      if (!id) {
        id = (window.crypto && crypto.randomUUID)
          ? crypto.randomUUID()
          : (Date.now().toString(36) + Math.random().toString(36).slice(2));
        sessionStorage.setItem("brain-client-id", id);
      }
      return id;
    } catch (e) {
      return Date.now().toString(36) + Math.random().toString(36).slice(2);
    }
  }

  var CLIENT_ID = makeClientId();
  window.brainClientId = CLIENT_ID;

  var PING_INTERVAL_MS = 20000;

  function ping() {
    fetch("/ping", {
      method: "POST",
      keepalive: true,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ client_id: CLIENT_ID }),
    })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (!data) { return; }
        var countEl = document.getElementById("presence-count");
        if (countEl) { countEl.textContent = data.count + " connected"; }
        document.body.dataset.facilitator = data.is_facilitator ? "yes" : "no";
        document.dispatchEvent(new CustomEvent("brain:presence", { detail: data }));
      })
      .catch(function () {});
  }

  ping();
  setInterval(ping, PING_INTERVAL_MS);

  // Signal when the page disappears (tab/window closed OR navigation): on
  // navigation, the next page's immediate ping() cancels the goodbye; on an
  // actual close, the server drops this client after a short grace period.
  window.addEventListener("pagehide", function () {
    if (navigator.sendBeacon) {
      navigator.sendBeacon("/leaving", new Blob(
        [JSON.stringify({ client_id: CLIENT_ID })], { type: "application/json" }));
    }
  });
})();
