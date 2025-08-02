from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs


@pytest.fixture(scope="module")
def checkbox(catalog):
    component = catalog.render(
        "form.Checkbox",
        on_url="enabled",
        _content="Enabled",
    )
    return BeautifulSoup(component, "html.parser")

class DescribeButton:

    def has_label(self, checkbox):
        assert checkbox.find("label")
    
    def has_input(self, checkbox):
        assert checkbox.find("input")

    def has_content_into_label(self, checkbox):
        assert "Enabled" == checkbox.find("label").text.strip()

    def its_name_is_on_url(self, checkbox):
        assert "enabled" == checkbox.find("input")["name"]

    def its_label_refers_to_input(self, checkbox):
        assert checkbox.find("input")["name"] == checkbox.find("label")["for"]
