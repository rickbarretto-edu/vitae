from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs


@pytest.fixture(scope="module")
def button(catalog):
    component = catalog.render(
        "form.Button",
        _attrs=HTMLAttrs({"href": "#", "onclick": "doAction()"}),
        _content="Click here!",
    )
    return BeautifulSoup(component, "html.parser")

class DescribeButton:

    def has_content(self, button):
        assert "Click here!" == button.text.strip()

    def has_href(self, button: BeautifulSoup):
        assert "#" == button.find("button")["href"] # type: ignore

    def has_onclick(self, button):
        assert "doAction()" == button.find("button")["onclick"]

    def is_button(self, button):
        assert "button" == button.find("button").name
