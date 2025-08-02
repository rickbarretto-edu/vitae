
from vitae.infra.database import tables

from .address import City, Country, State, Address

class DescribeCity:
    def has_title_cased_name(self):
        city = City("são paulo")
        assert city.name == "São Paulo"

    def has_empty_string_if_none(self):
        city = City(None)
        assert city.name == ""

    def is_casted_to_string(self):
        city = City("rio")
        assert str(city) == "Rio"


class DescribeState:
    def has_uppercase_abbr(self):
        state = State("sp")
        assert state.abbr == "SP"

    def has_empty_string_if_none(self):
        state = State(None)
        assert state.abbr == ""

    def is_casted_to_string(self):
        state = State("mg")
        assert str(state) == "MG"


class DescribeCountry:
    def has_title_cased_name(self):
        country = Country("estados unidos")
        assert country.name == "Estados Unidos"

    def has_empty_string_if_none(self):
        country = Country(None)
        assert country.name == ""

    def is_casted_to_string(self):
        country = Country("canadá")
        assert str(country) == "Canadá"


class DescribeAddress:
    def test_brazilian_format(self):
        address = Address(
            city=City("campinas"),
            state=State("sp"),
            country=Country("brasil"),
        )
        assert str(address) == "Campinas (SP)"

    def test_foreign_format(self):
        address = Address(
            city=City("paris"),
            state=State("idf"),
            country=Country("frança"),
        )
        assert str(address) == "Paris (IDF), França"

    def is_created_from_table(self):
        addr = Address.from_table(tables.Address(
            researcher_id="0",
            institution_id="0",
            city = "london",
            state = "ldn",
            country = "reino unido",
        ))

        assert addr.city.name == "London"
        assert addr.state.abbr == "LDN"
        assert addr.country.name == "Reino Unido"
