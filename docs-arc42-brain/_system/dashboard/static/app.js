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
        // This tab's own name in the masthead; only Yoda gets the avatar.
        var me = document.getElementById("presence-me");
        if (me) {
          document.getElementById("presence-name").textContent = data.nickname;
          document.getElementById("presence-avatar").hidden = !data.is_facilitator;
          me.hidden = false;
        }
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

  // -- /actions: facilitator-gated generate/preview buttons -----------------
  //
  // Buttons start disabled in the markup; enabled/disabled state is driven
  // by body[data-facilitator], read once here and kept live via the
  // "brain:presence" event every ping() dispatches.
  var GEN_SELECTOR = '[data-action="generate"], [data-action="preview"]';
  var genButtons = document.querySelectorAll(GEN_SELECTOR);
  if (genButtons.length) {
    var applyFacilitatorState = function () {
      var isFacilitator = document.body.dataset.facilitator === "yes";
      genButtons.forEach(function (btn) { btn.disabled = !isFacilitator; });
    };
    applyFacilitatorState();
    document.addEventListener("brain:presence", applyFacilitatorState);

    var pollTimer = null;
    var pollErrors = 0;
    var POLL_ERROR_LIMIT = 10;
    var pollJob = function () {
      fetch("/actions/job")
        .then(function (r) {
          if (!r.ok) { throw new Error("bad status " + r.status); }
          return r.json();
        })
        .then(function (data) {
          pollErrors = 0;
          if (data && data.current === null) {
            clearInterval(pollTimer);
            window.location.reload();
          }
        })
        .catch(function () {
          pollErrors += 1;
          if (pollErrors >= POLL_ERROR_LIMIT) {
            clearInterval(pollTimer);
            applyFacilitatorState();
            var note = document.getElementById("facilitator-note");
            if (note) { note.textContent = "Lost contact with the server."; }
          }
        });
    };
    genButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var kind = btn.dataset.action;
        genButtons.forEach(function (b) { b.disabled = true; });
        fetch("/actions/" + kind, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ client_id: CLIENT_ID }),
        })
          .then(function (r) { return r.json(); })
          .then(function (data) {
            if (data && data.error) {
              alert(data.error);
              applyFacilitatorState();
              return;
            }
            pollTimer = setInterval(pollJob, 1000);
          })
          .catch(function () { applyFacilitatorState(); });
      });
    });
  }

  // -- /links: "check now" button, run any time, no facilitator gate --------
  var linkBtn = document.getElementById("linkcheck-btn");
  if (linkBtn) {
    linkBtn.addEventListener("click", function () {
      linkBtn.disabled = true;
      var status = document.getElementById("linkcheck-status");
      fetch("/actions/linkcheck", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ client_id: CLIENT_ID }),
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (status) {
            status.textContent = data && data.started
              ? "Checking now — this page will reload in a few seconds."
              : "A check is already running — this page will reload in a few seconds.";
          }
          setTimeout(function () { window.location.reload(); }, 5000);
        })
        .catch(function () {
          linkBtn.disabled = false;
          if (status) { status.textContent = "Could not start the check."; }
        });
    });
  }
})();
