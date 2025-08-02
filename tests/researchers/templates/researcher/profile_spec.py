from bs4 import BeautifulSoup, Tag
from jinja2 import Environment
import pytest
import jinjax


@pytest.fixture(scope="module")
def catalog():
    env = Environment()
    env.filters["words"] = lambda x: x.split(" ")
    catalog = jinjax.Catalog(jinja_env=env)
    catalog.add_folder("vitae/features/researchers/templates")
    return catalog


@pytest.fixture(scope="module")
def profile(catalog):
    component = catalog.render(
        "researcher.Profile",
        name="John Doe",
        lattes_id="1234567890123456"
    )
    return BeautifulSoup(component, "html.parser")


class DescribeProfile:

    def has_wrapper_div(self, profile):
        div = profile.find("div")
        assert div

    def has_initials_avatar(self, profile):
        avatar_div = profile.find("div", class_="rounded-full")
        assert avatar_div
        text = avatar_div.text.strip()
        assert text == "JD"

    def has_name_heading(self, profile):
        h2 = profile.find("h2")
        assert h2
        assert h2.text.strip() == "John Doe"

    def has_lattes_id_paragraph(self, profile):
        p = profile.find("p")
        assert p
        assert p.text.strip() == "ID: 1234567890123456"

