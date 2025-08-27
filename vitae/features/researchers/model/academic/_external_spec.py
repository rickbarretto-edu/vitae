
from vitae.infra.database import tables

from .external import ExternalLinks, Lattes, Orcid, InvalidURL


class DescribeLattes:
    def supports_valid_id(self):
        lattes = Lattes.from_id("1234567890123456")
        assert lattes.id == "1234567890123456"
        assert lattes.url == "http://lattes.cnpq.br/1234567890123456"

    def raises_invalid_url_for_wrong_url(self):
        import pytest
        with pytest.raises(InvalidURL):
            Lattes.from_url("http://invalid.url/1234567890123456")

    def supports_valid_url(self):
        url = "http://lattes.cnpq.br/1234567890123456"
        lattes = Lattes.from_url(url)
        assert lattes.id == "1234567890123456"
        assert lattes.url == url


class DescribeOrcid:
    def supports_valid_id(self):
        orcid = Orcid.from_id("0000-0000-0000-0000")
        assert orcid.id == "0000-0000-0000-0000"
        assert orcid.url == "http://orcid.org/0000-0000-0000-0000"

    def raises_invalid_url_when_invalid(self):
        import pytest
        with pytest.raises(InvalidURL):
            Orcid.from_url("http://invalid.org/0000-0000-0000-0000")

    def supports_valid_url(self):
        url = "http://orcid.org/0000-0000-0000-0000"
        orcid = Orcid.from_url(url)
        assert orcid.id == "0000-0000-0000-0000"
        assert orcid.url == url
