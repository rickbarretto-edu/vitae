from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET

import eliot
from loguru import logger

from src.lib.result import Result, catch
from src.processing.buffers import CurriculaBuffer

# TODO: those smaller functions should be moved to another module
# to avoid mixing abstractions.

# TODO: Also, a new Element(Tree) must be created to avoid
# mising abstractions and also make our codebase independent from the external XML parser.


__all__ = ["CurriculumParser"]


def normalized(tag: str) -> str:
    return tag.upper().replace(" ", "-")


def find(element: ET.Element | None, tag: str) -> ET.Element | None:
    if element is None:
        return None

    return element.find(normalized(tag))


def attribute(element: ET.Element | None, tag: str) -> str | None:
    if element is None:
        return None

    if element_attribute := element.attrib.get(normalized(tag)):
        return element_attribute.strip()


def as_int(text: str | None) -> int | None:
    if text is None:
        return None

    if text.isdigit():
        return int(text)


def log_parsing(topic: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Parsing {}'s data...", topic)

            result: Result[list | dict, ET.ParseError] = catch(
                lambda: func(*args, **kwargs)
            )

            if result:
                logger.debug("{}'s data successfully extracted.", topic)
                return result.value
            else:
                logger.error(
                    "Error when extracting {}'s data...: {}",
                    topic,
                    str(result.error),
                )
                return_type = func.__annotations__.get("return")
                return [] if isinstance(return_type, list) else {}

        return wrapper

    return decorator


class Node:
    def __init__(self, element: ET.Element | None):
        self.element = element

    def __getitem__(self, tag: str) -> str | None:
        return attribute(self.element, tag)

    def sub(self, tag: str) -> "Node":
        return Node(find(self.element, tag))


# TODO: This should not be called from open_curriculum, but instanciated.
# TODO: Each parsing method should be split into multiple Parser classes.
class CurriculumParser:
    """Parses curriculum from XML."""

    def __init__(self, file: Path, buffers: CurriculaBuffer) -> None:
        content = file.read_text(encoding="utf-8")

        self.id = file.name.removesuffix(".xml")
        self.document = ET.fromstring(content)
        self.data = find(self.document, "dados gerais")
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

        self.buffers.general.push(self.general_data())

        for experience in self.professional_experience():
            self.buffers.professions.push(experience)

        for background in self.academic_background():
            self.buffers.educations.push(background)

        for area in self.research_area():
            self.buffers.research_areas.push(area)

    @log_parsing("General Data")
    @eliot.log_call(action_type="parsing")
    def general_data(self):
        """Extract general data from the Lattes curriculum XML.

        This function navigates through the provided XML structure to extract
        general information about a researcher, such as their name, birthplace,
        ORCID ID, and professional institution details.

        Parameters
        ----------
        curriculum : xml.etree.ElementTree.Element
            The Lattes curriculum XML element representing a researcher's data.

        Returns
        -------
        dict
            A dictionary containing the following keys:
            - 'name' (str or None): Full name of the researcher.
            - 'city' (str or None): Birth city of the researcher.
            - 'state' (str or None): Birth state of the researcher.
            - 'country' (str or None): Birth country of the researcher.
            - 'quotes_names' (str or None): Names used in bibliographic citations.
            - 'orcid' (str or None): ORCID ID of the researcher.
            - 'abstract' (str or None): Abstract text from the researcher's CV.
            - 'professional_institution' (str or None): Name of the professional institution.
            - 'institution_state' (str or None): State of the professional institution.
            - 'institution_city' (str or None): City of the professional institution.

        Raises
        ------
        Exception
            If an error occurs during the extraction process, it is logged, and an
            empty dictionary is returned.
        """

        data = Node(self.data)
        resume = data.sub("resumo CV")
        professional_address = data.sub("endereco").sub("endereco profissional")

        if update_date := attribute(self.document, "data atualizacao"):
            update_date = datetime.strptime(update_date, "%d%m%Y")

        researcher_general_data = {
            "name": data["nome completo"],
            "city": data["cidade nascimento"],
            "state": data["UF nascimento"],
            "country": data["pais de nascimento"],
            "quotes_names": data["nome em citacoes bibliograficas"],
            "orcid": data["ORCID ID"],
            "abstract": resume["texto resumo CV RH"],
            "professional_institution": professional_address[
                "nome instituicao"
            ],
            "institution_state": professional_address["UF"],
            "institution_city": professional_address["cidade"],
        }

        return researcher_general_data

    @log_parsing("Professional Experience")
    @eliot.log_call(action_type="parsing")
    def professional_experience(self):
        """Extract professional experience from the Lattes curriculum.

        This function navigates through the XML structure of a Lattes curriculum
        to extract information about professional experiences.

        Parameters
        ----------
        curriculum : xml.etree.ElementTree.Element
            The Lattes curriculum of a researcher in XML format.

        Returns
        -------
        list of dict
            A list of dictionaries, where each dictionary contains information
            about a professional experience. Each dictionary has the following keys:
            - 'institution' (str or None): Name of the institution.
            - 'employment_relationship' (str or None): Type of employment relationship.
            - 'start_year' (int or None): Start year of the professional experience.
            - 'end_year' (int or None): End year of the professional experience.

        Notes
        -----
        If no professional experiences are found, an empty list is returned.
        In case of an error during extraction, the function logs the error and
        returns an empty list.
        """

        if (experiences := find(self.data, "atuacoes profissionais")) is None:
            return []

        professional_experience = []
        for experience in experiences.findall("ATUACAO-PROFISSIONAL"):
            institution = attribute(experience, "nome instituicao")
            links = experience.findall("VINCULOS")

            for link in links:
                if (link_type := attribute(link, "tipo de vinculo")) == "LIVRE":
                    link_type = attribute(link, "outro vinculo informado")
                start_year = attribute(link, "ano inicio")
                end_year = attribute(link, "ano fim")

                professional_experience.append(
                    {
                        "researcher_id": self.id,
                        "institution": institution,
                        "employment_relationship": link_type,
                        "start_year": as_int(start_year),
                        "end_year": as_int(end_year),
                    }
                )

        return professional_experience

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
                "institution": attribute(bg, "nome instituicao"),
                "course": attribute(bg, "nome curso"),
                "start_year": as_int(attribute(bg, "ano de inicio")),
                "end_year": as_int(attribute(bg, "ano de conclusao")),
            }
            for bg in find(self.data, "formacao academica titulacao") or []
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
                "major_knowledge_area": attribute(
                    area, "nome grande area do conhecimento"
                ),
                "knowledge_area": attribute(
                    area, "nome da area do conhecimento"
                ),
                "sub_knowledge_area": attribute(
                    area, "nome da sub-area do conhecimento"
                ),
                "specialty": attribute(area, "nome da especialidade"),
            }
            for area in find(self.data, "areas de atuacao") or []
        ]

    # TODO Ajustar Areas de Conhecimento
    @log_parsing("Academic Background")
    @eliot.log_call(action_type="parsing")
    def knowledgment_area(self, curriculo: ET.Element) -> list[Any]:
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
                "major_area": attribute(
                    knowledgement, "nome grande area do conhecimento"
                ),
                "area": attribute(
                    knowledgement, "nome da area do conhecimento"
                ),
                "sub_area": attribute(
                    knowledgement, "nome da sub-area do conhecimento"
                ),
                "specialty": attribute(knowledgement, "nome da especialidade"),
            }
            for knowledgement in find(curriculo, "areas de atuacao") or []
        ]
