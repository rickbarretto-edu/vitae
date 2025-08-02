import pytest

from vitae.features.ingestion.adapters import Researcher
from vitae.features.ingestion.parsing._xml import Node
from vitae.features.ingestion.parsing.researcher import researcher_from_xml

from ._test_utils import Document


@pytest.fixture
def researcher() -> str:
    return "123456789"


@pytest.fixture
def document() -> Node:
    return Document.of("""
    <DADOS-GERAIS 
        NOME-COMPLETO="Alan Mathison Turing" 
        NOME-EM-CITACOES-BIBLIOGRAFICAS="TURING, A. M." 
        NACIONALIDADE="B" 
        PAIS-DE-NASCIMENTO="Brasil" 
        ORCID-ID="https://orcid.org/0000-0002-1825-0097"
    >
        <RESUMO-CV TEXTO-RESUMO-CV-RH="Pioneering computer scientist and ..."/>
        <AREAS-DE-ATUACAO>
            <AREA-DE-ATUACAO 
                NOME-GRANDE-AREA-DO-CONHECIMENTO="Ciências Exatas" 
                NOME-DA-AREA-DO-CONHECIMENTO="Ciência da Computação" 
                NOME-DA-SUB-AREA-DO-CONHECIMENTO="Inteligência Artificial" 
                NOME-DA-ESPECIALIDADE="Aprendizado de Máquina"
            />
            <AREA-DE-ATUACAO 
                NOME-GRANDE-AREA-DO-CONHECIMENTO="Engenharia" 
                NOME-DA-AREA-DO-CONHECIMENTO="Engenharia de Software" 
                NOME-DA-SUB-AREA-DO-CONHECIMENTO="DevOps" 
                NOME-DA-ESPECIALIDADE="Automação de Deploy"
            />
            <AREA-DE-ATUACAO 
                NOME-GRANDE-AREA-DO-CONHECIMENTO="Ciências Exatas" 
                NOME-DA-AREA-DO-CONHECIMENTO="Matemática Aplicada" 
                NOME-DA-SUB-AREA-DO-CONHECIMENTO="Estatística Computacional" 
                NOME-DA-ESPECIALIDADE="Big Data"
            />
            <AREA-DE-ATUACAO 
                NOME-GRANDE-AREA-DO-CONHECIMENTO="Engenharia" 
                NOME-DA-AREA-DO-CONHECIMENTO="Engenharia Elétrica" 
                NOME-DA-SUB-AREA-DO-CONHECIMENTO="Sistemas Computacionais" 
                NOME-DA-ESPECIALIDADE="Redes Neurais"
            />
            <AREA-DE-ATUACAO 
                NOME-GRANDE-AREA-DO-CONHECIMENTO="Ciências Exatas" 
                NOME-DA-AREA-DO-CONHECIMENTO="Ciência da Computação" 
                NOME-DA-SUB-AREA-DO-CONHECIMENTO="Computação em Nuvem" 
                NOME-DA-ESPECIALIDADE="Infraestrutura Distribuída"
            />
            <AREA-DE-ATUACAO 
                NOME-GRANDE-AREA-DO-CONHECIMENTO="Ciências Exatas" 
                NOME-DA-AREA-DO-CONHECIMENTO="Ciência da Computação" 
                NOME-DA-SUB-AREA-DO-CONHECIMENTO="Criptografia" 
                NOME-DA-ESPECIALIDADE="Segurança da Informação"
            />
        </AREAS-DE-ATUACAO>
    </DADOS-GERAIS>
    """).as_node


class DescribeAlanTuring:
    """Tests for researcher_from_xml function."""

    def its_owned_by_turing(self, researcher, document):
        actual = researcher_from_xml(researcher, document)

        assert actual.lattes_id == researcher

    def is_turing(self, researcher, document):
        actual = researcher_from_xml(researcher, document)

        assert actual.full_name == "Alan Mathison Turing"

    def has_quote_name(self, researcher, document):
        actual = researcher_from_xml(researcher, document)

        assert actual.quotes_names == "TURING, A. M."

    def has_caberry_orcid(self, researcher, document):
        """Caberry ORCID is a fictional person used for demonstration."""
        actual = researcher_from_xml(researcher, document)

        assert actual.orcid == "https://orcid.org/0000-0002-1825-0097"

    def has_abstract(self, researcher, document):
        actual = researcher_from_xml(researcher, document)
    
        assert actual.abstract
        assert actual.abstract.startswith("Pioneering computer scientist")

    def is_natural_brazilian(self, researcher, document):
        actual = researcher_from_xml(researcher, document)

        assert actual.nationality.born_country == "Brasil"
        assert actual.nationality.nationality == "B"

    def is_expert_at_6_areas(self, researcher, document):
        actual = researcher_from_xml(researcher, document)
        assert len(actual.expertise) == 6


class DescribeTuringExpertise:

    def is_expert_at_machine_learning(self, researcher, document):
        turing = researcher_from_xml(researcher, document)
        expertise = turing.expertise[0]

        assert expertise.major == "Ciências Exatas"
        assert expertise.area == "Ciência da Computação"
        assert expertise.sub == "Inteligência Artificial"
        assert expertise.speciality == "Aprendizado de Máquina"

    def is_expert_at_security(self, researcher, document):
        turing = researcher_from_xml(researcher, document)
        expertise = turing.expertise[-1]

        assert expertise.major == "Ciências Exatas"
        assert expertise.area == "Ciência da Computação"
        assert expertise.sub == "Criptografia"
        assert expertise.speciality == "Segurança da Informação"

    def is_expert_at_all(self, researcher, document):
        turing: Researcher = researcher_from_xml(researcher, document)
        expected = [
            ("Ciências Exatas", "Ciência da Computação", "Inteligência Artificial", "Aprendizado de Máquina"),
            ("Engenharia", "Engenharia de Software", "DevOps", "Automação de Deploy"),
            ("Ciências Exatas", "Matemática Aplicada", "Estatística Computacional", "Big Data"),
            ("Engenharia", "Engenharia Elétrica", "Sistemas Computacionais", "Redes Neurais"),
            ("Ciências Exatas", "Ciência da Computação", "Computação em Nuvem", "Infraestrutura Distribuída"),
            ("Ciências Exatas", "Ciência da Computação", "Criptografia", "Segurança da Informação"),
        ]
        for i, (major, area, sub, speciality) in enumerate(expected):
            expertise = turing.expertise[i]
            assert expertise.major == major
            assert expertise.area == area
            assert expertise.sub == sub
            assert expertise.speciality == speciality


