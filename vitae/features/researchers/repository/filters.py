from collections.abc import Sequence
from typing import Protocol

import attrs
from sqlmodel import select

from vitae.infra.database import Database, tables


class Filters(Protocol):
    def countries(self) -> Sequence[str]: ...
    def states(self) -> Sequence[str]: ...
    def titles(self) -> Sequence[str]: ...
    def expertises(self) -> Sequence[str]: ...


@attrs.frozen
class FiltersInDatabase:
    database: Database

    def countries(self) -> Sequence[str]:
        with self.database.session as session:
            selected = select(tables.Address.country).distinct()
            return sorted(
                [x for x in session.exec(selected).all() if x is not None],
            )

    def states(self) -> Sequence[str]:
        with self.database.session as session:
            selected = select(tables.Address.state).distinct()
            return sorted(
                [x for x in session.exec(selected).all() if x is not None],
            )

    def titles(self) -> Sequence[str]:
        with self.database.session as session:
            selected = select(tables.Education.category).distinct()
            return sorted(
                [x for x in session.exec(selected).all() if x is not None],
            )

    def expertises(self) -> Sequence[str]:
        with self.database.session as session:
            selected = select(tables.Expertise.sub).distinct()
            return sorted(
                [x for x in session.exec(selected).all() if x is not None],
            )
