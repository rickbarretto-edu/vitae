from bs4 import BeautifulSoup, Tag
import pytest
from jinjax import HTMLAttrs


@pytest.fixture(scope="module")
def address_with_value(catalog):
    component = catalog.render(
        "researcher.Address",
        value="São Paulo, SP"
    )
    return BeautifulSoup(component, "html.parser")


@pytest.fixture(scope="module")
def address_without_value(catalog):
    component = catalog.render(
        "researcher.Address"
    )
    return BeautifulSoup(component, "html.parser")


class DescribeAddress:

    def has_content(self, address_with_value):
        assert "São Paulo, SP" in address_with_value.text

    def has_default_value(self, address_without_value):
        assert "Não fornecida." in address_without_value.text

    def has_label(self, address_with_value):
        assert "Localização" in address_with_value.text
