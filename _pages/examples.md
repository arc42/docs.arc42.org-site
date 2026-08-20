---
layout: arc42-doc-section
title: All examples
permalink: /examples/
nav_title: Examples
group: meta
order: 19
---

# Examples

<!-- Plain lede, not an .arc42-example: that box is reserved for worked
     examples inside the documentation, never for site meta-copy. The second
     paragraph is the pointer to examples.arc42.org, and it sits ABOVE the list
     on purpose — the list runs long, and a reader who scrolls into it has
     already decided what "example" means on this site. -->
<p>These examples illustrate the various sections of arc42, taken from real-life systems.</p>

<p>Each one is an excerpt: a single section, shown on its own. For complete architecture
documentation of real systems &mdash; every arc42 section, from context to glossary &mdash;
see <a target="_blank" rel="noopener noreferrer nofollow" href="https://examples.arc42.org">examples.arc42.org</a>.</p>

<div class="example-list">
  <ul>
    {% assign examples = site.examples   %}
    {% for example in examples  %}            
       {% include example-header-nonutshell.html page=example link=true  %}
    {% endfor %}
  </ul>

</div>
