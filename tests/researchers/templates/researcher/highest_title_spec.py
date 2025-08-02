from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs


@pytest.fixture(scope="module")
def title_with_until(catalog):
    component = catalog.render(
        "researcher.HighestAcademicTitle",
        name="Doutorado",
        at=2015,
        until=2019,
    )
    return BeautifulSoup(component, "html.parser")


@pytest.fixture(scope="module")
def title_without_until(catalog):
    component = catalog.render(
        "researcher.HighestAcademicTitle",
        name="Mestrado",
        at=2020,
        until=None,
    )
    return BeautifulSoup(component, "html.parser")


@pytest.fixture(scope="module")
def title_without_name(catalog):
    component = catalog.render(
        "researcher.HighestAcademicTitle",
        name="",
        at=2020,
        until=None,
    )
    return BeautifulSoup(component, "html.parser")


class DescribeHighestAcademicTitle:

    def is_list_item(self, title_with_until):
        assert title_with_until.find("li")

    def has_title_with_years(self, title_with_until):
        spans = title_with_until.find_all("span")
        assert "Doutorado (2015 - 2019)" in spans[1].text

    def has_title_with_starting_year(self, title_without_until):
        spans = title_without_until.find_all("span")
        assert "Mestrado (2020)" in spans[1].text

    def has_default_value(self, title_without_name):
        spans = title_without_name.find_all("span")
        assert "Nenhum título especificado." in spans[1].text

    def has_label(self, title_with_until, title_without_until, title_without_name):
        assert "Título" in title_with_until.find_all("span")[0].text
        assert "Título" in title_without_until.find_all("span")[0].text
        assert "Título" in title_without_name.find_all("span")[0].text
