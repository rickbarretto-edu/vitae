from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

import attrs
from sqlmodel import col, select

from vitae.infra.database import Database, tables

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.orm import Mapped


class Filters(Protocol):
    def countries(self) -> Sequence[str]: ...
    def states(self) -> Sequence[str]: ...
    def titles(self) -> Sequence[str]: ...
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

    def countries(self) -> Sequence[str]:
        return self._keywords(col(tables.Address.country))

    def states(self) -> Sequence[str]:
        return self._keywords(col(tables.Address.state))

    def titles(self) -> Sequence[str]:
        return self._keywords(col(tables.Education.category))

    def expertises(self) -> Sequence[str]:
        return self._keywords(col(tables.Expertise.sub))
