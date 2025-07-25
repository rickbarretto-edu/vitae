from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

import attrs
from sqlmodel import col, select

from vitae.features.researchers.model.researcher import Researcher
from vitae.infra.database import Database, tables

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sqlalchemy import Engine


class Researchers(Protocol):
    """Researchers's interface."""

    def by_id(self, lattes_id: str) -> Researcher | None: ...
    def by_name(self, name: str) -> Iterable[Researcher]: ...


@attrs.frozen
class ResearchersInDatabase(Researchers):
    database: Database

    def by_id(self, lattes_id: str) -> Researcher | None:
        with self.database.session as session:
            result = session.exec(
                select(tables.Researcher).where(
                    col(tables.Researcher.lattes_id) == lattes_id,
                ),
            ).first()

            if result:
                return Researcher.from_table(result)
            return None

    def by_name(self, name: str) -> Iterable[Researcher]:
        return []
