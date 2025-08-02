
from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs

@pytest.fixture(scope="module")
def state_select(catalog):
    component = catalog.render(
        "form.StateSelect",
        on_url="state",
        available=["sp", "rj", "mg"],
        _content="Select State"
    )
    return BeautifulSoup(component, "html.parser")


class DescribeStateSelect:

    def is_select(self, state_select):
        assert state_select.find("select").name == "select"

    def its_name_is_bound(self, state_select):
        tag = state_select.find("select")
        assert tag["name"] == "state"

    def has_4_options(self, state_select):
        options = state_select.find_all("option")
        assert len(options) == 4

    def has_raw_values(self, state_select):
        expected = ["", "sp", "rj", "mg"]
        actual = [opt["value"] for opt in state_select.find_all("option")]
        assert expected == actual

    def has_upper_labels(self, state_select):
        expected = ["Select State", "SP", "RJ", "MG"]
        actual = [opt.text.strip() for opt in state_select.find_all("option")]
        assert expected == actual

    def it_reuses_form_select(self, state_select):
        tag = state_select.find("select")
        classes = tag["class"]
        assert "Select" in classes
