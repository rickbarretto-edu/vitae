
from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs

@pytest.fixture(scope="module")
def select(catalog):
    component = catalog.render(
        "form.Select",
        on_url="category",
        _content="""<option value="">Select Category</option>
                    <option value="science">Science</option>
                    <option value="art">Art</option>"""
    )
    return BeautifulSoup(component, "html.parser")


class DescribeSelect:

    def is_select(self, select):
        assert select.find("select").name == "select"

    def is_bound_to_url(self, select):
        tag = select.find("select")
        assert tag["name"] == "category"

    def has_expected_options(self, select):
        options = select.find_all("option")
        expected_values = ["", "science", "art"]
        expected_labels = ["Select Category", "Science", "Art"]

        actual_values = [opt["value"] for opt in options]
        actual_labels = [opt.text.strip() for opt in options]

        assert expected_values == actual_values
        assert expected_labels == actual_labels

    def has_bind_script(self, select):
        script = select.find("script")
        assert script is not None
        assert "URLSearchParams" in script.text
        assert "selectedOption.selected = true" in script.text
