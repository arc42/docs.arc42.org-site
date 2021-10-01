
### Examples

<div id="search-results">
  <ul>
    {% assign selected_samples = (site.samples | where: "category", include.category) | reverse %}
    {% for sample in selected_samples  %}            
       {% include sample-header.html page=sample link=true  %}
   {% endfor %}
  </ul>

</div>

