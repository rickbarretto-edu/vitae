
from vitae.infra.database import tables

from .titles import AcademicDegree, AcademicTitles


class DescribeAcademicDegree:
    def should_be_created_from_scream_case(self):
        degree = AcademicDegree("MESTRADO", begin=2010, finish=2012)
        assert degree._name == "MESTRADO"
        assert degree.begin == 2010
        assert degree.finish == 2012

    def raises_if_name_is_not_scream_case(self):
        import pytest
        with pytest.raises(ValueError):
            AcademicDegree("Mestrado")

    def has_title_if_finished(self):
        degree = AcademicDegree("GRADUACAO", finish=2020)
        assert degree.has_title is True

    def has_no_title_if_not_finished(self):
        degree = AcademicDegree("GRADUACAO")
        assert degree.has_title is False

    def its_title_is_formatted(self):
        degree = AcademicDegree("POS_DOUTORADO")
        assert degree.title == "Pós-doutorado"

    def can_be_compared_by_rank(self):
        d1 = AcademicDegree("MESTRADO")
        d2 = AcademicDegree("DOUTORADO")
        assert d2 > d1
        assert not (d1 > d2)
        assert d1 != d2

    def has_negative_rank_if_title_unknown(self):
        degree = AcademicDegree("UNKNOWN_TITLE")
        assert degree.rank == -1


class DescribeAcademicTitles:
    def has_only_degrees_with_titles(self):
        titled = AcademicDegree("GRADUACAO", finish=2010)
        untitled = AcademicDegree("GRADUACAO")
        titles = AcademicTitles([titled, untitled])
        assert titles.titles == [titled]

    def has_highest_degree(self):
        grad = AcademicDegree("GRADUACAO", finish=2010)
        ms = AcademicDegree("MESTRADO", finish=2015)
        phd = AcademicDegree("DOUTORADO", finish=2020)
        at = AcademicTitles([grad, ms, phd])
        assert at.highest == phd

    def has_no_highest_if_no_title(self):
        deg = AcademicDegree("GRADUACAO")
        at = AcademicTitles([deg])
        assert at.highest is None

    def supports_from_table(self):
        some_id = "0000"

        education = tables.Education(
            id=some_id,
            researcher_id=some_id,
            institution_id=some_id,
            category="graduacao", 
            start=2008, 
            end=2012
        )
        at = AcademicTitles.from_tables([education])
        degree = at._degrees[0]

        assert isinstance(degree, AcademicDegree)
        assert degree._name == "GRADUACAO"
        assert degree.begin == 2008
        assert degree.finish == 2012
