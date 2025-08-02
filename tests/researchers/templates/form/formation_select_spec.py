from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs


@pytest.fixture(scope="module")
def select(catalog):
    component = catalog.render(
        "form.FormationSelect",
        on_url="education",
        available=["undergrad", "master", "phd"],
        _content="All Educations",
    )
    return BeautifulSoup(component, "html.parser")

class DescribeFormationSelect:

    def has_4_options(self, select):
        options = select.find_all("option")
        assert 4 == len(options)
    
    def its_options_has_given_values(self, select):
        options = select.find_all("option")

        expected = ["", "undergrad", "master", "phd"]
        actual = [option["value"].strip() for option in options]

        assert expected == actual

    def its_options_display_is_titled(self, select):
        options = select.find_all("option")

        expected = ["All Educations", "Undergrad", "Master", "Phd"]
        actual = [option.text.strip() for option in options]

        assert expected == actual

    def is_select(self, select):
        assert "select" == select.find("select").name

    def its_bind_to_url(self, select):
        assert "education" == select.find("select")["name"]
