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

        def new_expertise(major, area, sub):
            return tables.Expertise(
                id=1, researcher_id="0",
                major=major, 
                area=area, 
                sub=sub,
            )

        expertises = [
            new_expertise("major1", "area2", "sub1"),
            new_expertise("major2", "area2", None),
        ]

        expertises_obj = Expertises.from_tables(expertises)
        specialities = list(expertises_obj.specialities)

        assert len(specialities) == 2
        assert specialities[0] == "Sub1"
        assert specialities[1] == "Area2"
