from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs


@pytest.fixture(scope="module")
def nationality_with_value(catalog):
    component = catalog.render(
        "researcher.Nationality",
        value="Brasileira"
    )
    return BeautifulSoup(component, "html.parser")


@pytest.fixture(scope="module")
def nationality_without_value(catalog):
    component = catalog.render(
        "researcher.Nationality",
        value=""
    )
    return BeautifulSoup(component, "html.parser")


class DescribeNationality:

    def is_list_item(self, nationality_with_value):
        assert nationality_with_value.find("li")

    def has_content(self, nationality_with_value):
        assert "Brasileira" in nationality_with_value.find_all("span")[1].text

    def has_default_value(self, nationality_without_value):
        assert "Nacionalidade não informada." in nationality_without_value.find_all("span")[1].text

    def has_label(self, nationality_with_value, nationality_without_value):
        assert "Nacionalidade" in nationality_with_value.find_all("span")[0].text
        assert "Nacionalidade" in nationality_without_value.find_all("span")[0].text
