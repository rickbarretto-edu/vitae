from datetime import datetime
import xml.etree.ElementTree as ET
import zipfile

from src.pipeline_etl.load import load
from src.utils.loggers import ConfigLogger

logger = ConfigLogger(__name__).logger


class CurriculumParser:
    """Parses curriculum from XML."""

    def open_curriculum(
        self,
        curriculum_zip,
        general_data_buffer,
        profession_buffer,
        research_area_buffer,
        education_buffer,
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
        logger.info(f"Processing file {curriculum_zip}")

        try:
            with zipfile.ZipFile(curriculum_zip, "r") as zip_file:
                name = zip_file.namelist()[0]
                researcherID = name.split(".")[0]
                logger.info(
                    f"Extracting curriculum for researcher ID: {researcherID}"
                )

                with zip_file.open(name) as curriculum_xml:
                    tree = ET.parse(curriculum_xml)
                    curriculum = tree.getroot()

                    # ============= GENERAL DATA ================#
                    general_data = self.general_data(curriculum)
                    general_data["id"] = researcherID
                    general_data_buffer.append(general_data)

                    # ============= PROFESSIONAL EXPERIENCE ================#
                    professional_experience = self.professional_experience(
                        curriculum
                    )
                    for experience in professional_experience:
                        experience["researcher_id"] = researcherID
                        profession_buffer.append(experience)

                    # ============= ACADEMIC BACKGROUND ================#
                    academic_background = self.academic_background(curriculum)
                    for background in academic_background:
                        background["researcher_id"] = researcherID
                        education_buffer.append(background)

                    # ============= RESEARCH AREA ================#
                    research_area = self.research_area(curriculum)
                    for area in research_area:
                        area["researcher_id"] = researcherID
                        research_area_buffer.append(area)

                    if flush:
                        logger.info("INSERTING INTO DATABASE")
                        load.upsert_researcher(general_data_buffer)
                        load.upsert_professional_experience(profession_buffer)
                        load.upsert_academic_background(education_buffer)
                        load.upsert_research_area(research_area_buffer)

        except Exception as e:
            logger.error(f"Error processing file {curriculum_zip}: {str(e)}")

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
            if update_date := curriculum.attrib.get("DATA-ATUALIZACAO"):
                update_date = datetime.strptime(update_date, "%d%m%Y")

            if general_data := curriculum.find("DADOS-GERAIS"):
                full_name = (
                    general_data.attrib.get("NOME-COMPLETO", "").strip() or None
                )
                birth_city = (
                    general_data.attrib.get("CIDADE-NASCIMENTO", "").strip()
                    or None
                )
                birth_state = (
                    general_data.attrib.get("UF-NASCIMENTO", "").strip() or None
                )
                birth_country = (
                    general_data.attrib.get("PAIS-DE-NASCIMENTO", "").strip()
                    or None
                )
                citation_names = (
                    general_data.attrib.get(
                        "NOME-EM-CITACOES-BIBLIOGRAFICAS", ""
                    ).strip()
                    or None
                )
                orcid = general_data.attrib.get("ORCID-ID", "").strip() or None
            else:
                full_name = birth_city = birth_state = birth_country = (
                    citation_names
                ) = orcid = None

            resume = general_data.find("RESUMO-CV")
            resume_text = (
                resume.attrib.get("TEXTO-RESUMO-CV-RH", "").strip() or None
                if resume is not None
                else None
            )

            if address := general_data.find("ENDERECO"):
                if professional_address := address.find("ENDERECO-PROFISSIONAL"):
                    institution_name = (
                        professional_address.attrib.get(
                            "NOME-INSTITUICAO-EMPRESA", ""
                        ).strip()
                        or None
                    )
                    institution_state = (
                        professional_address.attrib.get("UF", "").strip() or None
                    )
                    institution_city = (
                        professional_address.attrib.get("CIDADE", "").strip()
                        or None
                    )
                else:
                    institution_name = institution_state = institution_city = None
            else:
                institution_name = institution_state = institution_city = None

            researcher_general_data = {
                "name": full_name,
                "city": birth_city,
                "state": birth_state,
                "country": birth_country,
                "quotes_names": citation_names,
                "orcid": orcid,
                "abstract": resume_text,
                "professional_institution": institution_name,
                "institution_state": institution_state,
                "institution_city": institution_city,
            }

            logger.debug("Researcher general data successfully extracted")
            return researcher_general_data

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
            general_data = curriculum.find("DADOS-GERAIS")

            experiences = (
                general_data.find("ATUACOES-PROFISSIONAIS")
                if general_data is not None
                else None
            )
            if experiences is None:
                return []

            professional_experience = []
            for experience in experiences.findall("ATUACAO-PROFISSIONAL"):
                institution = (
                    experience.attrib.get("NOME-INSTITUICAO", "").strip()
                    or None
                )
                links = experience.findall("VINCULOS")

                for link in links:
                    link_type = (
                        link.attrib.get("TIPO-DE-VINCULO", "").strip() or None
                    )
                    if link_type == "LIVRE":
                        link_type = (
                            link.attrib.get(
                                "OUTRO-VINCULO-INFORMADO", ""
                            ).strip()
                            or None
                        )
                    start_year = (
                        link.attrib.get("ANO-INICIO", "").strip() or None
                    )
                    end_year = link.attrib.get("ANO-FIM", "").strip() or None

                    professional_experience.append(
                        {
                            "institution": institution,
                            "employment_relationship": link_type,
                            "start_year": int(start_year)
                            if start_year and start_year.isdigit()
                            else None,
                            "end_year": int(end_year)
                            if end_year and end_year.isdigit()
                            else None,
                        }
                    )

            logger.debug("Professional experience successfully extracted")
            return professional_experience

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
            general_data = curriculum.find("DADOS-GERAIS")

            backgrounds = general_data.find("FORMACAO-ACADEMICA-TITULACAO")
            if backgrounds is None:
                return []

            academic_background = []
            for background in backgrounds:
                background_type = background.tag
                if not background_type:
                    print(f"Background type: {background_type}")
                institution = (
                    background.attrib.get("NOME-INSTITUICAO", "").strip()
                    or None
                )
                course = background.attrib.get("NOME-CURSO", "").strip() or None
                start_year = (
                    background.attrib.get("ANO-DE-INICIO", "").strip() or None
                )
                end_year = (
                    background.attrib.get("ANO-DE-CONCLUSAO", "").strip()
                    or None
                )

                academic_background.append(
                    {
                        "type": background_type,
                        "institution": institution,
                        "course": course,
                        "start_year": int(start_year)
                        if start_year and start_year.isdigit()
                        else None,
                        "end_year": int(end_year)
                        if end_year and end_year.isdigit()
                        else None,
                    }
                )

            logger.debug("Academic background successfully extracted")
            return academic_background

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
