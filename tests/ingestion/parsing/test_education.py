from collections.abc import Iterable, Iterator
from typing import Final
from vitae.features.ingestion.adapters.academic import Education, StudyField
from vitae.features.ingestion.adapters.institution import Institution
from vitae.features.ingestion.parsing._xml import Node
from vitae.features.ingestion.parsing.academic import education_from_xml
from .utils import Document, XmlString
import pytest

@pytest.fixture
def sample_researcher() -> str:
    return "123456789"


@pytest.fixture
def document_sample() -> Node:
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
    """Describe education_from_xml function's behavior."""

    def it_parses_all_entries(self, sample_researcher, document_sample):
        educations: list[Education] = list(education_from_xml(sample_researcher, document_sample))
        assert len(educations) == 4

    def it_parses_graduation(self, sample_researcher, document_sample):
        educations: list[Education] = list(education_from_xml(sample_researcher, document_sample))
        grad = educations[0]
        assert grad.category == "GRADUACAO"
        assert grad.course == "Computer Science"
        assert grad.start == 2010
        assert grad.end == 2014
        assert grad.institution.lattes_id == "UNI001"
        assert grad.institution.name == "Tech University"

    def it_parses_master(self, sample_researcher, document_sample):
        educations: list[Education] = list(education_from_xml(sample_researcher, document_sample))
        master = educations[1]
        assert master.category == "MESTRADO"
        assert master.course == "Artificial Intelligence"
        assert master.start == 2015
        assert master.end == 2017
        assert master.institution.lattes_id == "UNI002"
        assert master.institution.name == "Institute of Technology"
        assert len(master.fields) == 2
        assert any(sf.area == "Ciência da Computação" for sf in master.fields)
        assert any(
            fields.specialty == "Redes Neurais"
            or fields.specialty == "Aprendizado de Máquina"
            for fields in master.fields
        )

    def it_parses_phd(self, sample_researcher, document_sample):
        educations: list[Education] = list(education_from_xml(sample_researcher, document_sample))
        phd = educations[2]
        assert phd.category == "DOUTORADO"
        assert phd.course == "Data Science"
        assert phd.start == 2018
        assert phd.end == 2022
        assert phd.institution.lattes_id == "UNI003"
        assert phd.institution.name == "Advanced Computing Institute"

    def it_parses_posdoc(self, sample_researcher, document_sample):
        educations: list[Education] = list(education_from_xml(sample_researcher, document_sample))
        postdoc = educations[3]
        assert postdoc.category == "POS-DOUTORADO"
        assert postdoc.start == 2022
        assert postdoc.end == 2024
        assert postdoc.institution.lattes_id == "UNI004"
        assert postdoc.institution.name == "Global Tech Lab"
        assert len(postdoc.fields) == 3
        assert any(field.area == "Engenharia de Software" for field in postdoc.fields)
        assert any(field.specialty == "Big Data" for field in postdoc.fields)




