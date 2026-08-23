{%- comment -%}
  "Practical Tips" block at the foot of every arc42 section page: the tips
  written for that section, plus a link into the FAQ. (The file keeps its old
  name so the twelve `{% include further-info.md %}` call sites stay put.)

  The tips list carries no heading of its own. It used to sit under "### Tips"
  below an h2 named "Further Info"; once the h2 became "Practical Tips" that
  subheading only restated its parent, so it is gone and the list runs straight
  on from the h2.

  Parameters
    category  required — the _posts category to pull tips from.
    topic     required — human-readable topic name for the FAQ sentence.
    faqlink   required — URL of the matching FAQ category.

  The block at the foot pointing at examples.arc42.org takes NO parameter from
  here — _includes/examples-link.html resolves the section from `page.number`
  against _data/sections.yml. That is on purpose: this include has twelve call
  sites and none of them had to change.

  Rewritten from the version that reused _includes/article-header.html inside a
  `<div id="search-results">`. Two problems with that:

  · the id was a straight collision with the panel assets/js/search.js writes
    its results into — two elements with the same id on one page, one of which
    the search code looks up by that id;

  · it rendered every tip as a full <article><header><h4> with its own byline
    furniture, which is a lot of document outline for what is a list of links.

  The tip titles link to the tip's own page and the tags link to the keyword
  index (/keywords/#<tag>, whose ids _pages/keywords.html cgi_escapes). Before
  this, the masthead advertised 144 tips and a section page could not reach a
  single one of them.
{%- endcomment -%}

<hr class="with-no-margin"/>

## Practical Tips

{% assign section_tips = site.posts | where: "category", include.category | reverse -%}
{%- if section_tips.size > 0 %}
<ul class="tips-list">
{%- for tip in section_tips %}
  <li>
    <a class="tip-title" href="{{ tip.url | relative_url }}">{{ tip.title }}</a>
    {%- if tip.tags.size > 0 %}
    <span class="tags">
      {%- for tag in tip.tags %}
      {%- assign tag_id = tag | cgi_escape %}
      <a class="tag" href="{{ '/keywords/#' | append: tag_id | relative_url }}">#{{ tag }}</a>
      {%- endfor %}
    </span>
    {%- endif %}
  </li>
{%- endfor %}
</ul>
{%- else %}
<p class="tips-empty">No tips have been written for this section yet.</p>
{%- endif %}

### Related Questions

See <a target="_blank" rel="noopener noreferrer nofollow" href="{{ include.faqlink }}">here for questions related to {{ include.topic }}</a>.

{% include examples-link.html variant="block" %}
