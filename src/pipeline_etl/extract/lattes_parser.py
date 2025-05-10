from datetime import datetime
import xml.etree.ElementTree as ET
import zipfile

from src.pipeline_etl.load import load
from src.utils.loggers import ConfigLogger

configLogger = ConfigLogger(__name__)
logger = configLogger.logger


class CurriculumParser:
    """
    CLASS TO PARSE THE LATTES CURRICULUM XML FILES

    Description: This class is responsible for extracting information from the Lattes curriculum XML files. It includes methods to extract
    general data, professional experience, academic background, and research areas from the XML structure.

    Attributes:
        curriculum (str): Path to the Lattes curriculum XML file.
    """

    def __init__(self):
        pass

    def open_curriculum(
        self,
        curriculumZIP,
        generalDataBuffer,
        professionBuffer,
        researchAreaBuffer,
        educationBuffer,
        flush,
    ):
        """Opens and processes an XML curriculum file contained within a ZIP archive.

        This method extracts the XML file from the provided ZIP archive, parses it,
        and processes its contents to extract general data, professional experience,
        academic background, and research area information. The extracted data is
        appended to the respective buffers and optionally flushed to a database.

        Parameters
        ----------
        curriculumZIP : str
            Path to the ZIP file containing the Lattes curriculum XML.
        generalDataBuffer : list
            Buffer to store general data extracted from the curriculum.
        professionBuffer : list
            Buffer to store professional experience data extracted from the curriculum.
        researchAreaBuffer : list
            Buffer to store research area data extracted from the curriculum.
        educationBuffer : list
            Buffer to store academic background data extracted from the curriculum.
        flush : bool
            If True, the extracted data is inserted into the database.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If an error occurs while processing the ZIP file or its contents.

        Notes
        -----
        - The method assumes that the ZIP file contains a single XML file.
        - The XML file name is used to extract the researcher ID.
        - The extracted data is processed using helper methods such as `general_data`,
          `professional_experience`, `academic_background`, and `research_area`.
        - If `flush` is True, the data is inserted into the database using the `load` module.
        """
        logger.info(f"Processing file {curriculumZIP}")

        try:
            with zipfile.ZipFile(curriculumZIP, "r") as zipFile:
                name = zipFile.namelist()[0]
                researcherID = name.split(".")[0]
                logger.info(
                    f"Extracting curriculum for researcher ID: {researcherID}"
                )

                with zipFile.open(name) as curriculumXML:
                    tree = ET.parse(curriculumXML)
                    curriculum = tree.getroot()

                    # ============= GENERAL DATA ================#
                    researcherGeneralData = self.general_data(curriculum)
                    researcherGeneralData["id"] = researcherID
                    generalDataBuffer.append(researcherGeneralData)

                    # ============= PROFESSIONAL EXPERIENCE ================#
                    professionalExperience = self.professional_experience(
                        curriculum
                    )
                    for experience in professionalExperience:
                        experience["researcher_id"] = researcherID
                        professionBuffer.append(experience)

                    # ============= ACADEMIC BACKGROUND ================#
                    academicBackground = self.academic_background(curriculum)
                    for background in academicBackground:
                        background["researcher_id"] = researcherID
                        educationBuffer.append(background)

                    # ============= RESEARCH AREA ================#
                    researchArea = self.research_area(curriculum)
                    for area in researchArea:
                        area["researcher_id"] = researcherID
                        researchAreaBuffer.append(area)

                    if flush:
                        logger.info("INSERTING INTO DATABASE")
                        load.upsert_researcher(generalDataBuffer)
                        load.upsert_professional_experience(professionBuffer)
                        load.upsert_academic_background(educationBuffer)
                        load.upsert_research_area(researchAreaBuffer)

        except Exception as e:
            logger.error(f"Error processing file {curriculumZIP}: {str(e)}")

    def general_data(self, curriculum):
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

        try:
            CV = curriculum

            updateDate = CV.attrib.get("DATA-ATUALIZACAO", None)
            if updateDate:
                updateDate = datetime.strptime(updateDate, "%d%m%Y")

            generalData = CV.find("DADOS-GERAIS")
            if generalData is not None:
                fullName = (
                    generalData.attrib.get("NOME-COMPLETO", "").strip() or None
                )
                birthCity = (
                    generalData.attrib.get("CIDADE-NASCIMENTO", "").strip()
                    or None
                )
                birthState = (
                    generalData.attrib.get("UF-NASCIMENTO", "").strip() or None
                )
                birthCountry = (
                    generalData.attrib.get("PAIS-DE-NASCIMENTO", "").strip()
                    or None
                )
                citationNames = (
                    generalData.attrib.get(
                        "NOME-EM-CITACOES-BIBLIOGRAFICAS", ""
                    ).strip()
                    or None
                )
                orcid = generalData.attrib.get("ORCID-ID", "").strip() or None
            else:
                fullName = birthCity = birthState = birthCountry = (
                    citationNames
                ) = orcid = None

            resume = generalData.find("RESUMO-CV")
            resumeText = (
                resume.attrib.get("TEXTO-RESUMO-CV-RH", "").strip() or None
                if resume is not None
                else None
            )

            address = generalData.find("ENDERECO")
            if address is not None:
                professionalAddress = address.find("ENDERECO-PROFISSIONAL")
                if professionalAddress is not None:
                    institutionName = (
                        professionalAddress.attrib.get(
                            "NOME-INSTITUICAO-EMPRESA", ""
                        ).strip()
                        or None
                    )
                    institutionState = (
                        professionalAddress.attrib.get("UF", "").strip() or None
                    )
                    institutionCity = (
                        professionalAddress.attrib.get("CIDADE", "").strip()
                        or None
                    )
                else:
                    institutionName = institutionState = institutionCity = None
            else:
                institutionName = institutionState = institutionCity = None

            researcherGeneralData = {
                "name": fullName,
                "city": birthCity,
                "state": birthState,
                "country": birthCountry,
                "quotes_names": citationNames,
                "orcid": orcid,
                "abstract": resumeText,
                "professional_institution": institutionName,
                "institution_state": institutionState,
                "institution_city": institutionCity,
            }

            logger.debug("Researcher general data successfully extracted")
            return researcherGeneralData

        except Exception as e:
            logger.error(f"Error extracting general data: {str(e)}")
            return {}

    def professional_experience(self, curriculum):
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

        try:
            CV = curriculum
            generalData = CV.find("DADOS-GERAIS")

            experiences = (
                generalData.find("ATUACOES-PROFISSIONAIS")
                if generalData is not None
                else None
            )
            if experiences is None:
                return []

            professionalExperience = []
            for experience in experiences.findall("ATUACAO-PROFISSIONAL"):
                institution = (
                    experience.attrib.get("NOME-INSTITUICAO", "").strip()
                    or None
                )
                links = experience.findall("VINCULOS")

                for link in links:
                    linkType = (
                        link.attrib.get("TIPO-DE-VINCULO", "").strip() or None
                    )
                    if linkType == "LIVRE":
                        linkType = (
                            link.attrib.get(
                                "OUTRO-VINCULO-INFORMADO", ""
                            ).strip()
                            or None
                        )
                    startYear = (
                        link.attrib.get("ANO-INICIO", "").strip() or None
                    )
                    endYear = link.attrib.get("ANO-FIM", "").strip() or None

                    professionalExperience.append(
                        {
                            "institution": institution,
                            "employment_relationship": linkType,
                            "start_year": int(startYear)
                            if startYear and startYear.isdigit()
                            else None,
                            "end_year": int(endYear)
                            if endYear and endYear.isdigit()
                            else None,
                        }
                    )

            logger.debug("Professional experience successfully extracted")
            return professionalExperience

        except Exception as e:
            logger.error(f"Error extracting professional experience: {str(e)}")
            return []

    def academic_background(self, curriculum) -> list:
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

        try:
            CV = curriculum

            generalData = CV.find("DADOS-GERAIS")

            backgrounds = generalData.find("FORMACAO-ACADEMICA-TITULACAO")
            if backgrounds is None:
                return []

            academicBackground = []
            for background in backgrounds:
                backgroundType = background.tag
                if backgroundType == None:
                    print(f"Background type: {backgroundType}")
                institution = (
                    background.attrib.get("NOME-INSTITUICAO", "").strip()
                    or None
                )
                course = background.attrib.get("NOME-CURSO", "").strip() or None
                startYear = (
                    background.attrib.get("ANO-DE-INICIO", "").strip() or None
                )
                endYear = (
                    background.attrib.get("ANO-DE-CONCLUSAO", "").strip()
                    or None
                )

                academicBackground.append(
                    {
                        "type": backgroundType,
                        "institution": institution,
                        "course": course,
                        "start_year": int(startYear)
                        if startYear and startYear.isdigit()
                        else None,
                        "end_year": int(endYear)
                        if endYear and endYear.isdigit()
                        else None,
                    }
                )

            logger.debug("Academic background successfully extracted")
            return academicBackground

        except Exception as e:
            logger.error(f"Error extracting academic background: {str(e)}")
            return []

    def research_area(self, curriculum):
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
        >>> curriculum = ET.parse('lattes.xml').getroot()
        >>> parser = LattesParser()
        >>> research_areas = parser.research_area(curriculum)
        >>> print(research_areas)
        [{'major_knowledge_area': 'Engineering', 'knowledge_area': 'Civil Engineering',
          'sub_knowledge_area': 'Structural Engineering', 'specialty': 'Concrete Structures'}, ...]
        """
       
        try:
            CV = curriculum

            generalData = CV.find("DADOS-GERAIS")

            areas = generalData.find("AREAS-DE-ATUACAO")
            if areas is None:
                return []

            researchArea = []
            for area in areas:
                majorArea = (
                    area.attrib.get(
                        "NOME-GRANDE-AREA-DO-CONHECIMENTO", ""
                    ).strip()
                    or None
                )
                knowledgeArea = (
                    area.attrib.get("NOME-DA-AREA-DO-CONHECIMENTO", "").strip()
                    or None
                )
                subKnowledgeArea = (
                    area.attrib.get(
                        "NOME-DA-SUB-AREA-DO-CONHECIMENTO", ""
                    ).strip()
                    or None
                )
                specialty = (
                    area.attrib.get("NOME-DA-ESPECIALIDADE", "").strip() or None
                )

                researchArea.append(
                    {
                        "major_knowledge_area": majorArea,
                        "knowledge_area": knowledgeArea,
                        "sub_knowledge_area": subKnowledgeArea,
                        "specialty": specialty,
                    }
                )

            logger.debug("Research area successfully extracted")
            return researchArea

        except Exception as e:
            logger.error(f"Error extracting research area: {str(e)}")
            return []

    # TODO Ajustar Areas de Conhecimento
    def knowledgment_area(self, curriculo):
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
            - "GRANDE_AREA" : str or None
                The name of the major area of knowledge.
            - "AREA" : str or None
                The name of the area of knowledge.
            - "SUB_AREA" : str or None
                The name of the sub-area of knowledge.
            - "ESPECIALIDADE" : str or None
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
        [{'GRANDE_AREA': 'Ciências Exatas',
          'AREA': 'Matemática',
          'SUB_AREA': 'Álgebra',
          'ESPECIALIDADE': 'Teoria dos Grupos'}]
        """

        try:
            CV = curriculo

            atuacoes = CV.find("AREAS-DE-ATUACAO")
            if atuacoes is None:
                return []

            areaAtuacao = []
            for atuacao in atuacoes:
                grandeArea = atuacao.attrib.get(
                    "NOME-GRANDE-AREA-DO-CONHECIMENTO", None
                )
                area = atuacao.attrib.get("NOME-DA-AREA-DO-CONHECIMENTO", None)
                subArea = atuacao.attrib.get(
                    "NOME-DA-SUB-AREA-DO-CONHECIMENTO", None
                )
                especialidade = atuacao.attrib.get(
                    "NOME-DA-ESPECIALIDADE", None
                )

                areaAtuacao.append(
                    {
                        "GRANDE_AREA": grandeArea,
                        "AREA": area,
                        "SUB_AREA": subArea,
                        "ESPECIALIDADE": especialidade,
                    }
                )

            logger.debug("Formação acadêmica extraída com sucesso")
            return areaAtuacao

        except Exception as e:
            logger.error(f"Erro ao extrair área de atuação: {str(e)}")
            return []


parser = CurriculumParser()
