from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from vitae.features.ingestion import adapters

from . import _xml as xml
from .academic import education_from_xml
from .professional import address_from_xml, experience_from_xml
from .researcher import researcher_from_xml

if TYPE_CHECKING:
    from collections.abc import Iterator

__all__ = [
    "CurriculumDocument",
]


class CurriculumDocument:
    """Parser for XML Curriculum files.

    Notes
    -----
    - The filename is the ID of the researcher.

    """

    def __init__(self, file: Path) -> None:
        content = file.read_text(encoding="utf-8")

        self.id = file.name.removesuffix(".xml")
        self.document = xml.parse(content)

    @property
    def as_schema(self) -> adapters.Curriculum:
        return adapters.Curriculum(
            researcher=self.researcher,
            address=self.address,
            education=list(self.academic),
            experience=list(self.experience),
        )

    @property
    def researcher(self) -> adapters.Researcher:
        return researcher_from_xml(self.id, self.document)

    @property
    def address(self) -> adapters.Address | None:
        return address_from_xml(self.id, self.document)

    @property
    def academic(self) -> Iterator[adapters.Education]:
        return education_from_xml(self.id, self.document)

    @property
    def experience(self) -> Iterator[adapters.Experience]:
        return experience_from_xml(self.id, self.document)
