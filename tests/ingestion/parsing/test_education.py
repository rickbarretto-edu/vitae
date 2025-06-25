import pytest

from vitae.features.ingestion.adapters.academic import Education
from vitae.features.ingestion.parsing._xml import Node
from vitae.features.ingestion.parsing.academic import education_from_xml

from .utils import Document


@pytest.fixture
def researcher() -> str:
    return "123456789"


@pytest.fixture
def document() -> Node:
    return Document.of("""
        <DADOS-GERAIS>
        <FORMACAO-ACADEMICA-TITULACAO>
            <GRADUACAO
                CODIGO-CURSO="101" NOME-CURSO="Computer Science" CODIGO-AREA-CURSO="4001" 
                STATUS-DO-CURSO="CONCLUIDO" ANO-DE-INICIO="2010" ANO-DE-CONCLUSAO="2014" 
                NOME-DO-ORIENTADOR="Dr. Alan Turing" NUMERO-ID-ORIENTADOR="12345"
                CODIGO-INSTITUICAO="UNI001" NOME-INSTITUICAO="Tech University"
            />
            <MESTRADO 
                CODIGO-CURSO="201" NOME-CURSO="Artificial Intelligence" CODIGO-AREA-CURSO="4002" 
                STATUS-DO-CURSO="CONCLUIDO" ANO-DE-INICIO="2015" ANO-DE-CONCLUSAO="2017" 
                CODIGO-INSTITUICAO="UNI002" NOME-INSTITUICAO="Institute of Technology" 
                NOME-COMPLETO-DO-ORIENTADOR="Dr. Ada Lovelace" NUMERO-ID-ORIENTADOR="67890" 
            >
                <PALAVRAS-CHAVE PALAVRA-CHAVE-1="Machine Learning"/> 
                <AREAS-DO-CONHECIMENTO>
                    <AREA-DO-CONHECIMENTO-1 
                        NOME-GRANDE-AREA-DO-CONHECIMENTO="Engenharia" 
                        NOME-DA-AREA-DO-CONHECIMENTO="Engenharia Elétrica" 
                        NOME-DA-SUB-AREA-DO-CONHECIMENTO="Sistemas Computacionais" 
                        NOME-DA-ESPECIALIDADE="Redes Neurais"
                    />
                    <AREA-DO-CONHECIMENTO-2 
                        NOME-GRANDE-AREA-DO-CONHECIMENTO="Ciências Exatas" 
                        NOME-DA-AREA-DO-CONHECIMENTO="Ciência da Computação" 
                        NOME-DA-SUB-AREA-DO-CONHECIMENTO="Inteligência Artificial" 
                        NOME-DA-ESPECIALIDADE="Aprendizado de Máquina"
                    />
                </AREAS-DO-CONHECIMENTO>
                <SETORES-DE-ATIVIDADE/>
            </MESTRADO>
            <DOUTORADO 
                CODIGO-INSTITUICAO="UNI003" NOME-INSTITUICAO="Advanced Computing Institute" 
                CODIGO-CURSO="301" NOME-CURSO="Data Science" 
                STATUS-DO-CURSO="CONCLUIDO" ANO-DE-INICIO="2018" ANO-DE-CONCLUSAO="2022"  
                NOME-COMPLETO-DO-ORIENTADOR="Dr. Grace Hopper" NUMERO-ID-ORIENTADOR="54321"
            />
            <POS-DOUTORADO 
                CODIGO-INSTITUICAO="UNI004" NOME-INSTITUICAO="Global Tech Lab" 
                ANO-DE-INICIO="2022" ANO-DE-CONCLUSAO="2024" STATUS-DO-CURSO="CONCLUIDO" 
                NUMERO-ID-ORIENTADOR="98765"
            >
                <AREAS-DO-CONHECIMENTO>
                    <AREA-DO-CONHECIMENTO-1 
                        NOME-GRANDE-AREA-DO-CONHECIMENTO="Ciências Exatas" 
                        NOME-DA-AREA-DO-CONHECIMENTO="Ciência da Computação" 
                        NOME-DA-SUB-AREA-DO-CONHECIMENTO="Computação em Nuvem" 
                        NOME-DA-ESPECIALIDADE="Infraestrutura Distribuída"
                    />
                    <AREA-DO-CONHECIMENTO-2
                        NOME-GRANDE-AREA-DO-CONHECIMENTO="Engenharia" 
                        NOME-DA-AREA-DO-CONHECIMENTO="Engenharia de Software" 
                        NOME-DA-SUB-AREA-DO-CONHECIMENTO="DevOps" 
                        NOME-DA-ESPECIALIDADE="Automação de Deploy"
                    />
                    <AREA-DO-CONHECIMENTO-3
                        NOME-GRANDE-AREA-DO-CONHECIMENTO="Ciências Exatas" 
                        NOME-DA-AREA-DO-CONHECIMENTO="Matemática Aplicada" 
                        NOME-DA-SUB-AREA-DO-CONHECIMENTO="Estatística Computacional" 
                        NOME-DA-ESPECIALIDADE="Big Data"
                    />
                </AREAS-DO-CONHECIMENTO>
            </POS-DOUTORADO>
        </FORMACAO-ACADEMICA-TITULACAO>
        </DADOS-GERAIS>
        """).as_node


