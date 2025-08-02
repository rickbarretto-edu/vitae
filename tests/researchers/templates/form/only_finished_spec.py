
from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs

@pytest.fixture(scope="module")
def checkbox(catalog):
    component = catalog.render(
        "form.OnlyFinishedFormation",
        on_url="finished",
        _content="Apenas finalizadas."
    )
    return BeautifulSoup(component, "html.parser")


class DescribeOnlyFinishedFormation:

    def is_checkbox_input(self, checkbox):
        input_tag = checkbox.find("input")
        assert input_tag is not None
        assert input_tag["type"] == "checkbox"

    def its_name_is_bound_to_url_key(self, checkbox):
        input_tag = checkbox.find("input")
        assert input_tag["name"] == "finished"

    def has_associated_label(self, checkbox):
        label_tag = checkbox.find("label")
        assert label_tag is not None
        assert "Apenas finalizadas." in label_tag.text

    def it_reuses_form_checkbox(self, checkbox):
        assert checkbox.find("form") is None  # It’s just a rendered component, not a real <form>
        assert checkbox.find("input")["type"] == "checkbox"
