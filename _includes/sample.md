
### Examples

<div id="search-results">
    {% assign selected_samples = (site.samples | where: "category", include.category) | reverse %}
    {% for sample in selected_samples  %}            
      {% include sample-header.html page=sample link=true  %}
        
   {% endfor %}
</div>

