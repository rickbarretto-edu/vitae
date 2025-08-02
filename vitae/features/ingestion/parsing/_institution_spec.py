from collections.abc import Iterable
import pytest

from vitae.features.ingestion.parsing._xml import Node
from vitae.features.ingestion.parsing.professional import experience_from_xml, address_from_xml
from vitae.features.ingestion.parsing.academic import education_from_xml

from ._test_utils import Document


@pytest.fixture
def researcher() -> str:
    return "123456789"


@pytest.fixture
def document() -> Node:
    return Document.of("""
    <DADOS-GERAIS>
        <ENDERECO>
            <ENDERECO-PROFISSIONAL 
                CODIGO-INSTITUICAO-EMPRESA="UNI001" 
                NOME-INSTITUICAO-EMPRESA="Tech University"
                CEP="123"
            />
        </ENDERECO>
        <FORMACAO-ACADEMICA-TITULACAO>
            <GRADUACAO CODIGO-INSTITUICAO="UNI001" NOME-INSTITUICAO="Tech University"/>
        </FORMACAO-ACADEMICA-TITULACAO>
        <ATUACOES-PROFISSIONAIS>
            <ATUACAO-PROFISSIONAL CODIGO-INSTITUICAO="1234" NOME-INSTITUICAO="University of Computer Science">
                <VINCULOS/>
            </ATUACAO-PROFISSIONAL>
        </ATUACOES-PROFISSIONAIS>
    </DADOS-GERAIS>
    <DADOS-COMPLEMENTARES>
        <INFORMACOES-ADICIONAIS-INSTITUICOES>
            <INFORMACAO-ADICIONAL-INSTITUICAO 
                CODIGO-INSTITUICAO="UNI001" 
                SIGLA-INSTITUICAO="TU" 
                SIGLA-UF-INSTITUICAO="SP" 
                NOME-PAIS-INSTITUICAO="Brasil" 
            />
            <INFORMACAO-ADICIONAL-INSTITUICAO 
                CODIGO-INSTITUICAO="1234" 
                SIGLA-INSTITUICAO="UCS" 
                SIGLA-UF-INSTITUICAO="RJ" 
                NOME-PAIS-INSTITUICAO="Brasil" 
            />
        </INFORMACOES-ADICIONAIS-INSTITUICOES>
    </DADOS-COMPLEMENTARES>
    """).as_node


def unwrap[T](x: T | None) -> T:
    assert x is not None
    return x

def first[T](xs: Iterable[T]) -> T:
    return list(xs)[0]

class DescribeTechUniFromProfessionalAddress:
    """Describe Institution found at professional `Address`."""

    def its_id_is_uni001(self, researcher, document):
        tech_uni = unwrap(address_from_xml(researcher, document)).institution
        assert tech_uni.lattes_id == "UNI001"

    def its_name_is_tech_uni(self, researcher, document):
        tech_uni = unwrap(address_from_xml(researcher, document)).institution
        assert tech_uni.name == "Tech University"

    def its_abbreviation_is_tu(self, researcher, document):
        tech_uni = unwrap(address_from_xml(researcher, document)).institution
        assert tech_uni.abbr == "TU"

    def its_from_brazil(self, researcher, document):
        tech_uni = unwrap(address_from_xml(researcher, document)).institution
        assert tech_uni.country == "Brasil"

    def its_from_sp(self, researcher, document):
        tech_uni = unwrap(address_from_xml(researcher, document)).institution
        assert tech_uni.state == "SP"


class DescribeUniOfCSFromProfessionalExperience:
    """Describe Institution found at professional `Experience`."""

    def its_id_is_uni001(self, researcher, document):
        tech_uni = first(experience_from_xml(researcher, document)).institution
        assert tech_uni.lattes_id == "1234"

    def its_name_is_uni_of_cs(self, researcher, document):
        tech_uni = first(experience_from_xml(researcher, document)).institution
        assert tech_uni.name == "University of Computer Science"

    def its_abbreviation_is_ucs(self, researcher, document):
        tech_uni = first(experience_from_xml(researcher, document)).institution
        assert tech_uni.abbr == "UCS"

    def its_from_brazil(self, researcher, document):
        tech_uni = first(experience_from_xml(researcher, document)).institution
        assert tech_uni.country == "Brasil"

    def its_from_rj(self, researcher, document):
        tech_uni = first(experience_from_xml(researcher, document)).institution
        assert tech_uni.state == "RJ"


class DescribeTechUniFromEducation:
    """Describe Institution got from `Education`."""

    def its_the_same_from_address(self, researcher, document):
        from_address = unwrap(address_from_xml(researcher, document)).institution
        from_education = first(education_from_xml(researcher, document)).institution

        assert from_address == from_education