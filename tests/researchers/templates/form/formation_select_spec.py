from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs


@pytest.fixture(scope="module")
def label(catalog):
    component = catalog.render(
        "form.Label",
        of="username",
        _content="Username"
    )
    return BeautifulSoup(component, "html.parser")


class DescribeLabel:

    def is_label(self, label):
        assert label.find("label").name == "label"

    def is_bound(self, label):
        tag = label.find("label")
        assert tag["for"] == "username"

    def has_content(self, label):
        tag = label.find("label")
        assert tag.text.strip() == "Username"
