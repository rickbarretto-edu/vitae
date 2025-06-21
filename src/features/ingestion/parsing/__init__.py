from collections.abc import Iterator
from pathlib import Path

from src.features.ingestion import domain
from src.features.ingestion.adapters import schema

from . import _xml as xml
from .academic_background import academic_background
from .general_data import general_data
from .professional_experiences import professional_experiences
from .research_area import research_area

__all__ = ["CurriculumParser"]


class CurriculumParser:
    """Parser for XML Curriculum files.

    Notes
    -----
    - The filename is the ID of the researcher.

    """

    def __init__(self, file: Path) -> None:
        content = file.read_text(encoding="utf-8")

        self.id = file.name.removesuffix(".xml")
        self.document = xml.parse(content)
        self.data = self.document.first("dados gerais")

    @property
    def all(self) -> domain.Curriculum:
        return domain.Curriculum(
            _personal_data=self.researcher,
            _academic_background=self.background,
            _professional_experiences=self.experiences,
            _research_areas=self.areas,
        )

    @property
    def researcher(self) -> schema.GeneralData:
        return general_data(self.id, self.data)

    @property
    def experiences(self) -> Iterator[schema.ProfessionalExperience]:
        yield from professional_experiences(self.id, self.data)

    @property
    def background(self) -> Iterator[schema.AcademicBackground]:
        yield from academic_background(self.id, self.data)

    @property
    def areas(self) -> Iterator[schema.ResearchArea]:
        yield from research_area(self.id, self.data)
