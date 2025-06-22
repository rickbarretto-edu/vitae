from collections.abc import Iterator
from pathlib import Path

from vitae.features.ingestion import domain
from vitae.features.ingestion.adapters import schema

from . import _xml as xml
from .academic import academic_background
from .researcher import expertise, general_data, nationality
from .professional import professional_experiences

__all__ = ["CurriculumParser", "schema"]


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
        researcher = researcher(self.id, self.data)
        nationality_ = nationality(self.id, self.data)
        expertise_ = expertise(self.id, self.data)
        experiences = professional(self.id, self.data)
        background = academic(self.id, self.data)

        return domain.Curriculum(
            _personal_data=researcher,
            _nationality=nationality_,
            _expertise=expertise_,
            _academic_background=background,
            _professional_experiences=experiences,
        )
