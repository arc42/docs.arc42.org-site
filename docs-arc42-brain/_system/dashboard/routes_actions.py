"""Blueprint for presence heartbeat and action routes: ping/leaving/who,
facilitator-gated generate/preview, job polling, link health and reload.

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
    services = _services()
    if not services["presence"].is_facilitator(client_id(request)):
        return jsonify(error="only the facilitator can generate"), 403
    job, started = services["runner"].start(kind)
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
