from pathlib import Path

import eliot
from loguru import logger

from . import _xml as xml
from .academic_background import academic_background
from .general_data import general_data
from .knowledge_areas import knowledge_areas
from .professional_experiences import professional_experiences
from .research_area import research_area

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
        """Parameters
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

        return general_data(self.id, self.data)

    @eliot.log_call(action_type="parsing")
    def experiences(self):
        for experience in professional_experiences(self.id, self.data):
            yield experience

    @eliot.log_call(action_type="parsing")
    def background(self):
        for background in academic_background(self.id, self.data):
            yield background

    @eliot.log_call(action_type="parsing")
    def areas(self):
        for area in research_area(self.id, self.data):
            yield area
