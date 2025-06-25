import pytest

from vitae.features.ingestion.parsing._xml import Node
from vitae.features.ingestion.parsing.professional import experience_from_xml

from .utils import Document


@pytest.fixture
def sample_researcher() -> str:
    return "123456789"


@pytest.fixture
def document_sample() -> Node:
    return Document.of("""
    <DADOS-GERAIS>
    <ATUACOES-PROFISSIONAIS>
        <ATUACAO-PROFISSIONAL 
            CODIGO-INSTITUICAO="1234" NOME-INSTITUICAO="University of Computer Science" >
            <VINCULOS
                TIPO-DE-VINCULO="SERVIDOR_PUBLICO"
                ANO-INICIO="2006" ANO-FIM="2013"
                OUTRO-VINCULO-INFORMADO=""
            />
            <VINCULOS
                TIPO-DE-VINCULO="SERVIDOR_PUBLICO"
                ANO-INICIO="2013" ANO-FIM="" 
                OUTRO-VINCULO-INFORMADO=""
            />
            <ATIVIDADES-DE-DIRECAO-E-ADMINISTRACAO/>
            <ATIVIDADES-DE-PESQUISA-E-DESENVOLVIMENTO>
                <PESQUISA-E-DESENVOLVIMENTO/>
            </ATIVIDADES-DE-PESQUISA-E-DESENVOLVIMENTO>
            <ATIVIDADES-DE-ENSINO><ENSINO/></ATIVIDADES-DE-ENSINO>
        </ATUACAO-PROFISSIONAL>
        <ATUACAO-PROFISSIONAL CODIGO-INSTITUICAO="5678" NOME-INSTITUICAO="Tech Innovations Inc." >
            <VINCULOS  
                TIPO-DE-VINCULO="LIVRE"
                ANO-INICIO="2001" ANO-FIM="2004" 
                OUTRO-VINCULO-INFORMADO="MSc Computer Science Student"
            />
            <VINCULOS 
                TIPO-DE-VINCULO="LIVRE"
                ANO-INICIO="2007" ANO-FIM="2009" 
                OUTRO-VINCULO-INFORMADO="PhD Computer Science Student" 
            />
        </ATUACAO-PROFISSIONAL>
    </ATUACOES-PROFISSIONAIS>
    </DADOS-GERAIS>
    """).as_node


class DescribeExperienceFromXml:
    """Tests for experience_from_xml function."""

    def has_4_entries(self, sample_researcher, document_sample):
        experiences = list(experience_from_xml(sample_researcher, document_sample))
        assert len(experiences) == 4


class DescribeFirstUCSExperience:
    def has_saple_researcher_as_owner(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[0]
        assert exp.researcher_id == sample_researcher

    def it_starts_at_2006(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[0]
        assert exp.start == 2006

    def and_ends_at_2013(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[0]
        assert exp.end == 2013

    def is_public_service_relationship(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[0]
        assert exp.relationship == "SERVIDOR_PUBLICO"

    def has_link_with_ucf(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[0]
        assert exp.institution.lattes_id == "1234"
        assert exp.institution.name == "University of Computer Science"


class DescribeSecondUCSExperience:
    def has_sample_researcher_as_owner(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[1]
        assert exp.researcher_id == sample_researcher

    def it_starts_at_2013(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[1]
        assert exp.start == 2013

    def has_no_end(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[1]
        assert exp.end is None

    def is_public_service_relationship(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[1]
        assert exp.relationship == "SERVIDOR_PUBLICO"

    def has_link_with_ucf(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[1]
        assert exp.institution.lattes_id == "1234"
        assert exp.institution.name == "University of Computer Science"


class DescribeFirstTechInnovationsExperience:
    def has_sample_researcher_as_owner(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[2]
        assert exp.researcher_id == sample_researcher

    def it_starts_at_2001(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[2]
        assert exp.start == 2001

    def and_ends_at_2004(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[2]
        assert exp.end == 2004

    def when_relationship_is_free(self, sample_researcher, document_sample):
        def its_considered_other():
            exp = list(experience_from_xml(sample_researcher, document_sample))[2]
            assert exp.relationship == "MSc Computer Science Student"
        
        its_considered_other()

    def has_link_with_tech_innovations(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[2]
        assert exp.institution.lattes_id == "5678"
        assert exp.institution.name == "Tech Innovations Inc."


class DescribeSecondTechInnovationsExperience:
    def has_sample_researcher_as_owner(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[3]
        assert exp.researcher_id == sample_researcher

    def it_starts_at_2007(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[3]
        assert exp.start == 2007

    def and_ends_at_2009(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[3]
        assert exp.end == 2009

    def when_relationship_is_free(self, sample_researcher, document_sample):
        def its_considered_other():
            exp = list(experience_from_xml(sample_researcher, document_sample))[3]
            assert exp.relationship == "PhD Computer Science Student"

        its_considered_other()

    def has_link_with_tech_innovations(self, sample_researcher, document_sample):
        exp = list(experience_from_xml(sample_researcher, document_sample))[3]
        assert exp.institution.lattes_id == "5678"
        assert exp.institution.name == "Tech Innovations Inc."

