import pytest
import yaml

from braingen.emit import emit_section, render_frontmatter, yaml_scalar
from braingen.parse import load_vault
from tests import vaultkit as vk


def test_yaml_scalar_plain_when_safe_quoted_otherwise():
    assert yaml_scalar(13) == "13"
    assert yaml_scalar("/tips/9-1/") == "/tips/9-1/"
    assert yaml_scalar("/section-9/#background-on-adrs") == "/section-9/#background-on-adrs"
    assert yaml_scalar("9 - Architecture decisions") == "9 - Architecture decisions"
    assert yaml_scalar("Tip 9-2: Criteria!", quote=True) == '"Tip 9-2: Criteria!"'
    assert yaml_scalar("a: b") == '"a: b"'
    assert yaml_scalar("yes") == '"yes"'
    assert yaml_scalar("") == '""'
    assert yaml_scalar('say "hi"', quote=True) == '"say \\"hi\\""'
    with pytest.raises(TypeError):
        yaml_scalar(True)


def test_render_frontmatter_reads_back_and_omits_empty_related():
    related = [
        {"kind": "tip", "title": 'Tip 9-2: "quoted"', "url": "/tips/9-2/"},
        {"kind": "term", "title": "ADR", "url": ""},
    ]
    text = render_frontmatter([("layout", "post"), ("title", "T: x"), ("related", related)], quoted=frozenset({"title"}))
    assert text.startswith('---\nlayout: post\ntitle: "T: x"\nrelated:\n- kind: tip\n')
    assert text.endswith("---\n")
    assert yaml.safe_load(text.split("---\n")[1]) == {
        "layout": "post",
        "title": "T: x",
        "related": [
            {"kind": "tip", "title": 'Tip 9-2: "quoted"', "url": "/tips/9-2/"},
            {"kind": "term", "title": "ADR"},
        ],
    }
    assert "related" not in render_frontmatter([("layout", "post"), ("related", [])])


def test_emit_section(tmp_path):
    vk.section(tmp_path)
    vault = load_vault(tmp_path)

    out = emit_section(vault, vault.pages["section-9"])

    assert out.rel == "_pages/section-9.md"
    assert out.source == "wiki/sections/section-9.md"
    assert out.text == (
        "---\nlayout: arc42-doc-section\ntitle: 9 - Architecture decisions\npermalink: /section-9/\n"
        "number: 9\norder: 13\n"
        "# generated from docs-arc42-brain/wiki/sections/section-9.md — do not edit\n---\n\n"
        "# 9. Architecture Decisions\n\n"
        '<div class="arc42-help" markdown="1">\n'
        "## Background (on ADRs)\nText.\n\n"
        '{% include example.md category="decisions" %}\n\n'
        "</div>\n\n"
        '{% include examples-link.html variant="inline" %}\n\n'
        "_&lt;describe here >_\n\n\n"
        "{% include further-info.md\n"
        '   category="decisions"\n'
        '   topic="fundamental architecture and design decisions"\n'
        '   faqlink="https://faq.arc42.org/category_c/#c-sec-9" %}\n'
    )
