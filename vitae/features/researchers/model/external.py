from __future__ import annotations

import re
from typing import Self

import attrs


class InvalidURL(ValueError):  # noqa: N818
    pass


@attrs.frozen
class Lattes:
    """Researcher's Lattes.

    Lattes has an ID of the type: 0000000000000000,
    and also an associated URL.
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

    Orcid has an ID of the type: 0000-0000-0000-0000,
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
        host = r"orcid\.org"
        match = re.search(rf"{host}/([\d\-]+)", url)

        if not match:
            message = "Invalid Orcid URL"
            raise InvalidURL(message)

        orcid_id = match.group(1)
        return cls(orcid_id)
