from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs


@pytest.fixture(scope="module")
def specialities(catalog):
    component = catalog.render(
        "researcher.Specialities",
        specialities=["machine learning", "data science"]
    )
    return BeautifulSoup(component, "html.parser")


class DescribeSpecialities:

    def is_unordered_list(self, specialities):
        ul = specialities.find("ul")
        assert ul

    def has_no_bullet_point(self, specialities):
        classes = specialities.find("ul").get("class", [])
        assert "list-none" in classes

    def has_pill_list_items(self, specialities):
        pills = specialities.find_all("li")
        assert len(pills) == 2

    def has_title_cased_text_in_pills(self, specialities):
        pills = specialities.find_all("li")
        expected = ["Machine Learning", "Data Science"]
        actual = [pill.text.strip() for pill in pills]
        assert expected == actual
