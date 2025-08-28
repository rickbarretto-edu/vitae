
from vitae.infra.database import tables

from . import FullName, Nationality, Person

class DescribeFullName:
    def has_title_cased_name(self):
        fn = FullName("joão da silva")
        assert fn.value == "João Da Silva"

    def has_each_name_part(self):
        fn = FullName("maria clara")
        assert fn.each == ["Maria", "Clara"]

    def has_first_name(self):
        fn = FullName("ana beatriz rocha")
        assert fn.first == "Ana"

    def has_surname(self):
        fn = FullName("carlos eduardo fernandes")
        assert fn.surname == "Fernandes"

    def has_initials(self):
        fn = FullName("luiz carlos")
        assert fn.initials == "LC"

    def supports_str(self):
        fn = FullName("joão pedro")
        assert str(fn) == "João Pedro"


class DescribeNationality:
    def when_brazilian_from_brazil(self):
        nat = Nationality.from_table(tables.Nationality(
            researcher_id="",
            born_country="Brasil",
            nationality="B",
        ))
        assert str(nat) == "Brasileiro(a)"

    def when_brazilian_with_foreign_born_country(self):
        nat = Nationality.from_table(tables.Nationality(
            researcher_id="",
            born_country="Portugal",
            nationality="B",
        ))
        assert str(nat) == "Portugal (Brasileiro)"

    def when_foreigner(self):
        nat = Nationality.from_table(tables.Nationality(
            researcher_id="",
            born_country="França",
            nationality="E",
        ))
        assert str(nat) == "França (Estrangeiro)"

    def should_be_empty(self):
        nationality = Nationality.from_table(tables.Nationality(
            researcher_id="",
        ))

        assert str(nationality) == ""
