
from dataclasses import dataclass

from vitae.features.ingestion.adapters.institution import Institution
from vitae.features.ingestion.parsing.professional import address_from_xml
from .utils import Document, XmlString

from vitae.features.ingestion.adapters.professional import Address
import pytest

@dataclass
class SampleDocument(Document):
    address: Address

    @property
    def template(self) -> XmlString:
        template = """
        <DADOS-GERAIS>
            <RESUMO-CV/>
            <ENDERECO FLAG-DE-PREFERENCIA="ENDERECO_INSTITUCIONAL">
                <ENDERECO-PROFISSIONAL 
                    CODIGO-INSTITUICAO-EMPRESA="{institution_id}" 
                    NOME-INSTITUICAO-EMPRESA="{institution_name}" 
                    CODIGO-ORGAO="" NOME-ORGAO="" CODIGO-UNIDADE="" NOME-UNIDADE="" 
                    LOGRADOURO-COMPLEMENTO="{public_place}"
                    PAIS="{country}" 
                    UF="{state}" 
                    CEP="{cep}" 
                    CIDADE="{city}" 
                    BAIRRO="{neighborhood}" 
                    DDD="" TELEFONE="" RAMAL="" FAX="" CAIXA-POSTAL="" HOME-PAGE=""
                />
            </ENDERECO>
        </DADOS-GERAIS>
        """

        address: Address = self.address
        institution: Institution = address.institution

        return template.format(
            cep=address.cep,
            country=address.country,
            state=address.state,
            city=address.city,
            neighborhood=address.neighborhood,
            public_place=address.public_place,
            institution_id=institution.lattes_id,
            institution_name=institution.name,
        )
    

@pytest.fixture
def sample_researcher() -> str:
    return "123456789"

@pytest.fixture
def sample_address(sample_researcher: str) -> Address:
    institution = Institution(lattes_id="12345", name="Test University", abbr=None, country=None, state=None)
    return Address(
        researcher_id=sample_researcher,
        cep="12345-678",
        country="Brazil",
        state="SP",
        city="São Paulo",
        neighborhood="Centro",
        public_place="Av. Paulista, 1000",
        institution=institution,
    )


class DescribeAddressFromXml:
    """Describe address_from_xml function's behavior."""

    def it_parses_valid_address(self, sample_researcher, sample_address):
        sample = SampleDocument(sample_address).as_node
        actual = address_from_xml(sample_researcher, sample)

        assert actual is not None
        assert actual.cep == sample_address.cep
        assert actual.country == sample_address.country
        assert actual.state == sample_address.state
        assert actual.city == sample_address.city
        assert actual.neighborhood == sample_address.neighborhood
        # assert actual.public_place == sample_address.public_place
        assert actual.institution.lattes_id == sample_address.institution.lattes_id
        assert actual.institution.name == sample_address.institution.name


    def its_none_cep_is_missing(self, sample_researcher, sample_address):
        sample = SampleDocument(
            Address(
                researcher_id=sample_researcher,
                cep="",
                country=sample_address.country,
                state=sample_address.state,
                city=sample_address.city,
                neighborhood=sample_address.neighborhood,
                public_place=sample_address.public_place,
                institution=sample_address.institution,
            )
        ).as_node

        actual = address_from_xml(sample_researcher, sample)

        assert actual is None

