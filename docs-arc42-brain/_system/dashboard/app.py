"""Flask app factory for the docs-arc42-brain dashboard.

Routes only; keep this file under 300 lines. Everything else (model,
presence, generate runner, link checker) is injected as `services` and
stashed on `app.extensions["brain"]`, to be filled in by later tasks.
"""
from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, render_template


def create_app(repo: Path | None = None, **services) -> Flask:
    if repo is None:
        repo = Path(os.environ.get("BRAIN_REPO", "."))
    repo = Path(repo)

    app = Flask(__name__)
    app.config["REPO"] = repo
    app.extensions["brain"] = dict(services)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app


# Module-level factory target for gunicorn ("app:create_app()"); no eager
# instance here, since create_app() needs BRAIN_REPO to be set at call time.
app = None
