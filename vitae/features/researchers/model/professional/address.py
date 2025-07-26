from __future__ import annotations

from typing import TYPE_CHECKING

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


@attrs.frozen
class State:
    abbr: str = attrs.field(converter=as_upper)


@attrs.frozen
class Country:
    name: str = attrs.field(converter=as_title)


@attrs.frozen
class Address:
    """Researcher's Address."""

    city: City
    state: State
    country: Country

    def __str__(self) -> str:
        match self:
            case Address(city, state, country="Brasil"):
                return f"{city} ({state})"
            case Address(city, state, country):
                return f"{city} ({state}), {country}"
            case _:
                return ""

    @classmethod
    def from_table(cls, table: tables.Address) -> Address:
        return cls(
            city=City(table.city),
            state=State(table.state),
            country=Country(table.country),
        )
