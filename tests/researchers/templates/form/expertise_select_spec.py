from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs


@pytest.fixture(scope="module")
def select(catalog):
    component = catalog.render(
        "form.ExpertiseSelect",
        on_url="expertise",
        available=["math", "chemistry", "history"],
        _content="Expertise",
    )
    return BeautifulSoup(component, "html.parser")

class DescribeButton:

    def has_4_options(self, select):
        options = select.find_all("option")
        assert 4 == len(options)
    
    def its_options_has_given_values(self, select):
        options = select.find_all("option")

        expected = ["", "math", "chemistry", "history"]
        actual = [option["value"].strip() for option in options]

        assert expected == actual

    def its_options_display_is_titled(self, select):
        options = select.find_all("option")

        expected = ["Expertise", "Math", "Chemistry", "History"]
        actual = [option.text.strip() for option in options]

        assert expected == actual

    def is_select(self, select):
        assert "select" == select.find("select").name

    def its_bind_to_url(self, select):
        assert "expertise" == select.find("select")["name"]