class DescribeEducationFromXml:
    """Tests for education_from_xml function."""

    def has_4_entries(self, researcher, document):
        educations: list[Education] = list(
            education_from_xml(researcher, document)
        )
        assert len(educations) == 4


class DescribeGraduationOfEducation:
    def is_graduation(self, researcher, document):
        grad = list(education_from_xml(researcher, document))[0]
        assert grad.category == "GRADUACAO"

    def is_cs_course(self, researcher, document):
        grad = list(education_from_xml(researcher, document))[0]
        assert grad.course == "Computer Science"

    def its_starts_at_2014(self, researcher, document):
        grad = list(education_from_xml(researcher, document))[0]
        assert grad.start == 2010

    def and_ends_at_2014(self, researcher, document):
        grad = list(education_from_xml(researcher, document))[0]
        assert grad.end == 2014

    def its_serviced_by_tech_uni(self, researcher, document):
        grad = list(education_from_xml(researcher, document))[0]
        assert grad.institution.lattes_id == "UNI001"
        assert grad.institution.name == "Tech University"


class DescribeMasterOfEducation:
    def is_master(self, researcher, document):
        master = list(education_from_xml(researcher, document))[1]
        assert master.category == "MESTRADO"

    def is_ai_course(self, researcher, document):
        master = list(education_from_xml(researcher, document))[1]
        assert master.course == "Artificial Intelligence"

    def its_starts_at_2015(self, researcher, document):
        master = list(education_from_xml(researcher, document))[1]
        assert master.start == 2015

    def and_ends_at_2017(self, researcher, document):
        master = list(education_from_xml(researcher, document))[1]
        assert master.end == 2017

    def its_serviced_by_tech_inst(self, researcher, document):
        master = list(education_from_xml(researcher, document))[1]
        assert master.institution.lattes_id == "UNI002"
        assert master.institution.name == "Institute of Technology"

    def has_fields(self, researcher, document):
        master = list(education_from_xml(researcher, document))[1]
        assert len(master.fields) == 2
        assert any(sf.area == "Ciência da Computação" for sf in master.fields)
        assert any(
            field.specialty == "Redes Neurais"
            or field.specialty == "Aprendizado de Máquina"
            for field in master.fields
        )


class DescribePhdOfEducation:
    def is_phd(self, researcher, document):
        phd = list(education_from_xml(researcher, document))[2]
        assert phd.category == "DOUTORADO"

    def is_data_science_course(self, researcher, document):
        phd = list(education_from_xml(researcher, document))[2]
        assert phd.course == "Data Science"

    def its_starts_at_2018(self, researcher, document):
        phd = list(education_from_xml(researcher, document))[2]
        assert phd.start == 2018

    def and_ends_at_2022(self, researcher, document):
        phd = list(education_from_xml(researcher, document))[2]
        assert phd.end == 2022

    def its_serviced_by_advanced_computing(self, researcher, document):
        phd = list(education_from_xml(researcher, document))[2]
        assert phd.institution.lattes_id == "UNI003"
        assert phd.institution.name == "Advanced Computing Institute"


class DescribePostdocOfEducation:
    def is_postdoc(self, researcher, document):
        postdoc = list(education_from_xml(researcher, document))[
            3
        ]
        assert postdoc.category == "POS-DOUTORADO"

    def its_starts_at_2022(self, researcher, document):
        postdoc = list(education_from_xml(researcher, document))[
            3
        ]
        assert postdoc.start == 2022

    def and_ends_at_2024(self, researcher, document):
        postdoc = list(education_from_xml(researcher, document))[
            3
        ]
        assert postdoc.end == 2024

    def its_serviced_by_global_lab(self, researcher, document):
        postdoc = list(education_from_xml(researcher, document))[
            3
        ]
        assert postdoc.institution.lattes_id == "UNI004"
        assert postdoc.institution.name == "Global Tech Lab"

    def has_fields(self, researcher, document):
        postdoc = list(education_from_xml(researcher, document))[
            3
        ]
        assert len(postdoc.fields) == 3
        assert any(
            field.area == "Engenharia de Software" for field in postdoc.fields
        )
        assert any(field.specialty == "Big Data" for field in postdoc.fields)
