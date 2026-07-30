// ============================================================================
// site.js — every behaviour on the site that is not search.
//
// Replaces four files and 90KB of dependency: jQuery 3.7.1, the garand-sticky
// plugin, assets/js/script.js and assets/js/header-link.js. It is plain ES5,
// has no dependencies and no build step, and is loaded with `defer`.
//
// What was dropped on the way, and why:
//
//   · the sticky plugin was initialised against `.site-aside .sticky`. There is
//     no element with class `sticky` anywhere in the repository, so it had been
//     doing nothing for as long as it has been loaded. Sticky columns are
//     `position: sticky` in CSS now.
//
//   · script.js set `rel` on external links by passing "noopener" as a THIRD
//     argument to jQuery's .attr(name, value). jQuery ignores it. Every
//     external link on this site has therefore been opening in a new tab with a
//     live window.opener reference for years. That is fixed below, and it is a
//     real fix rather than a port.
//
//   · script.js focused the search box on ANY keyup of `/`, including while the
//     reader was typing a slash into a form field. Guarded now.
//
// What is new: the on-page TOC is built and tracked here (nothing in the HTML
// hardcodes an entry or an active state), and the inline <details> TOC is moved
// under the page <h1> and opened when the viewport can afford it.
// ============================================================================

(function () {
    'use strict';

    var main = document.getElementById('main-content') || document.querySelector('main');
    if (!main) return;

    var reduceMotion = window.matchMedia
        ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
        : false;

    // Callout headings are h2 in the markdown ("## Content", "## Motivation",
    // "## Form" inside <div class="arc42-help">). They are labels inside a box,
    // not landmarks on the page, and section 10 alone has seven of them. The TOC
    // lists only headings that belong to the document itself.
    var EXCLUDED_ANCESTORS = '.arc42-help, .arc42-example, .example-list, .toc, .toc-inline';

    // ---- small helpers ------------------------------------------------------

    function toArray(nodeList) {
        return Array.prototype.slice.call(nodeList);
    }

    function inExcluded(el) {
        return el.closest ? !!el.closest(EXCLUDED_ANCESTORS) : false;
    }

    // The sprite lives at /assets/icons/ui.svg, but site.baseurl can move it.
    // Rather than hardcode a path that would silently 404, read the base off any
    // <use> the Liquid include has already rendered on this page.
    function spriteHref(name) {
        var existing = document.querySelector('svg use[href]');
        var base = existing
            ? String(existing.getAttribute('href')).split('#')[0]
            : '/assets/icons/ui.svg';
        return base + '#' + name;
    }

    // "3.1 Business context" → ["3.1", "Business context"].
    // "Practical Tips"       → ["",    "Practical Tips"].
    // The number column is rendered either way so that the labels line up; an
    // unnumbered entry starting 2em left of its neighbours reads as a mistake.
    function splitNumber(text) {
        var m = /^\s*([0-9]+(?:\.[0-9]+)*\.?)\s+(.*)$/.exec(text);
        if (m) return [m[1].replace(/\.$/, ''), m[2]];
        return ['', text.replace(/^\s+|\s+$/g, '')];
    }

    // The condensed masthead bar overlaps anything scrolled to the top of the
    // viewport, so both the anchor offset and the scroll-spy threshold have to
    // clear it. --bar-h is the token that defines its height.
    function barHeight() {
        var raw = getComputedStyle(document.documentElement).getPropertyValue('--bar-h');
        var n = parseInt(raw, 10);
        return isNaN(n) ? 56 : n;
    }

    // ========================================================================
    // 1. Permalink anchors on headings
    // ========================================================================
    // From header-link.js, which used jQuery and a FontAwesome <i>. h1 is left
    // alone: a permalink to the top of the page you are already on is noise.

    (function headingAnchors() {
        var headings = toArray(main.querySelectorAll('h2[id], h3[id], h4[id], h5[id], h6[id]'));
        var href = spriteHref('link');

        headings.forEach(function (h) {
            if (h.querySelector('.header-link')) return;
            // Not on the "Content / Motivation / Form" labels inside a callout:
            // section 10 repeats "Content" three times, kramdown numbers the
            // duplicates content-1 and content-2, and a permalink to a label is
            // not a link anybody wants to copy.
            if (inExcluded(h)) return;

            var a = document.createElement('a');
            // Two classes on purpose: `.header-link` is the scripted one styled
            // in _content.scss; `a.headerlink` is the hand-written class used in
            // _examples content and coloured in _utilities.scss. Carrying both
            // means the anchor looks the same however it got onto the page.
            a.className = 'header-link headerlink';
            a.href = '#' + h.id;
            a.setAttribute('aria-label', 'Permalink to “' + h.textContent.trim() + '”');
            a.innerHTML = '<svg class="icon icon--link" aria-hidden="true" focusable="false">'
                + '<use href="' + href + '"></use></svg>';
            h.appendChild(a);
        });
    })();

    // ========================================================================
    // 1b. Scrollable, keyboard-reachable table wrappers
    // ========================================================================
    // Content tables are hand-written Markdown, so no wrapper exists in the
    // source. _content.scss styles `.table-scroll` (thin scrollbar, edge fade,
    // inset focus ring) and sets `min-width: 32rem` on the table INSIDE it —
    // without this pass none of that ever applies, and at 390px roughly 244px
    // of a context table is simply cut off with no way to reach it.
    //
    // tabindex="0" is the accessibility point: an overflow container that is
    // not focusable cannot be scrolled by keyboard at all (WCAG 2.1.1).

    (function scrollableTables() {
        toArray(main.querySelectorAll('table')).forEach(function (table, i) {
            var parent = table.parentNode;
            if (!parent || parent.className.indexOf('table-scroll') !== -1) return;

            var wrap = document.createElement('div');
            wrap.className = 'table-scroll';
            wrap.setAttribute('tabindex', '0');
            wrap.setAttribute('role', 'region');

            // Prefer the table's own caption as the accessible name; it is the
            // one string an author already wrote to describe this table.
            var caption = table.querySelector('caption');
            var name = caption && caption.textContent.trim();
            wrap.setAttribute('aria-label', name || 'Table ' + (i + 1));

            parent.insertBefore(wrap, table);
            wrap.appendChild(table);
        });
    })();

    // ========================================================================
    // 2. On-page TOC: build, then scroll-spy
    // ========================================================================

    (function tableOfContents() {
        var aside = document.querySelector('.toc');
        var details = document.getElementById('toc-inline');
        if (!aside && !details) return;

        var subheads = toArray(main.querySelectorAll('h2[id]')).filter(function (h) {
            return !inExcluded(h);
        });

        var layout = document.querySelector('.layout--doc');

        if (!subheads.length) {
            // No entries: do not leave a 240px column of nothing beside the
            // prose, and do not show an empty grey disclosure box either. The
            // gate counts h2s only — the title added below must never be the
            // thing that keeps an otherwise empty TOC on the page.
            if (layout) layout.classList.add('has-no-toc');
            return;
        }

        // The section title leads the list. Eight of the twelve arc42 sections
        // keep every subheading inside .arc42-help, which is excluded above, so
        // their TOC listed one entry — "Practical Tips" — naming the appendix at
        // the foot of the page and never the page itself. The h1 gives the box a
        // subject, and a way back to the top once the reader has scrolled off it.
        var title = main.querySelector('h1[id]');
        var headings = title ? [title].concat(subheads) : subheads;

        var links = [];   // every <a> in both lists, in document order

        function buildList(ol, extraLinkClass) {
            headings.forEach(function (h) {
                var parts = splitNumber(h.textContent);
                var li = document.createElement('li');
                if (h === title) li.className = 'is-title';
                var a = document.createElement('a');
                a.href = '#' + h.id;
                if (extraLinkClass) a.className = extraLinkClass;

                // The number stays in the accessible name. "5.1 Whitebox
                // Overall System / 5.2 Level 2 / 5.3 Level 3" read aloud
                // without their numbers would be three unrelated phrases.
                var num = document.createElement('span');
                num.className = 'toc-num';
                num.textContent = parts[0];

                a.appendChild(num);
                a.appendChild(document.createTextNode(' ' + parts[1]));
                li.appendChild(a);
                ol.appendChild(li);

                links.push({ id: h.id, a: a });
            });
        }

        var asideList = aside && aside.querySelector('.toc-list');
        if (asideList) {
            buildList(asideList);
            aside.classList.add('is-ready');
        }

        if (details) {
            var inlineList = details.querySelector('.toc-inline-list');
            if (inlineList) buildList(inlineList);
            details.classList.add('is-ready');

            // Sit under the <h1>, not above it. The heading comes from the
            // markdown, so Liquid cannot get between the title and the body; the
            // include is emitted first and moved here. Above the heading it read
            // as a table of contents for the site rather than for this page.
            var h1 = main.querySelector('h1');
            if (h1 && h1.parentNode) {
                h1.parentNode.insertBefore(details, h1.nextSibling);
            }

            // Open by default wherever there is vertical room for it. The mockup
            // left it shut, so between 800 and 1100px — a laptop window with a
            // screenful of space going spare — the reader had no page map at all
            // unless they thought to click for one.
            var wide = window.matchMedia ? window.matchMedia('(min-width: 641px)') : null;
            var programmatic = false;
            var userDecided = false;

            function setOpen(value) {
                if (details.open === value) return;
                programmatic = true;
                details.open = value;
            }

            details.addEventListener('toggle', function () {
                if (programmatic) { programmatic = false; return; }
                userDecided = true;
            });

            setOpen(wide ? wide.matches : true);

            if (wide) {
                var onChange = function () {
                    if (!userDecided) setOpen(wide.matches);
                };
                if (wide.addEventListener) wide.addEventListener('change', onChange);
                else if (wide.addListener) wide.addListener(onChange);
            }
        }

        // ---- scroll-spy -----------------------------------------------------
        // IntersectionObserver is the trigger; a geometry read is the decision.
        // Observing alone cannot answer "which section am I in" when several
        // headings are on screen at once or when none is, which is the normal
        // case on this site: section 1 carries 24 tips under one h2, so a reader
        // can spend an entire screenful of scrolling inside a single entry with
        // no heading visible anywhere. Scanning for the last heading above the
        // threshold line always has an answer.

        var activeId = null;

        function setActive(id) {
            if (id === activeId) return;
            activeId = id;

            var activeAnchor = null;
            links.forEach(function (link) {
                if (link.id === id) {
                    link.a.setAttribute('aria-current', 'location');
                    if (asideList && asideList.contains(link.a)) activeAnchor = link.a;
                } else {
                    link.a.removeAttribute('aria-current');
                }
            });

            keepInView(activeAnchor);
        }

        // The pane scrolls now (it has to; see _toc.scss), so on a long page the
        // active entry can be outside it. Scroll the pane, never the page —
        // scrollIntoView() would drag the document along with it.
        function keepInView(anchor) {
            if (!anchor || !aside) return;
            if (aside.scrollHeight <= aside.clientHeight) return;

            var box = aside.getBoundingClientRect();
            var row = anchor.getBoundingClientRect();
            var delta = 0;

            if (row.top < box.top + 8) delta = row.top - box.top - 8;
            else if (row.bottom > box.bottom - 8) delta = row.bottom - box.bottom + 8;
            if (!delta) return;

            if (aside.scrollTo && !reduceMotion) {
                aside.scrollTo({ top: aside.scrollTop + delta, behavior: 'smooth' });
            } else {
                aside.scrollTop += delta;
            }
        }

        function update() {
            var line = barHeight() + 24;
            var current = headings[0];

            for (var i = 0; i < headings.length; i++) {
                if (headings[i].getBoundingClientRect().top - line <= 0) current = headings[i];
                else break;
            }

            // At the foot of the document the last heading may never reach the
            // threshold line — a short closing section would otherwise be the one
            // entry the TOC could never highlight.
            var scrolled = window.pageYOffset || document.documentElement.scrollTop;
            var atBottom = scrolled + window.innerHeight
                >= document.documentElement.scrollHeight - 4;
            if (atBottom) current = headings[headings.length - 1];

            setActive(current.id);
        }

        var queued = false;
        function schedule() {
            if (queued) return;
            queued = true;
            var run = function () {
                queued = false;
                update();
            };
            if (window.requestAnimationFrame) window.requestAnimationFrame(run);
            else window.setTimeout(run, 16);
        }

        if (window.IntersectionObserver) {
            var observer = new IntersectionObserver(schedule, {
                rootMargin: '-' + barHeight() + 'px 0px 0px 0px',
                threshold: [0, 1]
            });
            headings.forEach(function (h) { observer.observe(h); });
        }

        // Covers the two cases the observer cannot see: reaching the bottom of
        // the page, and long scrolls that never cross a heading edge.
        window.addEventListener('scroll', schedule, { passive: true });
        window.addEventListener('resize', schedule);
        update();
    })();

    // ========================================================================
    // 3. Rail toggle
    // ========================================================================
    // Contract with _layouts/default.html: a .rail-toggle button carrying
    // aria-controls, and the panel it names. Class `open`, aria-expanded flipped
    // together — the attribute is what a screen reader reads, the class is what
    // CSS sees, and they must never disagree.

    (function railToggle() {
        var btn = document.querySelector('.rail-toggle');
        if (!btn) return;

        var panel = document.getElementById(btn.getAttribute('aria-controls') || 'rail-body');
        if (!panel) return;

        btn.addEventListener('click', function () {
            var open = panel.classList.toggle('open');
            btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
    })();

    // ========================================================================
    // 4. Keyboard: "/" focuses search, Escape leaves it
    // ========================================================================

    (function searchShortcut() {
        var input = document.getElementById('search');
        if (!input) return;

        function isTyping(el) {
            if (!el) return false;
            if (el.isContentEditable) return true;
            var tag = el.tagName;
            return tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT';
        }

        document.addEventListener('keydown', function (e) {
            if (e.key === '/' && !e.metaKey && !e.ctrlKey && !e.altKey) {
                // The old version fired on any keyup of "/", which meant a
                // reader typing a URL or a regex into a field was yanked out of
                // it mid-word.
                if (isTyping(document.activeElement)) return;
                e.preventDefault();
                input.focus();
                if (input.select) input.select();
                return;
            }

            if (e.key === 'Escape' && document.activeElement === input) {
                // search.js owns the first Escape while its suggestion panel is
                // open; it closes the panel and leaves focus where it is. Only
                // once there is no panel left does Escape mean "let me out".
                if (input.getAttribute('aria-expanded') === 'true') return;
                input.blur();
            }
        });
    })();

    // ========================================================================
    // 5. External links
    // ========================================================================
    // rel="noopener noreferrer" is the point of this block. See the header note:
    // the jQuery version never set rel at all.

    (function externalLinks() {
        toArray(document.querySelectorAll('a[href]')).forEach(function (a) {
            if (a.protocol !== 'http:' && a.protocol !== 'https:') return;
            if (!a.host || a.host === window.location.host) return;
            if (a.hasAttribute('download')) return;

            a.setAttribute('target', '_blank');

            var rel = a.getAttribute('rel') || '';
            if (rel.indexOf('noopener') === -1) rel += ' noopener';
            if (rel.indexOf('noreferrer') === -1) rel += ' noreferrer';
            a.setAttribute('rel', rel.replace(/^\s+|\s+$/g, ''));
        });
    })();

    // ========================================================================
    // 6. Content images: centred, and clickable through to full size
    // ========================================================================
    // Carried over from script.js. Diagrams on this site are routinely wider
    // than the measure and are downscaled to fit, so the full-size file is the
    // only readable version of them.

    (function contentImages() {
        toArray(main.querySelectorAll('img')).forEach(function (img) {
            if (img.classList.contains('emoji') || img.classList.contains('eye-catch')) return;
            if (img.closest && img.closest('a')) return;

            var src = img.getAttribute('src');
            if (!src) return;

            var p = img.closest ? img.closest('p') : null;
            if (p) {
                p.style.textAlign = 'center';
                // Mark the paragraph ONLY when the image is all it holds. CSS
                // releases such a paragraph from the reading measure so diagrams
                // can use the full column — but `p:has(> img)` cannot express
                // "image-only", and kramdown happily emits paragraphs carrying a
                // sentence AND a diagram (see /section-10/ "See also"). Those
                // must keep the cap, or 250 characters of prose run the full
                // width of the page.
                if (!p.textContent.trim()) p.classList.add('is-figure');
            }

            var a = document.createElement('a');
            a.href = src;
            a.setAttribute('target', '_blank');
            a.setAttribute('rel', 'noopener noreferrer');
            // An image with no alt text would hand the link no accessible name
            // at all; where there is alt text it becomes the name by itself.
            if (!img.getAttribute('alt')) {
                a.setAttribute('aria-label', 'Open image at full size');
            }

            img.parentNode.insertBefore(a, img);
            a.appendChild(img);
        });
    })();
})();
