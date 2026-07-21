// Site search: lunr.js index over sections, tips, and examples.
// Incremental panel below the sidebar box (top hits only); the full
// result list lives on /search/. Ranking: exact > prefix > fuzzy,
// title > tags > content, sections slightly ahead of the rest.
(function () {
    'use strict';

    var input = document.getElementById('search');
    if (!input || !input.form) return;

    var form = input.form;
    var baseurl = form.getAttribute('data-baseurl') || '';
    var pagePane = document.getElementById('search-page-results');

    var PANEL_LIMIT = 6;
    var TYPE_LABELS = { section: 'Section', tip: 'Tip', example: 'Example', page: 'Page' };

    var idx = null;
    var byRef = null;
    var loading = null;

    function loadScript(src) {
        return new Promise(function (resolve, reject) {
            var s = document.createElement('script');
            s.src = src;
            s.onload = resolve;
            s.onerror = reject;
            document.head.appendChild(s);
        });
    }

    function normalizeTags(tags) {
        if (Array.isArray(tags)) return tags.join(' ');
        return tags || '';
    }

    // Section pages arrive unrendered: scrub Liquid tags and markdown
    // syntax so neither pollutes the index or the visible excerpts.
    function cleanContent(text) {
        return (text || '')
            .replace(/\{%.*?%\}/g, ' ')
            .replace(/\{\{.*?\}\}/g, ' ')
            .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ')
            .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
            .replace(/[#*_`|>]+/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
    }

    // Loaded lazily on first focus so readers who never search pay nothing.
    function ensureIndex() {
        if (!loading) {
            loading = loadScript(baseurl + '/assets/lib/lunr/lunr.min.js')
                .then(function () { return fetch(baseurl + '/search.json'); })
                .then(function (res) {
                    if (!res.ok) throw new Error('search.json ' + res.status);
                    return res.json();
                })
                .then(function (docs) {
                    byRef = {};
                    idx = lunr(function () {
                        this.ref('url');
                        this.field('title', { boost: 10 });
                        this.field('tags', { boost: 5 });
                        this.field('author');
                        this.field('content');
                        docs.forEach(function (d) {
                            d.content = cleanContent(d.content);
                            byRef[d.url] = d;
                            this.add({
                                url: d.url,
                                title: d.title || '',
                                tags: normalizeTags(d.tags),
                                author: d.author || '',
                                content: d.content || ''
                            }, { boost: d.type === 'section' ? 2 : 1 });
                        }, this);
                    });
                });
        }
        return loading;
    }

    // Three-tier query: exact (stemmed) beats prefix beats fuzzy.
    // Wildcard/fuzzy clauses skip the pipeline: stemming a prefix breaks it.
    function runQuery(raw, fields) {
        var tokens = lunr.tokenizer(raw).map(String);
        if (!tokens.length) return [];
        function clause(opts) {
            if (fields) opts.fields = fields;
            return opts;
        }
        return idx.query(function (q) {
            tokens.forEach(function (t) {
                q.term(t, clause({ boost: 100 }));
                q.term(t, clause({ boost: 10, usePipeline: false, wildcard: lunr.Query.wildcard.TRAILING }));
                if (t.length > 3) {
                    q.term(t, clause({ boost: 1, usePipeline: false, editDistance: t.length > 5 ? 2 : 1 }));
                }
            });
        });
    }

    function typeBadge(type) {
        var b = document.createElement('span');
        b.className = 'search-type search-type-' + (TYPE_LABELS[type] ? type : 'page');
        b.textContent = TYPE_LABELS[type] || 'Page';
        return b;
    }

    // ---- incremental panel under the sidebar box ----

    var panel = document.createElement('div');
    panel.className = 'search-panel';
    panel.id = 'search-panel';
    panel.hidden = true;
    form.insertAdjacentElement('afterend', panel);

    input.setAttribute('role', 'combobox');
    input.setAttribute('aria-expanded', 'false');
    input.setAttribute('aria-controls', 'search-panel');
    input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('autocomplete', 'off');

    var options = [];
    var active = -1;

    function closePanel() {
        panel.hidden = true;
        options = [];
        active = -1;
        input.setAttribute('aria-expanded', 'false');
        input.removeAttribute('aria-activedescendant');
    }

    function renderPanel(results, raw) {
        panel.textContent = '';
        options = [];
        active = -1;
        if (!results.length) {
            var none = document.createElement('p');
            none.className = 'search-panel-empty';
            none.textContent = 'No matches for “' + raw + '”';
            panel.appendChild(none);
        } else {
            var list = document.createElement('ul');
            list.setAttribute('role', 'listbox');
            results.slice(0, PANEL_LIMIT).forEach(function (r, i) {
                var d = byRef[r.ref];
                var li = document.createElement('li');
                li.setAttribute('role', 'option');
                li.setAttribute('aria-selected', 'false');
                li.id = 'search-option-' + i;
                var a = document.createElement('a');
                a.href = baseurl + d.url;
                a.appendChild(typeBadge(d.type));
                var title = document.createElement('span');
                title.className = 'search-hit-title';
                title.textContent = d.title;
                a.appendChild(title);
                li.appendChild(a);
                list.appendChild(li);
                options.push(li);
            });
            panel.appendChild(list);
            var all = document.createElement('a');
            all.className = 'search-panel-all';
            all.href = baseurl + '/search/?q=' + encodeURIComponent(raw);
            all.textContent = results.length > PANEL_LIMIT
                ? 'All ' + results.length + ' results'
                : 'Open results page';
            panel.appendChild(all);
        }
        panel.hidden = false;
        input.setAttribute('aria-expanded', 'true');
    }

    function setActive(next) {
        active = next;
        options.forEach(function (li, i) {
            li.classList.toggle('is-active', i === active);
            li.setAttribute('aria-selected', i === active ? 'true' : 'false');
        });
        if (active >= 0) {
            input.setAttribute('aria-activedescendant', options[active].id);
        } else {
            input.removeAttribute('aria-activedescendant');
        }
    }

    var timer = null;

    input.addEventListener('focus', function () {
        ensureIndex();
    });

    input.addEventListener('input', function () {
        var raw = input.value.trim();
        clearTimeout(timer);
        if (raw.length < 2) {
            closePanel();
            return;
        }
        timer = setTimeout(function () {
            ensureIndex()
                .then(function () { renderPanel(runQuery(raw), raw); })
                .catch(closePanel);
        }, 150);
    });

    input.addEventListener('keydown', function (e) {
        if (panel.hidden || !options.length) return;
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            setActive((active + 1) % options.length);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            setActive((active - 1 + options.length) % options.length);
        } else if (e.key === 'Enter') {
            if (active >= 0) {
                e.preventDefault();
                window.location.href = options[active].querySelector('a').href;
            }
            // No active option: let the form submit to /search/.
        } else if (e.key === 'Escape') {
            closePanel();
        }
    });

    document.addEventListener('click', function (e) {
        if (e.target !== input && !panel.contains(e.target)) closePanel();
    });

    // ---- full results on /search/ ----

    function excerpt(content, raw) {
        if (!content) return '';
        var probe = raw.split(/\s+/)[0].toLowerCase();
        var pos = content.toLowerCase().indexOf(probe);
        if (pos < 0) {
            return content.slice(0, 160) + (content.length > 160 ? '…' : '');
        }
        var start = Math.max(0, pos - 60);
        var end = Math.min(content.length, pos + 100);
        return (start > 0 ? '…' : '') + content.slice(start, end)
            + (end < content.length ? '…' : '');
    }

    function renderPage(results, raw) {
        pagePane.textContent = '';
        var count = document.createElement('p');
        count.className = 'search-count';
        count.textContent = (results.length === 1 ? '1 result' : results.length + ' results')
            + ' for “' + raw + '”';
        pagePane.appendChild(count);
        results.forEach(function (r) {
            var d = byRef[r.ref];
            var hit = document.createElement('div');
            hit.className = 'search-hit';
            var h = document.createElement('h2');
            h.appendChild(typeBadge(d.type));
            var a = document.createElement('a');
            a.href = baseurl + d.url;
            a.textContent = d.title;
            h.appendChild(a);
            hit.appendChild(h);
            var ex = excerpt(d.content, raw);
            if (ex) {
                var p = document.createElement('p');
                p.className = 'search-excerpt';
                p.textContent = ex;
                hit.appendChild(p);
            }
            var metaParts = [];
            if (d.date) metaParts.push(d.date);
            var tagText = normalizeTags(d.tags);
            if (tagText) metaParts.push(tagText);
            if (metaParts.length) {
                var meta = document.createElement('p');
                meta.className = 'search-meta';
                meta.textContent = metaParts.join(' · ');
                hit.appendChild(meta);
            }
            pagePane.appendChild(hit);
        });
    }

    if (pagePane) {
        var params = new URLSearchParams(window.location.search);
        var q = params.get('q');
        var t = params.get('t');
        var author = params.get('a');
        var raw = q || t || author || '';
        var fields = q ? null : (t ? ['tags'] : (author ? ['author'] : null));
        if (raw) {
            input.value = raw;
            ensureIndex()
                .then(function () { renderPage(runQuery(raw, fields), raw); })
                .catch(function () {
                    var err = document.createElement('p');
                    err.textContent = 'Search is unavailable right now. Please use the section navigation instead.';
                    pagePane.appendChild(err);
                });
        } else {
            var hint = document.createElement('p');
            hint.className = 'search-count';
            hint.textContent = 'Type into the search box to find sections, tips, and examples.';
            pagePane.appendChild(hint);
            ensureIndex();
        }
    }
})();
