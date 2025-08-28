from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Protocol

import attrs
from sqlmodel import col, select

from vitae.infra.database import Database, tables

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.orm import Mapped


class Filters(Protocol):
    @cached_property
    def countries(self) -> Sequence[str]: ...
    @cached_property
    def states(self) -> Sequence[str]: ...
    @cached_property
    def titles(self) -> Sequence[str]: ...
    @cached_property
    def expertises(self) -> Sequence[str]: ...


@attrs.frozen
class FiltersInDatabase:
    database: Database

    def _keywords(self, column: Mapped[str | None]) -> Sequence[str]:
        with self.database.session as session:
            selected = select(column).distinct()
            return sorted(
                [x for x in session.exec(selected).all() if x is not None],
            )

    @cached_property
    def countries(self) -> Sequence[str]:
        return self._keywords(col(tables.Address.country))

    @cached_property
    def states(self) -> Sequence[str]:
        return self._keywords(col(tables.Address.state))

    @cached_property
    def titles(self) -> Sequence[str]:
        return self._keywords(col(tables.Education.category))

    @cached_property
    def expertises(self) -> Sequence[str]:
        return return self._keywords(col(tables.Expertise.area))
