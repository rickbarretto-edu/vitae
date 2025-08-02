from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs

@pytest.fixture(scope="module")
def search(catalog):
    component = catalog.render(
        "form.Search",
        on_url="query",
        placeholder="Search here..."
    )
    return BeautifulSoup(component, "html.parser")


class DescribeSearch:

    def is_input(self, search):
        assert search.find("input").name == "input"

    def is_text_input(self, search):
        tag = search.find("input")
        assert tag["type"] == "text"

    def is_bound_to_url(self, search):
        tag = search.find("input")
        assert tag["name"] == "query"

    def has_placeholder(self, search):
        tag = search.find("input")
        assert tag["placeholder"] == "Search here..."

    def has_binder_script(self, search):
        script = search.find("script")
        assert script is not None
        assert "URLSearchParams" in script.text
        assert "self.value = value" in script.text
