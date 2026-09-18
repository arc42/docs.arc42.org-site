"""Flask app factory for the docs-arc42-brain dashboard.

Routes only; keep this file under 300 lines. All view data comes from
`model` / `relations`; nothing here re-derives vault logic. Everything else
(model, presence, generate runner, link checker) is injected as `services`
and stashed on `app.extensions["brain"]`.
"""
from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request
from markupsafe import Markup

from actions import Runner
from linkcheck import LinkChecker, link_summary
from model import (
    STATUSES, Model, examples_view, faq_view, gaps, issues_touching_sections,
    issues_view, lint_view, list_rows, log_entries, git_log, readiness,
    review_queue, sections_view, status_counts, tags_view, tips_view,
)
from presence import Presence
from relations import (
    group_links, link_graph, links_in, links_out, obsidian_url, search,
    suggestions, term_graph,
)
from render import render, render_meta
from routes_live import bp as actions_bp


def _fmt_meta(value, known=None):
    """A front-matter value as safe HTML: wikilinks resolved via
    `render.render_meta`, everything else escaped — never a raw
    `[[wikilink]]` or a python repr. Marked safe since `render_meta` already
    escapes anything it doesn't turn into a link."""
    return Markup(render_meta(value, known or set()))


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
    linkchecker: LinkChecker = app.extensions["brain"]["linkchecker"]

    app.register_blueprint(actions_bp)

    def _section_arg():
        """The `section` query arg as an int, or None (missing/not a number
        is "no filter", matching the list-page filter form)."""
        raw = request.args.get("section")
        if not raw:
            return None
        try:
            return int(raw)
        except ValueError:
            return None

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

    def _filtered_rows(b, ptype):
        return list_rows(
            b, ptype,
            status=request.args.get("status") or None,
            section=_section_arg(),
            system=request.args.get("system") or None,
        )

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
            link_rows=link_rows, link_summary=link_summary(link_rows),
            sections_open_issues=issues_touching_sections(b),
            statuses=STATUSES,
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
        return _list_page("Tips", "tip", _filtered_rows(b, "tip"), view["counts"], notes)

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
        return _list_page("Examples", "example", _filtered_rows(b, "example"), view["counts"], notes)

    @app.route("/faq")
    def faq_page():
        b = model.get()
        view = faq_view(b)
        notes = [view["note"]] if view["note"] else []
        return _list_page("FAQ", "faq", _filtered_rows(b, "faq"), status_counts(b.vault.by_type("faq")), notes)

    @app.route("/terms")
    def terms_page():
        b = model.get()
        view = tags_view(b)
        usage = dict(view["terms"])
        rows = _filtered_rows(b, "term")
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
        rows = _filtered_rows(b, "keyword")
        for r in rows:
            r["usage"] = usage.get(r["slug"], 0)
        return _list_page("Keywords", "keyword", rows, status_counts(b.vault.by_type("keyword")), [])

    @app.route("/systems")
    def systems_page():
        b = model.get()
        return _list_page("Systems", "system", _filtered_rows(b, "system"),
                           status_counts(b.vault.by_type("system")), [])

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

    @app.route("/suggestions")
    def suggestions_page():
        return render_template("suggestions.html", suggestions=suggestions(model.get()))

    @app.route("/graph")
    def graph_page():
        kind = request.args.get("kind", "links")
        if kind not in ("links", "terms"):
            kind = "links"
        return render_template("graph.html", kind=kind)

    @app.route("/graph.json")
    def graph_json():
        kind = request.args.get("kind", "links")
        b = model.get()
        return jsonify(term_graph(b) if kind == "terms" else link_graph(b))

    @app.route("/search")
    def search_page():
        q = request.args.get("q", "").strip()
        results = search(model.get(), q) if q else []
        return render_template("search.html", q=q, results=results)

    @app.route("/page/<slug>")
    def page_detail(slug):
        b = model.get()
        page = b.vault.pages.get(slug)
        if page is None:
            abort(404)
        known = set(b.vault.pages)
        return render_template(
            "page.html", page=page, body_html=render(page.body, known), known=known,
            out_groups=group_links(b, links_out(b, slug)),
            in_groups=group_links(b, links_in(b, slug)),
            obsidian=obsidian_url(b, page),
        )

    return app


# Module-level factory target for gunicorn ("app:create_app()"); no eager
# instance here, since create_app() needs BRAIN_REPO to be set at call time.
app = None
