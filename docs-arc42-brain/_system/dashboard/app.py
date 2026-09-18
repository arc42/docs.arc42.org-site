"""Flask app factory for the docs-arc42-brain dashboard.

Routes only; keep this file under 300 lines. All view data comes from
`model` / `relations`; nothing here re-derives vault logic. Everything else
(model, presence, generate runner, link checker) is injected as `services`
and stashed on `app.extensions["brain"]`.
"""
from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, abort, render_template, request

from actions import Runner
from linkcheck import LinkChecker
from model import (
    STATUSES, Model, examples_view, faq_view, gaps, issues_view, lint_view,
    log_entries, git_log, readiness, review_queue, section_number,
    sections_view, status_counts, tags_view, tips_view,
)
from presence import Presence, client_id
from relations import issues_naming, links_in, links_out, obsidian_url
from render import render


def _fmt_meta(value):
    """A front-matter value as plain text: no python reprs, ever."""
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (list, tuple)):
        return ", ".join(_fmt_meta(v) for v in value) if value else "—"
    if isinstance(value, dict):
        return ", ".join(f"{k}: {_fmt_meta(v)}" for k, v in value.items()) if value else "—"
    return str(value)


def create_app(repo: Path | None = None, **services) -> Flask:
    if repo is None:
        repo = Path(os.environ.get("BRAIN_REPO", "."))
    repo = Path(repo)

    app = Flask(__name__)
    app.config["REPO"] = repo
    app.jinja_env.filters["fmt_meta"] = _fmt_meta

    services.setdefault("model", Model(repo))
    model: Model = services["model"]
    services.setdefault("presence", Presence())
    runner = services.get("runner")
    if runner is None:
        runner = Runner(repo, on_finish=model.clear)
        services["runner"] = runner
    elif getattr(runner, "on_finish", "missing") is None:
        runner.on_finish = model.clear
    services.setdefault(
        "linkchecker", LinkChecker(repo / "docs-arc42-brain/build/dashboard/links.json")
    )

    app.extensions["brain"] = dict(services)
    presence: Presence = app.extensions["brain"]["presence"]
    linkchecker: LinkChecker = app.extensions["brain"]["linkchecker"]

    def _apply_filters(b, pages):
        status = request.args.get("status") or None
        section = request.args.get("section") or None
        system = request.args.get("system") or None
        if status:
            pages = [p for p in pages if p.status == status]
        if section:
            try:
                n = int(section)
            except ValueError:
                n = None
            if n is not None:
                pages = [p for p in pages if section_number(b, p) == n]
        if system:
            pages = [p for p in pages if any(l.target == system for l in p.links_in("system"))]
        return sorted(pages, key=lambda p: p.slug)

    def _rows(b, pages):
        rows = []
        for p in pages:
            sys_links = p.links_in("system")
            sys_name = None
            if sys_links:
                target = b.vault.pages.get(sys_links[0].target)
                sys_name = (target.meta.get("name") if target else None) or sys_links[0].target
            rows.append({
                "slug": p.slug,
                "title": p.meta.get("title") or p.slug,
                "status": p.status,
                "section": section_number(b, p),
                "system": sys_name,
                "updated": p.meta.get("updated"),
            })
        return rows

    def _filter_args():
        return {
            "status": request.args.get("status", ""),
            "section": request.args.get("section", ""),
            "system": request.args.get("system", ""),
        }

    def _list_page(title, ptype, pages_rows, counts, notes):
        return render_template(
            "list.html", title=title, ptype=ptype, pages=pages_rows, counts=counts,
            notes=notes, filters=_filter_args(), statuses=STATUSES,
        )

    def _link_summary(rows):
        if not rows:
            return None
        failures = sum(1 for r in rows if r["status"] is None or r["status"] >= 400)
        redirects = sum(1 for r in rows if r["status"] is not None and 300 <= r["status"] < 400)
        return {"failures": failures, "redirects": redirects, "ok": len(rows) - failures - redirects}

    @app.route("/")
    def home():
        b = model.get()
        parity = runner.parity()
        sections = sections_view(b, parity)
        tips = tips_view(b)
        examples = examples_view(b)
        faq = faq_view(b)
        tags = tags_view(b)
        issues = issues_view(b)
        lint = lint_view(b)
        review = review_queue(b)
        cutover = readiness(b, parity)
        gap = gaps(b)
        link_rows = linkchecker.results()
        return render_template(
            "home.html",
            sections=sections, tips=tips, examples=examples, faq=faq, tags=tags,
            tags_status_counts=status_counts(b.vault.by_type("term") + b.vault.by_type("keyword")),
            issues=issues, lint=lint,
            lint_error_n=sum(len(v) for v in lint["errors"].values()),
            lint_warning_n=sum(len(v) for v in lint["warnings"].values()),
            log_recent=log_entries(b, 5), commits=git_log(repo, 5),
            runner_last=runner.last, review=review, cutover=cutover, gaps=gap,
            link_rows=link_rows, link_summary=_link_summary(link_rows),
            sections_open_issues=sum(r["open_issues"] for r in sections["rows"]),
        )

    @app.route("/sections")
    def sections_page():
        b = model.get()
        view = sections_view(b, runner.parity())
        return render_template("sections.html", counts=view["counts"], rows=view["rows"])

    @app.route("/tips")
    def tips_page():
        b = model.get()
        view = tips_view(b)
        notes = []
        if view["without_related"]:
            notes.append(f"{len(view['without_related'])} without related: " + ", ".join(view["without_related"]))
        if view["legacy"]:
            notes.append(f"{len(view['legacy'])} still carrying legacy-tags: " + ", ".join(view["legacy"]))
        pages = _apply_filters(b, b.vault.by_type("tip"))
        return _list_page("Tips", "tip", _rows(b, pages), view["counts"], notes)

    @app.route("/examples")
    def examples_page():
        b = model.get()
        view = examples_view(b)
        notes = []
        if view["orphan_categories"]:
            notes.append(
                f"{len(view['orphan_categories'])} example categories no section references: "
                + ", ".join(view["orphan_categories"])
            )
        pages = _apply_filters(b, b.vault.by_type("example"))
        return _list_page("Examples", "example", _rows(b, pages), view["counts"], notes)

    @app.route("/faq")
    def faq_page():
        b = model.get()
        view = faq_view(b)
        notes = [view["note"]] if view["note"] else []
        pages = _apply_filters(b, b.vault.by_type("faq"))
        return _list_page("FAQ", "faq", _rows(b, pages), status_counts(b.vault.by_type("faq")), notes)

    @app.route("/terms")
    def terms_page():
        b = model.get()
        view = tags_view(b)
        usage = dict(view["terms"])
        pages = _apply_filters(b, b.vault.by_type("term"))
        rows = _rows(b, pages)
        for r in rows:
            r["usage"] = usage.get(r["slug"], 0)
        notes = []
        if view["incomplete_terms"]:
            notes.append(
                f"{len(view['incomplete_terms'])} without a definition sentence or home: "
                + ", ".join(view["incomplete_terms"])
            )
        return _list_page("Terms", "term", rows, status_counts(b.vault.by_type("term")), notes)

    @app.route("/keywords")
    def keywords_page():
        b = model.get()
        view = tags_view(b)
        usage = dict(view["keywords"])
        pages = _apply_filters(b, b.vault.by_type("keyword"))
        rows = _rows(b, pages)
        for r in rows:
            r["usage"] = usage.get(r["slug"], 0)
        return _list_page("Keywords", "keyword", rows, status_counts(b.vault.by_type("keyword")), [])

    @app.route("/systems")
    def systems_page():
        b = model.get()
        pages = _apply_filters(b, b.vault.by_type("system"))
        return _list_page("Systems", "system", _rows(b, pages), status_counts(b.vault.by_type("system")), [])

    @app.route("/tags")
    def tags_page():
        view = tags_view(model.get())
        return render_template("tags.html", **view)

    @app.route("/issues")
    def issues_page():
        view = issues_view(model.get())
        return render_template("issues.html", open=view["open"], by_severity=view["by_severity"],
                                by_kind=view["by_kind"])

    @app.route("/lint")
    def lint_page():
        b = model.get()
        view = lint_view(b)
        return render_template("lint.html", errors=view["errors"], warnings=view["warnings"],
                                known=set(b.vault.pages))

    @app.route("/log")
    def log_page():
        b = model.get()
        return render_template("log.html", entries=log_entries(b, 5), commits=git_log(repo, 10))

    @app.route("/review")
    def review_page():
        view = review_queue(model.get())
        return render_template("review.html", pages=view["pages"], checklist=view["checklist"])

    @app.route("/cutover")
    def cutover_page():
        view = readiness(model.get(), runner.parity())
        return render_template("cutover.html", rows=view["rows"], next=view["next"])

    @app.route("/gaps")
    def gaps_page():
        return render_template("gaps.html", **gaps(model.get()))

    @app.route("/page/<slug>")
    def page_detail(slug):
        b = model.get()
        page = b.vault.pages.get(slug)
        if page is None:
            abort(404)
        known = set(b.vault.pages)
        return render_template(
            "page.html", page=page, body_html=render(page.body, known), known=known,
            out_links=links_out(b, slug), in_links=links_in(b, slug),
            source_links=sorted(l.target for l in page.links_in("sources")),
            issues=issues_naming(b, slug), obsidian=obsidian_url(b, page),
        )

    @app.route("/ping", methods=["POST"])
    def ping():
        return presence.ping(client_id(request))

    @app.route("/leaving", methods=["POST"])
    def leaving():
        presence.leaving(client_id(request))
        return "", 204

    @app.route("/who")
    def who():
        return render_template("who.html", entries=presence.who())

    return app


# Module-level factory target for gunicorn ("app:create_app()"); no eager
# instance here, since create_app() needs BRAIN_REPO to be set at call time.
app = None
