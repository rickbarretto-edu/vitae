"""Institution Related Database Tables."""

# ruff: noqa: FA102, D101

from typing import TYPE_CHECKING

from .orm import Orm, link, required_key

if TYPE_CHECKING:
    from .professional import Address

__all__ = ["Institution"]


class Institution(Orm, table=True):
    lattes_id: str = required_key()
    name: str | None
    country: str | None
    state: str | None
    abbr: str | None

    addresses: list["Address"] = link("institution")

