---
layout: default
title: Home
order: 0
permalink: /home/
hero: full
---
<div class="home">

  <h1>Practical tips and examples for the arc42 template</h1>

  <p class="lead">
    Everything on this site is organized by the twelve arc42 template sections.
    Open a section to see what belongs in it, how much detail it deserves, and
    how other teams have written it.
  </p>

  <h2 class="directory-heading" id="template-sections">The template sections</h2>

  <ol class="directory">
    {%- for section in site.data.sections -%}
    {%- assign tip_count = site.posts | where: "category", section.category | size -%}
    {%- assign section_number = section.number | prepend: '0' | slice: -2, 2 -%}
    <li>
      <a class="dir-link" href="{{ section.permalink | relative_url }}">
        <span class="dir-num"><span class="visually-hidden">Section </span>{{ section_number }}</span>
        <span class="dir-body">
          <span class="dir-name">{{ section.name }}</span>
          <span class="dir-desc">{{ section.blurb }}</span>
        </span>
        <span class="dir-count">{{ tip_count }} <span class="unit">{% if tip_count == 1 %}tip{% else %}tips{% endif %}</span></span>
      </a>
    </li>
    {%- endfor -%}
  </ol>


  <section class="keyword-panel" aria-labelledby="kw-heading">
    <h2 id="kw-heading">Navigate by keyword</h2>

    <p class="kw-intro">
      Our tips are tagged by {{ site.tags.size }} keywords that will help you navigate.
      Three of these stand out:
    </p>

    <div class="keyword-list">
      <div class="kw-row">
        <a class="kw-chip" href="{{ '/keywords/#lean' | relative_url }}">lean</a>
        <span class="kw-def">You are looking for opportunities to shorten or streamline your
          documentation pragmatically. You want to reduce efforts without losing content or
          value. You are working in an agile environment and want to have lightweight
          documentation &ndash; based on the motto: <em>travel light</em>.</span>
      </div>
      <div class="kw-row">
        <a class="kw-chip" href="{{ '/keywords/#thorough' | relative_url }}">thorough</a>
        <span class="kw-def">You are working in a more formal environment, e.g. developing very
          large or critical systems with hard quality requirements. Your stakeholders require
          thoroughness, accuracy and attention to detail. Maybe your systems and their
          documentation have to be audited.</span>
      </div>
      <div class="kw-row">
        <a class="kw-chip" href="{{ '/keywords/#essential' | relative_url }}">essential</a>
        <span class="kw-def">Despite lean and agile, there is some information about your system
          that you should always document; i.e. quality goals of your architecture.</span>
      </div>
    </div>

    <p class="kw-all"><a href="{{ '/keywords/' | relative_url }}">Browse all {{ site.tags.size }} keywords &rsaquo;</a></p>
  </section>

  {%- comment -%}
    The brief variant: the offer, not the schedule. Placed after the keyword
    panel and before the closing notes, so it has a presence of its own rather
    than being a bullet in a list — but is not the last thing on the page, which
    would end the front door on a pitch.
  {%- endcomment -%}
  {% include subtle-ads.html variant="brief" %}

  <section class="closing" aria-labelledby="closing-heading">
    <h2 id="closing-heading">More from arc42</h2>

    <ul class="closing-list">
      <li>
        <p><strong>Want to see it all put together?</strong> Read
          <a href="https://examples.arc42.org" target="_blank" rel="noopener noreferrer nofollow">complete architecture
          documentation</a> of real systems, written with arc42 from context to glossary.</p>
      </li>
      <li>
        <img class="closing-icon" src="/assets/images/brand/faq-icon.png" alt="" width="42" height="42" loading="lazy">
        <p><strong>Still have questions?</strong> Try our
          <a href="https://faq.arc42.org" target="_blank" rel="noopener noreferrer nofollow">extensive FAQ</a>,
          answering more than 120 frequently asked questions.</p>
      </li>
      <li>
        <img class="closing-icon" src="/assets/images/brand/contact-icon.png" alt="" width="42" height="42" loading="lazy">
        <p><strong>Need further assistance?</strong> Let us
          <a href="{{ '/contact/' | relative_url }}">know here</a>, we're listening.</p>
      </li>
      <li>
        <p><strong>This is open source.</strong> This site is completely open-source, maintained on a
          <a href="https://github.com/arc42/docs.arc42.org-site/" target="_blank" rel="noopener noreferrer nofollow">public GitHub repository</a>.</p>
      </li>
    </ul>
  </section>

</div>
