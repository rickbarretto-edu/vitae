from datetime import datetime
from pathlib import Path
from typing import Any

import eliot
from loguru import logger

from src.processing.buffers import CurriculaBuffer
from src.processing.parsing import xml
from src.processing.parsing.general_data import general_data
from src.processing.parsing.professional_experiences import (
    professional_experiences,
)
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

        for background in self.academic_background():
            self.buffers.educations.push(background)

        for area in self.research_area():
            self.buffers.research_areas.push(area)

    @log_parsing("Academic Background")
    @eliot.log_call(action_type="parsing")
    def academic_background(self) -> list:
        """Extracts academic background information from a Lattes curriculum XML.

        This function navigates through the XML tags of a Lattes curriculum to extract
        information about the academic background of a researcher.

        Parameters
        ----------
        curriculum : xml.etree.ElementTree.Element
            The Lattes curriculum of a researcher in XML format.

        Returns
        -------
        list of dict
            A list of dictionaries, where each dictionary contains information about
            an academic background. Each dictionary includes the following keys:
            - 'type' (str): The type of academic background (e.g., undergraduate, master's, etc.).
            - 'institution' (str or None): The name of the institution.
            - 'course' (str or None): The name of the course.
            - 'start_year' (int or None): The year the course started.
            - 'end_year' (int or None): The year the course ended.

        Notes
        -----
        If no academic background information is found, an empty list is returned.
        Any errors during extraction are logged, and an empty list is returned in case of exceptions.
        """

        return [
            {
                "researcher_id": self.id,
                "type": bg.tag,
                "institution": xml.attribute(bg, "nome instituicao"),
                "course": xml.attribute(bg, "nome curso"),
                "start_year": xml.as_int(xml.attribute(bg, "ano de inicio")),
                "end_year": xml.as_int(xml.attribute(bg, "ano de conclusao")),
            }
            for bg in xml.find(
                self.data.element, "formacao academica titulacao"
            )
            or []
        ]

    @log_parsing("Research Area")
    @eliot.log_call(action_type="parsing")
    def research_area(self) -> list[Any]:
        """Extract research areas from the Lattes curriculum XML.

        This function navigates through the XML structure of a Lattes curriculum
        to extract information about research areas, including major knowledge
        areas, knowledge areas, sub-knowledge areas, and specialties.

        Parameters
        ----------
        curriculum : xml.etree.ElementTree.Element
            The Lattes curriculum XML element.

        Returns
        -------
        list of dict
            A list of dictionaries, where each dictionary contains information
            about a research area with the following keys:
            - 'major_knowledge_area' (str or None): The name of the major knowledge area.
            - 'knowledge_area' (str or None): The name of the knowledge area.
            - 'sub_knowledge_area' (str or None): The name of the sub-knowledge area.
            - 'specialty' (str or None): The name of the specialty.

        Notes
        -----
        If no research areas are found, an empty list is returned. In case of an
        error during extraction, the function logs the error and returns an empty list.

        Examples
        --------
        >>> curriculum = ET.parse("lattes.xml").getroot()
        >>> parser = LattesParser()
        >>> research_areas = parser.research_area(curriculum)
        >>> print(research_areas)
        [{'major_knowledge_area': 'Engineering', 'knowledge_area': 'Civil Engineering',
          'sub_knowledge_area': 'Structural Engineering', 'specialty': 'Concrete Structures'}, ...]
        """

        return [
            {
                "researcher_id": self.id,
                "major_knowledge_area": xml.attribute(
                    area, "nome grande area do conhecimento"
                ),
                "knowledge_area": xml.attribute(
                    area, "nome da area do conhecimento"
                ),
                "sub_knowledge_area": xml.attribute(
                    area, "nome da sub-area do conhecimento"
                ),
                "specialty": xml.attribute(area, "nome da especialidade"),
            }
            for area in xml.find(self.data.element, "areas de atuacao") or []
        ]

    # TODO Ajustar Areas de Conhecimento
    @log_parsing("Academic Background")
    @eliot.log_call(action_type="parsing")
    def knowledgment_area(self, curriculo: xml.Node) -> list[Any]:
        """Extracts the areas of expertise from a Lattes curriculum XML.

        This function parses the XML structure of a Lattes curriculum to extract
        information about the researcher's areas of expertise, including the
        major area, area, sub-area, and specialty.

        Parameters
        ----------
        curriculo : xml.etree.ElementTree.Element
            The XML element representing the Lattes curriculum.

        Returns
        -------
        list of dict
            A list of dictionaries, where each dictionary contains information
            about an area of expertise with the following keys:
            - "major_area" : str or None
                The name of the major area of knowledge.
            - "area" : str or None
                The name of the area of knowledge.
            - "sub_area" : str or None
                The name of the sub-area of knowledge.
            - "specialty" : str or None
                The name of the specialty.

        Notes
        -----
        If the "AREAS-DE-ATUACAO" tag is not found in the XML, an empty list is returned.
        In case of an exception during parsing, an error is logged, and an empty list is returned.

        Examples
        --------
        >>> from xml.etree.ElementTree import fromstring
        >>> xml_data = '''
        ... <CURRICULO>
        ...     <AREAS-DE-ATUACAO>
        ...         <AREA-DE-ATUACAO NOME-GRANDE-AREA-DO-CONHECIMENTO="Ciências Exatas"
        ...                         NOME-DA-AREA-DO-CONHECIMENTO="Matemática"
        ...                         NOME-DA-SUB-AREA-DO-CONHECIMENTO="Álgebra"
        ...                         NOME-DA-ESPECIALIDADE="Teoria dos Grupos"/>
        ...     </AREAS-DE-ATUACAO>
        ... </CURRICULO>
        ... '''
        >>> curriculo = fromstring(xml_data)
        >>> knowledgment_area(curriculo)
        [{'major_area': 'Ciências Exatas',
          'area': 'Matemática',
          'sub_area': 'Álgebra',
          'specialty': 'Teoria dos Grupos'}]
        """

        return [
            {
                "major_area": knowledgement["nome grande area do conhecimento"],
                "area": knowledgement["nome da area do conhecimento"],
                "sub_area": knowledgement["nome da sub-area do conhecimento"],
                "specialty": knowledgement["nome da especialidade"],
            }
            for knowledgement in curriculo.all("areas de atuacao")
        ]
