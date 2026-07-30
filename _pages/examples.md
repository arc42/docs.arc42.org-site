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
     examples inside the documentation, never for site meta-copy. -->
<p>These examples illustrate the various sections of arc42, taken from real-life systems.</p>

<div class="example-list">
  <ul>
    {% assign examples = site.examples   %}
    {% for example in examples  %}            
       {% include example-header-nonutshell.html page=example link=true  %}
    {% endfor %}
  </ul>

</div>
