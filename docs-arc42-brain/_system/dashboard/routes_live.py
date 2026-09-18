"""routes_live: presence heartbeat and action routes — ping/leaving/who,
facilitator-gated generate/preview, job polling, link health and reload.
(Renamed from routes_actions.py: it carries presence + actions + links +
reload, not just actions.)

Split out of `app.py` to keep that file under 300 lines (D: `app.py` holds
only routes). Routes only here too; view-shaping lives in `actions.py` /
`linkcheck.py`.
"""
from __future__ import annotations

from flask import Blueprint, current_app, jsonify, redirect, render_template, request

from actions import actions_view
from linkcheck import external_urls, link_summary
from presence import client_id

bp = Blueprint("actions", __name__)

# Every state-changing route on this blueprint (ping, leaving, the
# facilitator-gated actions, and /reload) is a plain unauthenticated POST,
# reachable from the LAN (compose.yaml binds 0.0.0.0). Without an origin
# check, any page the user's browser visits could trigger them with a
# no-cors fetch/form POST. Checked once, here, for every POST on the
# blueprint — not copy-pasted per route.
_SAFE_SEC_FETCH_SITE = {"same-origin", "none"}


def _same_origin(req) -> bool:
    """True unless the request is provably cross-site.
    - An `Origin` header, when present, must match this request's own
      host (scheme+host+port, as seen via `request.host_url`).
    - Without `Origin`, fall back to `Sec-Fetch-Site`: same-origin/none
      pass, cross-site/same-site are rejected.
    - With neither header (curl, server-to-server calls, most test
      clients), the request is allowed through — there's nothing to
      distinguish it from a legitimate script."""
    origin = req.headers.get("Origin")
    if origin is not None:
        return origin.rstrip("/") == req.host_url.rstrip("/")
    site = req.headers.get("Sec-Fetch-Site")
    if site is not None:
        return site in _SAFE_SEC_FETCH_SITE
    return True


@bp.before_request
def _reject_cross_origin():
    if request.method == "POST" and not _same_origin(request):
        return jsonify(error="cross-origin request refused"), 403


def _services():
    return current_app.extensions["brain"]


@bp.route("/ping", methods=["POST"])
def ping():
    return _services()["presence"].ping(client_id(request))


@bp.route("/leaving", methods=["POST"])
def leaving():
    _services()["presence"].leaving(client_id(request))
    return "", 204


@bp.route("/who")
def who():
    return render_template("who.html", entries=_services()["presence"].who())


def _start(kind):
    # Beyond the origin check above: require an actual JSON body, which
    # forces a CORS preflight that Flask never answers, closing off the
    # no-cors `text/plain` request the review flagged.
    if not request.is_json:
        return jsonify(error="expected application/json"), 415
    services = _services()
    if not services["presence"].is_facilitator(client_id(request)):
        return jsonify(error="only the facilitator can generate"), 403
    job, started = services["runner"].start(kind)
    # `job` can be None in a narrow race (see Runner.start): guard rather
    # than crash with a 500 on `None.to_dict()`.
    if job is None:
        return jsonify(started=False, job=None), 202
    return jsonify(started=started, job=job.to_dict()), 202


@bp.route("/actions/generate", methods=["POST"])
def generate():
    return _start("generate")


@bp.route("/actions/preview", methods=["POST"])
def preview():
    return _start("preview")


@bp.route("/actions/job")
def job_status():
    runner = _services()["runner"]
    return jsonify(
        current=runner.current.to_dict() if runner.current else None,
        last=runner.last.to_dict() if runner.last else None,
    )


@bp.route("/actions/linkcheck", methods=["POST"])
def linkcheck_start():
    services = _services()
    b = services["model"].get()
    started = services["linkchecker"].start(external_urls(b))
    return jsonify(started=started), 202


@bp.route("/actions")
def actions_page():
    services = _services()
    b = services["model"].get()
    view = actions_view(b, services["runner"])
    return render_template("actions.html", known=set(b.vault.pages), **view)


@bp.route("/links")
def links_page():
    services = _services()
    rows = services["linkchecker"].results()
    return render_template("links.html", rows=rows, summary=link_summary(rows))


@bp.route("/reload", methods=["POST"])
def reload_route():
    _services()["model"].clear()
    return redirect(request.referrer or "/")
