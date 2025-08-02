from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs


@pytest.fixture(scope="module")
def institution_with_name(catalog):
    component = catalog.render(
        "researcher.Institution",
        name="Universidade de São Paulo"
    )
    return BeautifulSoup(component, "html.parser")


@pytest.fixture(scope="module")
def institution_without_name(catalog):
    component = catalog.render(
        "researcher.Institution",
        name=""
    )
    return BeautifulSoup(component, "html.parser")


class DescribeInstitution:

    def is_list_item(self, institution_with_name):
        assert institution_with_name.find("li")

    def has_content(self, institution_with_name):
        assert "Universidade de São Paulo" in institution_with_name.find_all("span")[1].text

    def has_default_value(self, institution_without_name):
        assert "Sem associação com alguma instituição." in institution_without_name.find_all("span")[1].text

    def has_label(self, institution_with_name, institution_without_name):
        assert "Instituição" in institution_with_name.find_all("span")[0].text
        assert "Instituição" in institution_without_name.find_all("span")[0].text
