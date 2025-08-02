from vitae.infra.database import tables

from .expertises import Expertises, StudyField

class DescribeStudyField:
    def has_taxonomy_ordered_and_title_cased(self):
        sf = StudyField("science", "computer science", "ai", "deep learning")
        taxonomy = list(sf.taxonomy)
        assert taxonomy == ["Science", "Computer Science", "Ai", "Deep Learning"]

    def has_specialization_as_most_specific_level(self):
        sf = StudyField("science", "computer science", None, "deep learning")
        assert sf.specialization == "Deep Learning"

    def has_specialization_when_only_broad_field(self):
        sf = StudyField("science", None, None, None)
        assert sf.specialization == "Science"


class DescribeExpertises:
    def can_be_created_from_tables(self):

        expertises = [
            tables.Expertise("major1", "area1", "sub1"),
            tables.Expertise("major2", "area2", None),
        ]

        expertises_obj = Expertises.from_tables(expertises)
        specialities = list(expertises_obj.specialities)

        assert len(specialities) == 2
        assert specialities[0] == "Sub1"
        assert specialities[1] == "Area2"
