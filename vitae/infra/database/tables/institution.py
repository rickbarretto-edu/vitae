"""Institution Related Database Tables."""

# ruff: noqa: FA102, D101

from .orm import Orm, required_key

__all__ = ["Institution"]


class Institution(Orm, table=True):
    id: str = required_key()

    lattes_id: str | None
    name: str | None
    country: str | None
    state: str | None
    abbr: str | None
