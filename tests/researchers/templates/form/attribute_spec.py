import pytest
from jinjax import HTMLAttrs

@pytest.fixture(scope="module")
def attribute(catalog):
    return catalog.render(
        "form.Attribute",
        _attrs=HTMLAttrs({"class": "flex flex-col gap-2"}),
        _content="<label>Label</label><input placeholder='Search'/>",
    )

class DescribeFormAttribute:

    def has_content(self, attribute):
        assert "<label>Label</label>" in attribute
        assert "<input placeholder='Search'" in attribute

    def has_custom_class(self, attribute):
        assert 'class="flex flex-col gap-2"' in attribute

    def is_a_div(self, attribute):
        assert attribute.strip().startswith("<div")
        assert attribute.strip().endswith("</div>")
