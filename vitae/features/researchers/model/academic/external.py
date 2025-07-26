"""External websites models."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Self

import attrs

from vitae.features.researchers.lib import optional

if TYPE_CHECKING:
    from vitae.infra.database import tables

__all__ = [
    "ExternalLinks",
    "Lattes",
    "Orcid",
]


@attrs.frozen
class ExternalLinks:
    """Researcher's links to external websites.

    Orcid is optional.
    """

    lattes: Lattes
    orcid: Orcid | None

    @classmethod
    def from_table(cls, researcher: tables.Researcher):
        return cls(
            lattes=Lattes.from_id(researcher.lattes_id),
            orcid=optional(researcher.orcid, Orcid.from_url),
        )


class InvalidURL(ValueError):  # noqa: N818
    pass


@attrs.frozen
class Lattes:
    """Researcher's Lattes.

    Lattes has an ID of 16-digits and also an associated URL.
    """

    id: str = attrs.field(
        validator=attrs.validators.matches_re(r"^\d{16}$"),
    )

    @property
    def url(self) -> str:
        return f"http://lattes.cnpq.br/{self.id}"

    @classmethod
    def from_id(cls, id: str) -> Self:
        return cls(id)

    @classmethod
    def from_url(cls, url: str) -> Self:
        """Lattes given a Lattes' URL.

        A valid URL has "lattes.cnpq.br/{id}"

        Returns
        -------
        Self.

        Raises
        ------
        InvalidURL

        """
        host = r"lattes\.cnpq\.br"
        match = re.search(rf"{host}/(\d+)", url)

        if not match:
            message = "Invalid Lattes URL"
            raise InvalidURL(message)

        lattes_id = match.group(1)
        return cls(lattes_id)


@attrs.frozen
class Orcid:
    """Researcher's Orcid.

    Orcid has an ID of 4 groups of 4-digits separated by hyphen,
    i.e.: "0000-0000-0000-0000",
    and also an associated URL.
    """

    id: str = attrs.field(
        validator=attrs.validators.matches_re(r"^\d{4}-\d{4}-\d{4}-\d{4}$"),
    )

    @property
    def url(self) -> str:
        return f"http://orcid.org/{self.id}"

    @classmethod
    def from_id(cls, id: str) -> Self:
        return cls(id)

    @classmethod
    def from_url(cls, url: str) -> Self:
        """Orcid given a Lattes' URL.

        A valid URL has "orcid.org/{id}"

        Returns
        -------
        Self

        Raises
        ------
        InvalidURL

        """
        host = r"orcid\.org"
        match = re.search(rf"{host}/([\d\-]+)", url)

        if not match:
            message = "Invalid Orcid URL"
            raise InvalidURL(message)

        orcid_id = match.group(1)
        return cls(orcid_id)
