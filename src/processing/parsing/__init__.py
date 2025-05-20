from pathlib import Path

import eliot
from loguru import logger

from src.processing.parsing import parsers
from src.processing.buffers import CurriculaBuffer
from src.processing.parsing import xml


__all__ = ["CurriculumParser"]


class CurriculumParser:
    """Parser for XML Curriculum files.

    Attributes
    ----------
    id : str
        Researcher's ID.
    document: xml.Node
        Node element containing the whole XML document.
    data: xml.Node
        Node element containing the general data.
    buffers: CurriculaBuffer
        Buffer to store the parsed data.

    Methods
    -------
    parse() -> None
        Parses the XML document.

    Notes
    -----
    - The filename is the ID of the researcher.
    - The extracted data is processed using helper functions presents into `.parsers`, module.
    - Flusing to database must be done outside this class. Use ``Buffer.on_flush`` for this.
    """

    def __init__(self, file: Path) -> None:
        """
        Parameters
        ----------
        file : Path
            Path to the XML file.
        buffers : CurriculaBuffer
            Buffer to store the parsed data.
        """
        content = file.read_text(encoding="utf-8")

        self.id = file.name.removesuffix(".xml")
        self.document = xml.parse(content)
        self.data = self.document.first("dados gerais")

    @eliot.log_call(action_type="parsing")
    def researcher(self):
        """Parse the Curriculum XML file and extract useful information."""

        logger.info("Parsing researcher ({}) curriculum", self.id)

        return parsers.general_data(self.data)

        # for experience in parsers.professional_experiences(self.id, self.data):
        #     self.buffers.professions.push(experience)

        # for background in parsers.academic_background(self.id, self.data):
        #     self.buffers.educations.push(background)

        # for area in parsers.research_area(self.id, self.data):
        #     self.buffers.research_areas.push(area)
