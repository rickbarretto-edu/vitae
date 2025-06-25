import pytest

from dataclasses import dataclass

from vitae.features.ingestion.adapters.institution import Institution
from vitae.features.ingestion.parsing.professional import address_from_xml
from vitae.features.ingestion.adapters.professional import Address

from .utils import Document, XmlString


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
    institution = Institution(
        lattes_id="12345",
        name="Test University",
        abbr=None,
        country=None,
        state=None,
    )
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


def unwrap[T](x: T | None) -> T:
    assert x is not None
    return x


class DescribeValidAddressFromXml:
    """Describe address_from_xml function's behavior."""

    def has_cep(self, sample_researcher, sample_address):
        address = unwrap(address_from_xml(sample_researcher, SampleDocument(sample_address).as_node))
        assert address.cep == sample_address.cep

    def has_country(self, sample_researcher, sample_address):
        address = unwrap(address_from_xml(sample_researcher, SampleDocument(sample_address).as_node))
        assert address.country == sample_address.country
    
    def has_state(self, sample_researcher, sample_address):
        address = unwrap(address_from_xml(sample_researcher, SampleDocument(sample_address).as_node))
        assert address.state == sample_address.state
    
    def has_city(self, sample_researcher, sample_address):
        address = unwrap(address_from_xml(sample_researcher, SampleDocument(sample_address).as_node))
        assert address.city == sample_address.city

    def has_neighborhood(self, sample_researcher, sample_address):
        address = unwrap(address_from_xml(sample_researcher, SampleDocument(sample_address).as_node))
        assert address.neighborhood == sample_address.neighborhood
    
    def has_public_place(self, sample_researcher, sample_address):
        address = unwrap(address_from_xml(sample_researcher, SampleDocument(sample_address).as_node))
        assert address.public_place == sample_address.public_place

    def has_associated_institution(self, sample_researcher, sample_address):
        address = unwrap(address_from_xml(sample_researcher, SampleDocument(sample_address).as_node))
        institution = address.institution
        assert institution.lattes_id == sample_address.institution.lattes_id
        assert institution.name == sample_address.institution.name


class DescribeCEPlessAddress:
    """Describe the behavior for an Address without CEP."""

    def its_is_none(self, sample_researcher, sample_address):
        actual = address_from_xml(sample_researcher, SampleDocument(
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
        ).as_node)

        assert actual is None
