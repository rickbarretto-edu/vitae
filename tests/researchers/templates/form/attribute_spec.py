from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs


@pytest.fixture(scope="module")
def attribute(catalog):
    component = catalog.render(
        "form.Attribute",
        _attrs=HTMLAttrs({"class": "flex flex-col gap-2"}),
        _content="<label>Label</label><input placeholder='Search'/>",
    )
    return BeautifulSoup(component, "html.parser")

class DescribeFormAttribute:

    def has_content(self, attribute):
        assert attribute.find("label").text == "Label" # type: ignore
        assert attribute.find("input")["placeholder"] == "Search" # type: ignore

    def has_custom_class(self, attribute):
        classes = attribute.find("div")["class"] # type: ignore
        
        assert "flex" in classes
        assert "flex-col" in classes
        assert "gap-2" in classes

    def is_a_div(self, attribute):
        assert attribute.find("div").name == "div" # type: ignore
