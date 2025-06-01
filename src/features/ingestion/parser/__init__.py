from pathlib import Path
from typing import Iterator

import eliot
from loguru import logger

from src.features.ingestion import schema

from . import _xml as xml
from .academic_background import academic_background
from .general_data import general_data
from .professional_experiences import professional_experiences
from .research_area import research_area

__all__ = ["CurriculumParser"]


class CurriculumParser:
    """Parser for XML Curriculum files.

    Notes:
    -----
    - The filename is the ID of the researcher.
    """

    def __init__(self, file: Path) -> None:
        logger.info("Parsing file: {}", file)

        content = file.read_text(encoding="utf-8")

        self.id = file.name.removesuffix(".xml")
        self.document = xml.parse(content)
        self.data = self.document.first("dados gerais")

    @eliot.log_call(action_type="parsing")
    def researcher(self) -> schema.GeneralData:
        return general_data(self.id, self.data)

    @eliot.log_call(action_type="parsing")
    def experiences(self) -> Iterator[schema.ProfessionalExperience]:
        yield from professional_experiences(self.id, self.data)

    @eliot.log_call(action_type="parsing")
    def background(self) -> Iterator[schema.AcademicBackground]:
        yield from academic_background(self.id, self.data)

    @eliot.log_call(action_type="parsing")
    def areas(self) -> Iterator[schema.ResearchArea]:
        yield from research_area(self.id, self.data)
