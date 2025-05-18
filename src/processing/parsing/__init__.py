from datetime import datetime
from pathlib import Path
from typing import Any

import eliot
from loguru import logger

from src.processing.buffers import CurriculaBuffer
from src.processing.parsing import xml
from src.processing.parsing.academic_background import academic_background
from src.processing.parsing.general_data import general_data
from src.processing.parsing.professional_experiences import (
    professional_experiences,
)
from src.processing.parsing.research_area import research_area
from src.processing.parsing.logging import log_parsing


__all__ = ["CurriculumParser"]


# TODO: This should not be called from open_curriculum, but instanciated.
# TODO: Each parsing method should be split into multiple Parser classes.
class CurriculumParser:
    """Parses curriculum from XML."""

    def __init__(self, file: Path, buffers: CurriculaBuffer) -> None:
        content = file.read_text(encoding="utf-8")

        self.id = file.name.removesuffix(".xml")
        self.document = xml.parse(content)
        self.data = self.document.first("dados gerais")
        self.buffers = buffers

    @eliot.log_call(action_type="parsing")
    def parse(self):
        """Opens and processes an XML curriculum file contained within a ZIP archive.

        This method extracts the XML file from the provided ZIP archive, parses it,
        and processes its contents to extract general data, professional experience,
        academic background, and research area information. The extracted data is
        appended to the respective buffers and optionally flushed to a database.

        Parameters
        ----------
        curriculum : str
            Path to the XML file.
        buffers : CurriculaBuffer
            Store and flush data to database.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If an error occurs while processing the XML file or its contents.

        Notes
        -----
        - The method assumes that the ZIP file contains a single XML file.
        - The XML file name is used to extract the researcher ID.
        - The extracted data is processed using helper methods such as `general_data`,
          `professional_experience`, `academic_background`, and `research_area`.
        - If `flush` is True, the data is inserted into the database using the `load` module.
        """
        logger.info("Extracting researcher ({}) information", self.id)

        self.buffers.general.push(general_data(self.data))

        for experience in professional_experiences(self.id, self.data):
            self.buffers.professions.push(experience)

        for background in academic_background(self.id, self.data):
            self.buffers.educations.push(background)

        for area in research_area(self.id, self.data):
            self.buffers.research_areas.push(area)
