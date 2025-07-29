"""Academic Titles models."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar, Self

import attrs

if TYPE_CHECKING:
    from vitae.infra.database import tables

__all__ = [
    "AcademicDegree",
    "AcademicTitles",
]


def _should_be_scream_case(instance, attribute, value) -> None:
    """Attrs validator for scream-case.

    Sream-case is all-uppercased letters separated by underscores,
    i.e.: 'SCREAM_CASE'.

    Note:
    ----
    `instance` and `attribute` are required parameters by attrs,
    but not used in this function.

    Raises:
    ------
    ValueError

    """
    pattern = r"^[A-Z]+(_[A-Z]+)*$"
    if not re.fullmatch(pattern, value):
        message = (
            "Value must be SCREAM_CASE: "
            "all uppercase letters separated by underscores."
        )
        raise ValueError(message)


@attrs.frozen
class AcademicTitles:
    """All Academic Titles of a Researcher."""

    _degrees: list[AcademicDegree]

    @property
    def titles(self) -> list[AcademicDegree]:
        return sorted([degree for degree in self._degrees if degree.has_title])

    @property
    def highest(self) -> AcademicDegree | None:
        if self.titles:
            return self.titles[-1]
        return None

    @classmethod
    def from_tables(cls, tables: list[tables.Education]) -> Self:
        return cls([AcademicDegree.from_table(x) for x in tables])


@attrs.frozen
class AcademicDegree:
    """Researcher's Academic Degree.

    This supports comparisons, so you can sort degrees
    from the highest to the lowest one.

    If `_name` isn't listed in `_ORDER`,
    this is considered as being the lowest one.
    """

    _name: str = attrs.field(validator=_should_be_scream_case)
    begin: int | None = None
    finish: int | None = None

    @property
    def has_title(self) -> bool:
        return self.finish is not None

    @property
    def title(self) -> str:
        """Formated value."""
        return self._FORMATED_KNOWN_PORTUGUESE_TITLES[self._name]

    def __str__(self) -> str:
        return self.title

    _FORMATED_KNOWN_PORTUGUESE_TITLES: ClassVar[dict[str, str]] = {
        "POS_DOUTORADO": "Pós-doutorado",
        "LIVRE_DOCENCIA": "Livre-docência",
        "DOUTORADO": "Doutorado",
        "MESTRADO": "Mestrado",
        "MESTRADO_PROFISSIONALIZANTE": "Mestrado Profissionalizante",
        "ESPECIALIZACAO": "Especialização",
        "APERFEICOAMENTO": "Aperfeiçoamento",
        "RESIDENCIA_MEDICA": "Residência Médica",
        "GRADUACAO": "Graduação",
        "CURSO_TECNICO_PROFISSIONALIZANTE": "Curso Técnico",
        "ENSINO_MEDIO_SEGUNDO_GRAU": "Segundo Grau",
        "ENSINO_FUNDAMENTAL_PRIMEIRO_GRAU": "Primeiro Grau",
    }

    @property
    def rank(self) -> int:
        """Title's rank.

        If value is not found between known titles,
        this is considered the least significant as possible.
        """
        keys = list(self._FORMATED_KNOWN_PORTUGUESE_TITLES.keys())
        try:
            return len(keys) - keys.index(self._name)
        except ValueError:
            return -1

    def __lt__(self, other: AcademicDegree) -> bool:
        """Compare Title's rank."""
        return self.rank < other.rank

    def __eq__(self, other: AcademicDegree) -> bool:
        """Compare Title's rank."""
        return self.rank == other.rank

    @classmethod
    def from_table(cls, education: tables.Education) -> Self:
        return cls(
            education.category.replace("-", "_").upper(),
            begin=education.start,
            finish=education.end,
        )
