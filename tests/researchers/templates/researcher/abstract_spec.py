from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs

@pytest.fixture(scope="module")
def abstract(catalog):
    component = catalog.render(
        "researcher.Abstract",
        label="Resumo",
        _content="John Doe is a software engineer with 10+ years of experience..."
    )
    return BeautifulSoup(component, "html.parser")

class DescribeAbstract:

    def is_div(self, abstract):
        assert abstract.find("div")

    def has_heading(self, abstract):
        h4 = abstract.find("h4")
        assert h4

    def its_content_is_into_p(self, abstract):
        p = abstract.find("p")
        assert p
        assert p.text.strip() == "John Doe is a software engineer with 10+ years of experience..."

