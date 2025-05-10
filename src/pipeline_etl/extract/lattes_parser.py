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
        """
        FUNCTION TO OPEN THE XML CURRICULUM INSIDE THE ZIPPED FILE

        Description: Receives the zipped curriculum, extracts the XML from it, and reads it. Passes this XML to other extraction methods
        for some useful information from the curricula.

        Parameter: curriculumZIP - .zip file containing the Lattes curriculum.

        Return: None
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
                    researcherGeneralData = self.getGeneralData(curriculum)
                    researcherGeneralData["id"] = researcherID
                    generalDataBuffer.append(researcherGeneralData)

                    # ============= PROFESSIONAL EXPERIENCE ================#
                    professionalExperience = self.getProfessionalExperience(
                        curriculum
                    )
                    for experience in professionalExperience:
                        experience["researcher_id"] = researcherID
                        professionBuffer.append(experience)

                    # ============= ACADEMIC BACKGROUND ================#
                    academicBackground = self.getAcademicBackground(curriculum)
                    for background in academicBackground:
                        background["researcher_id"] = researcherID
                        educationBuffer.append(background)

                    # ============= RESEARCH AREA ================#
                    researchArea = self.getResearchArea(curriculum)
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
        """
        FUNCTION TO EXTRACT SOME GENERAL DATA FROM THE LATTES CURRICULUM

        Description: Receives the XML curriculum, navigates through it, saving researcher information in variables.

        Parameter: curriculum - Lattes curriculum of a researcher in XML.

        Return: researcherGeneralData - dictionary containing researcher information.
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

        Description: Receives the XML curriculum and navigates through its tags, extracting information about professional experiences.

        Parameter: curriculum - Lattes curriculum of a researcher in XML.

        Return: professionalExperience - list of dictionaries containing information about each professional experience.
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

        Description: Receives the XML curriculum and navigates through its tags, extracting information about academic background.

        Parameter: curriculum - Lattes curriculum of a researcher in XML.

        Return: academicBackground - list of dictionaries containing information about each academic background.
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
        """
        FUNCTION TO EXTRACT RESEARCH AREA FROM THE LATTES CURRICULUM

        Description: Receives the XML curriculum and navigates through its tags, extracting information about research areas.

        Parameter: curriculum - Lattes curriculum of a researcher in XML.

        Return: researchArea - list of dictionaries containing information about each research area.
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
        """
        FUNÇÃO PARA EXTRAIR A ÁREA DE ATUAÇÃO DO CURRÍCULO LATTES

        Descrição: Recebe o currículo XML e percorre suas tags, extraindo informações de área de atuação.

        Parâmetro: curriculo - currículo Lattes de um pesquisador em XML.

        Retorno: area - lista de dicionários contendo informações de cada área de atuação.
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
