from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

import attrs
from sqlmodel import and_, col, select

from vitae.features.researchers.model.researcher import Researcher
from vitae.infra.database import Database, tables

if TYPE_CHECKING:
    from collections.abc import Iterable


class Researchers(Protocol):
    """Researchers's interface."""

    def by_id(self, lattes_id: str) -> Researcher | None: ...
    def by_name(self, name: str) -> Iterable[Researcher]: ...


@attrs.frozen
class ResearchersInDatabase(Researchers):
    database: Database

    def by_id(self, lattes_id: str) -> Researcher | None:
        """Fetch a Researcher by its Lattes ID.

        The Lattes ID must be exactly the same.

        Returns
        -------
        A Researcher if any.

        """
        with self.database.session as session:
            result = session.exec(
                select(tables.Researcher).where(
                    col(tables.Researcher.lattes_id) == lattes_id,
                ),
            ).first()

            if result:
                return Researcher.from_table(result)
            return None

    def stricly_by_name(self, name: str, n: int = 50) -> Iterable[Researcher]:
        """Fetch Researchers by name.

        The query name does not need to match the first name,
        but this needs to strictly follow the correct sequence.

        Use this if the performance of `by_name` is significantly
        affecting the system.

        Scenario
        --------
        Given I have "Josiah Stinkney Carberry",
        When I look for "Josiah Caberry", I'll not find him.
        But, when I look for "Josiah Stinkney" or "Stinkney Carberry", I'll.

                >>> assert (
                ...     researchers.loosely_by_name("Josiah Stinkney")
                ...     is Researcher
                ... )
                >>> assert (
                ...     researchers.loosely_by_name("Stinkney Carberry")
                ...     is Researcher
                ... )
                >>> assert (
                ...     researchers.loosely_by_name("Josiah Carberry") is None
                ... )

        Returns
        -------
        Iterable[Researcher] of n researchers.

        """
        with self.database.session as session:
            result = session.exec(
                select(tables.Researcher)
                .where(col(tables.Researcher.full_name).ilike(f"%{name}%"))
                .limit(n),
            )

            return [Researcher.from_table(r) for r in result]

    def by_name(self, name: str, n: int = 50) -> Iterable[Researcher]:
        """Fetch Researchers by name.

        This query may be slower than `stricly_by_name`,
        but this is also more broad, and gives better results.
        For this, names may be searched in any order of sequence.

        Scenario
        --------
        Given I have "Josiah Stinkney Carberry",
        When I search by "Josiah Caberry" or "Caberry Stinkney",
        I'll be able to find him.

                >>> assert (
                ...     researchers.loosely_by_name("Josiah Caberry")
                ...     is Researcher
                ... )
                >>> assert (
                ...     researchers.loosely_by_name("Caberry Stinkney")
                ...     is Researcher
                ... )

        Returns
        -------
        Iterable[Researcher] of n researchers.

        """
        words = name.split()

        conditions = [
            col(tables.Researcher.full_name).ilike(f"%{word}%")
            for word in words
        ]

        with self.database.session as session:
            result = session.exec(
                select(tables.Researcher).where(and_(*conditions)).limit(n),
            )
            return [Researcher.from_table(r) for r in result]
