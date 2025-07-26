from __future__ import annotations

from typing import TYPE_CHECKING, Self

import attrs

if TYPE_CHECKING:
    from vitae.infra.database import tables


__all__ = [
    "Address",
    "City",
    "Country",
    "State",
]


def force_str(val: str | None) -> str:
    return val or ""


as_title = attrs.converters.pipe(
    force_str,
    lambda x: x.title(),
)

as_upper = attrs.converters.pipe(
    force_str,
    lambda x: x.upper(),
)


@attrs.frozen
class City:
    name: str = attrs.field(converter=as_title)

    def __str__(self) -> str:
        return self.name


@attrs.frozen
class State:
    abbr: str = attrs.field(converter=as_upper)

    def __str__(self) -> str:
        return self.abbr


@attrs.frozen
class Country:
    name: str = attrs.field(converter=as_title)

    def __str__(self) -> str:
        return self.name


@attrs.frozen
class Address:
    """Researcher's Address."""

    city: City
    state: State
    country: Country

    def __str__(self) -> str:
        if self.country == Country("Brasil"):
            return f"{self.city} ({self.state})"
        return f"{self.city} ({self.state}), {self.country}"

    @classmethod
    def from_table(cls, table: tables.Address) -> Address:
        return cls(
            city=City(table.city),
            state=State(table.state),
            country=Country(table.country),
        )
