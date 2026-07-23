# Training dates: integration concept

**Status:** proposal · **Date:** 2026-07-23 · **Scope:** trainings.arc42.org (source),
docs.arc42.org, faq.arc42.org, and any future arc42 site that shows course dates.

---

## 1. Why

The arc42 trainings fund the free arc42 sites, so the course offer has to be visible on
them. Today that visibility is arranged like this:

```
                  browser of every visitor
                            │
   docs.arc42.org ──────────┤ loads htmx (14 KB, unpkg)
                            └─→ GET arc42-subtle-ads-backend.vercel.app/api
                                 └─→ returns an HTML fragment, swapped into the page
```

That has five problems, and only the first is about performance.

1. **Every page pays for it.** ~200 pages on docs alone each pull a third-party script
   from unpkg and then make a second third-party request.
2. **The dates are invisible to search engines** and to readers without JavaScript. A page
   advertising courses contains no courses in its HTML.
3. **Failure is silent.** If the backend is slow or down, every visitor quietly sees a
   generic fallback and no maintainer finds out.
4. **The payload is HTML carrying one site's markup.** The fragment ships `<h3>`, `<h4>`
   and `class="subtle-ad"`. Whichever site embeds it inherits docs.arc42.org's markup
   contract; a CSS change on one site can break the block on another.
5. **No review, no history.** Whoever can deploy the backend can change content on ~200
   pages of docs.arc42.org instantly, with no commit, no diff, and no way to revert.

Point 5 is the one that should decide this. For an open-source, community-maintained set of
sites, content that appears sitewide belongs in version control.

### The i18n problem, concretely

Most public arc42 courses are held in German; the documentation sites are written in English
and read internationally. The source data does not currently express this. Of the four
courses the backend returned on 2026-07-23:

| Course | Language marker in the payload |
|---|---|
| iSAQB Advanced Topics | `(in German)` in the heading |
| IMPROVE | "Next available dates (in English)" |
| Req4Arc | none — dates are Frankfurt/Main, München, Mannheim |
| ADOC | none — "Ort: Zürich", German trainer line |

Three different conventions and two silent cases. A reader in Spain cannot tell from this
which courses they could actually attend. **Language must become a field, not a prose
convention.** That is the single most valuable change in this document.

---

## 2. Target architecture

One source of truth for the *facts*; each site owns its *presentation*.

```
   trainings.arc42.org  (or the trainings repo)
            │
            │  publishes  trainings.json      ← the contract in §3
            ▼
   ┌────────────────────────────────────────────────┐
   │  scheduled GitHub Action, one per consuming    │
   │  site: fetch → validate → commit if changed    │
   └────────────────────────────────────────────────┘
            │                │                │
            ▼                ▼                ▼
     docs.arc42.org    faq.arc42.org    (future site)
     _data/trainings   _data/trainings   _data/trainings
            │                │                │
     own template      own template      own template
     own CSS           own CSS           own CSS
```

Key property: **JSON crosses the boundary, never HTML.** Each site renders the same facts
in its own design system. docs can show a compact block on its home page and a full dated
list on section pages; faq can show something else entirely; neither can break the other.

### Why pull, not push

The alternative is the trainings repo pushing to each consumer on change (`repository_dispatch`).
Pull is better here:

- consumers stay independent — a new site self-serves, the source needs no change and no
  knowledge of who consumes it
- no cross-repo tokens to provision, rotate, or leak
- a consumer that is broken or archived cannot fail the source's release

Pull costs latency (up to one polling interval). For dates announced months ahead that is
irrelevant, and `workflow_dispatch` covers "publish this now".

---

## 3. The contract: `trainings.json`

The whole integration rests on this file. It should be published at a stable URL, e.g.
`https://trainings.arc42.org/api/trainings.json`, with `content-type: application/json` and
permissive CORS (already the case today).

```jsonc
{
  "$schema": "https://trainings.arc42.org/api/trainings.schema.json",
  "generated": "2026-07-22T09:14:00Z",   // ISO 8601 UTC — lets consumers show "dates as of"
  "courses": [
    {
      "id": "req4arc",                    // stable slug; consumers may key off it
      "title": "Req4Arc: Getting your Requirements right",
      "blurb": "What to do if your requirements need improvement.",
      "url": "https://trainings.arc42.org/req4arc",
      "certification": "iSAQB CPSA-F",    // optional, null when none
      "dates": [
        {
          "start": "2026-09-15",          // ISO 8601. NOT "15.-17. September 2026" —
          "end":   "2026-09-17",          //   consumers must be able to sort and expire
          "city":  "Frankfurt am Main",
          "country": "DE",                // ISO 3166-1 alpha-2
          "language": "de",               // ISO 639-1. REQUIRED. See §3.1
          "format": "public",             // public | inhouse | online
          "trainers": ["Peter Hruschka", "Gernot Starke"],
          "url": "https://trainings.arc42.org/req4arc/2026-09-frankfurt",
          "status": "open"                // open | waitlist | full | cancelled
        }
      ]
    }
  ]
}
```

### 3.1 `language` is required — no default

