---
layout: arc42-doc-section
title: All examples
permalink: /examples/
nav_title: Examples
group: meta
order: 19
---

# Examples

<div class="arc42-example">
These examples illustrate the various sections of arc42, taken from real-life systems.
</div>

<div id="search-results">
  <ul>
    {% assign examples = site.examples   %}
    {% for example in examples  %}            
       {% include example-header-nonutshell.html page=example link=true  %}
    {% endfor %}
  </ul>

</div>
