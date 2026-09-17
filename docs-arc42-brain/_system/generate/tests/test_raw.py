from pathlib import Path

import pytest
import yaml

from braingen.raw import make_raw

SECTIONS_YML = """
- number: 9
  name: Architecture Decisions
  category: decisions
  permalink: /section-9/
  examples_slug: 09-architecture-decisions
"""

PAGE = """---
layout: arc42-doc-section
title: 9 - Architecture decisions
permalink: /section-9/
number: 9
order: 13
---

# 9. Architecture Decisions

<div class="arc42-help" markdown="1">

## Content
Important decisions.

![flow]({{ site.imageurl }}/09/flow.png)

{% include example.md category="decisions" %}

</div>

{% include examples-link.html variant="inline" %}

{% include further-info.md
   category="decisions"
   topic="fundamental architecture and design decisions"
   faqlink="https://faq.arc42.org/category_c/#c-sec-9" %}
"""

TIP = """---
layout: post
title: "Tip 9-1: Document only architecturally relevant decisions!"
tags: decision quality stakeholder lean
category: decisions
permalink: /tips/9-1/
---

Body of the tip.
"""

EXAMPLE = """---
layout: post
title: "Example Decision: Use ADRs in Nygard format"
tags: decision example
category: decisions
permalink: /examples/decision-use-adrs/
---

![table]({{ site.exampleimages }}/adr-table.png)
"""

OTHER_EXAMPLE = EXAMPLE.replace("category: decisions", "category: concepts")


def build_site(root: Path) -> Path:
    site = root / "site"
    (site / "_data").mkdir(parents=True)
    (site / "_data/sections.yml").write_text(SECTIONS_YML)
    (site / "_pages").mkdir()
    (site / "_pages/section-9.md").write_text(PAGE)
    (site / "_posts/09-decisions").mkdir(parents=True)
    (site / "_posts/09-decisions/2016-03-01-t-9-1.md").write_text(TIP)
    (site / "_examples").mkdir()
    (site / "_examples/09-decision-example-adr.md").write_text(EXAMPLE)
    (site / "_examples/08-concept-example-x.md").write_text(OTHER_EXAMPLE)
    (site / "assets/images/sections/09").mkdir(parents=True)
    (site / "assets/images/sections/09/flow.png").write_bytes(b"png")
    (site / "assets/images/examples").mkdir(parents=True)
    (site / "assets/images/examples/adr-table.png").write_bytes(b"png")
    return site


def test_raw_all_copies_page_posts_matching_examples_and_images(tmp_path):
    site = build_site(tmp_path)
    vault = tmp_path / "vault"
    batch = make_raw(site, vault, 9, "all")
    assert batch == vault / "raw/section-9-all"
    assert (batch / "pages/section-9.md").read_text() == PAGE
    assert (batch / "posts/2016-03-01-t-9-1.md").read_text() == TIP
    assert (batch / "examples/09-decision-example-adr.md").exists()
    assert not (batch / "examples/08-concept-example-x.md").exists()
    assert (batch / "assets/sections/09/flow.png").read_bytes() == b"png"
    assert (batch / "assets/examples/adr-table.png").read_bytes() == b"png"
    m = yaml.safe_load((batch / "manifest.yaml").read_text())
    assert m["section"] == 9 and m["what"] == "all"
    assert m["name"] == "Architecture Decisions"
    assert m["category"] == "decisions"
    assert m["posts_dir"] == "09-decisions"
    assert m["permalink"] == "/section-9/"
    assert m["order"] == 13
    assert m["title"] == "9 - Architecture decisions"
    assert m["example_categories"] == ["decisions"]
    assert "pages/section-9.md" in m["files"] and "posts/2016-03-01-t-9-1.md" in m["files"]


def test_raw_page_only_and_content_only(tmp_path):
    site = build_site(tmp_path)
    vault = tmp_path / "vault"
    page_batch = make_raw(site, vault, 9, "page")
    assert (page_batch / "pages/section-9.md").exists()
    assert not (page_batch / "posts").exists()
    content_batch = make_raw(site, vault, 9, "content")
    assert not (content_batch / "pages").exists()
    assert (content_batch / "posts/2016-03-01-t-9-1.md").exists()
    assert (content_batch / "examples/09-decision-example-adr.md").exists()


def test_raw_refuses_to_overwrite(tmp_path):
    site = build_site(tmp_path)
    vault = tmp_path / "vault"
    make_raw(site, vault, 9, "page")
    with pytest.raises(FileExistsError):
        make_raw(site, vault, 9, "page")


def test_raw_unknown_section(tmp_path):
    site = build_site(tmp_path)
    with pytest.raises(ValueError, match="section 13"):
        make_raw(site, tmp_path / "vault", 13, "page")
