from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Self

import attrs

if TYPE_CHECKING:
    from vitae.infra.database import tables


def when_value_error[T](
    default_value: T,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return func(*args, **kwargs)
            except ValueError:
                return default_value

        return wrapper

    return decorator


def _should_be_upper(instance, attribute, value):
    whitespace_not_allowed = (
        "Whitespace is not allowed. Consider replace them by hyphens."
    )
    should_be_upper = "Value should be upper-cased. Use .upper() before."

    if " " in value:
        raise ValueError(whitespace_not_allowed)
    if not value.isupper():
        raise ValueError(should_be_upper)


@attrs.frozen
class AcademicTitles:
    """All Academic Titles of a Researcher."""

    titles: list[AcademicTitle]

    @property
    def highest(self) -> AcademicTitle:
        return max(self.titles)

    @classmethod
    def from_table(cls, tables: list[tables.Education]) -> Self:
        return cls([AcademicTitle.from_table(x) for x in tables])


@attrs.frozen
class AcademicTitle:
    """Researcher's Academic Title.

    This supports comparisons, so you can sort titles
    from the highest to the lowest one.

    If `_value` isn't listed in `_ORDER`,
    this is considered as being the lowest one.
    """

    _value: str = attrs.field(validator=_should_be_upper)

    @property
    def value(self) -> str:
        """Formated value."""
        return self._value.replace("-", " ").title()

    _ORDER: ClassVar[list[str]] = [
        "POS-DOUTORADO",
        "LIVRE-DOCENCIA",
        "DOUTORADO",
        "MESTRADO",
        "MESTRADO-PROFISSIONALIZANTE",
        "ESPECIALIZACAO",
        "APERFEICOAMENTO",
        "RESIDENCIA-MEDICA",
        "GRADUACAO",
        "CURSO-TECNICO-PROFISSIONALIZANTE",
        "ENSINO-MEDIO-SEGUNDO-GRAU",
        "ENSINO-FUNDAMENTAL-PRIMEIRO-GRAU",
    ]

    @when_value_error(True)
    def __lt__(self, other: AcademicTitle) -> bool:
        return self._ORDER.index(self._value) > self._ORDER.index(other._value)

    @when_value_error(False)
    def __le__(self, other: AcademicTitle) -> bool:
        return self._ORDER.index(self._value) >= self._ORDER.index(other._value)

    @when_value_error(False)
    def __gt__(self, other: AcademicTitle) -> bool:
        return self._ORDER.index(self._value) < self._ORDER.index(other._value)

    @when_value_error(False)
    def __ge__(self, other: AcademicTitle) -> bool:
        return self._ORDER.index(self._value) <= self._ORDER.index(other._value)

    @classmethod
    def from_table(cls, education: tables.Education) -> Self:
        return cls(education.category.replace(" ", "-").upper())
