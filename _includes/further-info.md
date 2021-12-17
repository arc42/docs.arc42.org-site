
<hr class="with-no-margin"/>
## Further Info

### Tips

<div id="search-results">
    {% assign selected_posts = (site.posts | where: "category", include.category) | reverse %}
    {% for post in selected_posts  %}
    <div class="article-wrapper">
        <article>
            {% include article-header.html page=post link=true share=false %}
        </article>
    </div>
    <hr class="with-no-margin"/>
    {% endfor %}
</div>

### Related Questions

See [here for questions related to {{ include.topic }}]({{ include.faqlink }}).