Every date carries `language`. There is deliberately **no fallback to German**: a missing
value is a validation error at the source, not something a consumer guesses. A wrong guess
is worse than a loud failure, because it sends someone to a course they cannot follow.

Consumers render it as a visible marker, never as colour alone:

> **DE** 15–17 Sep 2026 · Frankfurt am Main · Peter Hruschka, Gernot Starke

This is what makes the offer honest for an international readership, and it is why the
schema is worth the hour it costs.

### 3.2 Rules for consumers

- **Expire client-side.** Filter out dates whose `end` is in the past, so a stale file
  degrades to "fewer dates" rather than to "advertising a course that already happened".
- **Never show `cancelled`.** Show `full`/`waitlist` only if the linked page can accept a
  waitlist registration.
- **Cap the list.** Docs shows at most the next two dates per course and links out for the
  rest. A schedule is not documentation.
- **Always link out.** Every course and date links to the trainings site, which owns
  booking, price, and the fine print.

### 3.3 Compatibility

Additive changes (new optional fields) do not require consumer changes. A breaking change
means a new path (`/api/v2/trainings.json`), with the old path served for at least one
quarter. Consumers pin the path they read.

---

## 4. Rollout

### Phase 1 — build-time fetch of today's HTML *(done, ready to merge)*

`.github/workflows/refresh-trainings.yml` on docs.arc42.org. Weekly (Monday 04:17 UTC) plus
manual dispatch. It fetches the existing endpoint, **validates the payload**, writes
`_includes/generated/trainings.html`, and commits only when the content changed.

The validation step is not ceremony. `curl --fail` catches 4xx/5xx, but a CDN or platform
error page arrives as **200**; without a content check the job would commit an outage notice
to the foot of every section page. Hence: non-empty, contains `subtle-ad`, over 400 bytes.

This solves problems 1, 2, 3 and 5 for docs.arc42.org, today, with no change at the source.
It does **not** solve problem 4 or the i18n problem — it still moves HTML, and the language
data still isn't there.

Requires: one seed copy of `_includes/generated/trainings.html` committed before merge, as
Jekyll's `include` fails the build on a missing file.

### Phase 2 — publish `trainings.json`

At the source. Same data, second serializer; the HTML endpoint keeps working unchanged, so
nothing breaks while consumers migrate. Ship the schema alongside it and validate in the
trainings repo's own CI, so a missing `language` fails there rather than surfacing as a
wrong badge on three websites.

### Phase 3 — consumers switch to JSON

Each site changes its workflow to write `_data/trainings.json` and adds a template. On docs
that is roughly:

```liquid
{%- assign today = 'now' | date: '%Y-%m-%d' -%}
{%- for course in site.data.trainings.courses -%}
  <h4>{{ course.title }}</h4>
  <ul>
  {%- assign upcoming = course.dates | where_exp: "d", "d.end >= today" -%}
  {%- for d in upcoming limit: 2 -%}
    <li>
      <b class="lang-badge">{{ d.language | upcase }}</b>
      <a href="{{ d.url }}">{{ d.start | date: "%-d %b" }}–{{ d.end | date: "%-d %b %Y" }}</a>
      · {{ d.city }} · {{ d.trainers | join: ", " }}
    </li>
  {%- endfor -%}
  </ul>
{%- endfor -%}
```

Then htmx and the runtime fetch are deleted from every consumer.

### Phase 4 — retire the HTML endpoint

Once no consumer requests it for a full quarter.

---

## 5. Operational notes

**Pages rebuild.** docs.arc42.org publishes through GitHub Pages' build-from-branch
integration, so the workflow's push rebuilds the site. If Pages is ever switched to the
"GitHub Actions" source, note that pushes made with `GITHUB_TOKEN` deliberately do **not**
trigger further workflows (loop prevention); the deploy would then need a PAT or a
build-and-deploy step in the same job. Same caveat applies to faq.arc42.org — check which
mode it uses before copying the workflow.

**Commit noise.** The `git diff --quiet` guard means a week with no schedule change produces
no commit at all. When one does appear it is a genuine, reviewable record of what changed
and when.

**Monitoring.** A failed run mails the repository admins. That is the intended alerting: a
broken source becomes a maintainer's problem instead of a visitor's.

**Staleness.** Worst case seven days. Acceptable for courses announced months ahead, and
`workflow_dispatch` publishes immediately when it isn't.

**Forks.** The workflow is guarded on `github.repository`, so forks never run it and fork
owners never get failure mail.

---

## 6. Open questions for the arc42 team

1. **Where does the JSON live** — generated by the existing Vercel backend, or committed in
   a `arc42/trainings` repo and served from Pages? The repo option makes the schedule itself
   reviewable and gives the source the same governance benefit consumers get.
2. **Does faq.arc42.org build on Jekyll and Pages** the same way? If so the workflow copies
   across unchanged; if it is a different generator, only the template differs.
3. **Who owns the schema** — suggest it lives with the source and is versioned with it.
4. **Should in-house-only courses appear at all** on the documentation sites, given they
   have no public dates? Currently they are mentioned in prose but have nothing to link to.
5. **Is `trainings.arc42.org` or `arc42.de/termine` the canonical destination?** Both are
   linked from the current block; the sites should agree on one.
