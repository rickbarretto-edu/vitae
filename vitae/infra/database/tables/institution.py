"""Institution Related Database Tables."""

# ruff: noqa: FA102, D101

from .orm import Orm, required_key

__all__ = ["Institution"]


class Institution(Orm, table=True):
    lattes_id: str = required_key()
    name: str | None
    country: str | None
    state: str | None
    abbr: str | None
