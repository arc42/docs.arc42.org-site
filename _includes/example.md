
### Examples

<div id="search-results">
  <ul>
    {% assign selected_examples = (site.examples | where: "category", include.category)  %}
    {% for example in selected_examples  %}            
       {% include example-header.html page=example link=true  %}
   {% endfor %}
  </ul>

</div>

