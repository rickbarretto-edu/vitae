from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Literal, Protocol

import attrs
from sqlalchemy import Select
from sqlmodel import and_, col, select

from vitae.features.researchers.model.researcher import Researcher
from vitae.features.researchers.schemes import ChoosenFilters
from vitae.infra.database import Database, tables

if TYPE_CHECKING:
    from collections.abc import Iterable


type Order = Literal["asc", "desc"] | None
INVALID_ORDER_LITERAL = "order_by must be 'asc', 'desc', or None"

type SelectedResearchers = Select[tuple[tables.Researcher]]


# fmt: off
def using_filter(
    selected: SelectedResearchers,
    filters: ChoosenFilters | None,
) -> SelectedResearchers:

    if not filters:
        return selected

    if filters.get("started"):
        selected = selected.join(tables.Education).where(
            col(tables.Education.category) == filters["started"])

    if filters.get("has_finished"):
        selected = selected.where(
            col(tables.Education.end).is_not(None))

    if filters.get("expertise"):
        selected = selected.join(tables.Expertise).where(
            col(tables.Expertise.sub) == filters["expertise"])

    if filters.get("state"):
        selected = selected.join(tables.Address).where(
            col(tables.Address.state) == filters["state"])

    if filters.get("country"):
        selected = selected.where(
            col(tables.Address.country) == filters["country"])

    return selected.distinct()

# fmt: on


def ordered_by_name(
    selected: SelectedResearchers,
    order: Order | None,
) -> SelectedResearchers:
    a_z = col(tables.Researcher.full_name).asc()
    z_a = col(tables.Researcher.full_name).desc()

    match order:
        case "asc":
            return selected.order_by(a_z)
        case "desc":
            return selected.order_by(z_a)
        case None:
            return selected
        case _:
            raise ValueError(INVALID_ORDER_LITERAL)


class Researchers(Protocol):
    """Researchers's interface."""

    def by_id(self, lattes_id: str) -> Researcher | None: ...

    def by_name(
        self,
        name: str,
        researchers: int,
        page: int,
        order_by: Order,
        filter_by: ChoosenFilters | None,
    ) -> Iterable[Researcher]: ...

    def stricly_by_name(
        self,
        name: str,
        researchers: int,
        page: int,
        order_by: Order,
        filter_by: ChoosenFilters | None,
    ) -> Iterable[Researcher]: ...


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

    def stricly_by_name(
        self,
        name: str,
        researchers: int = 50,
        page: int = 1,
        order_by: Order = None,
        filter_by: ChoosenFilters | None = None,
    ) -> Iterable[Researcher]:
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
        has_name = col(tables.Researcher.full_name).ilike(f"%{name}%")
        offset = researchers * (page - 1)

        with self.database.session as session:
            selected = select(tables.Researcher).where(
                has_name if name else True,
            )
            filtered = using_filter(selected, filter_by)
            ordered = ordered_by_name(filtered, order_by)
            limited = ordered.offset(offset).limit(researchers)

            result: list[tables.Researcher] = session.exec(limited).all()  # type: ignore
            return [Researcher.from_table(r) for r in result]

    def by_name(
        self,
        name: str,
        researchers: int = 50,
        page: int = 1,
        order_by: Order = None,
        filter_by: ChoosenFilters | None = None,
    ) -> Iterable[Researcher]:
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
        each_name = name.split()
        offset = researchers * (page - 1)

        has_names = [
            col(tables.Researcher.full_name).ilike(f"%{name_token}%")
            for name_token in each_name
        ]

        with self.database.session as session:
            selected = select(tables.Researcher).where(
                and_(*has_names) if name else True,
            )
            filtered = using_filter(selected, filter_by)
            ordered = ordered_by_name(filtered, order_by)
            limited = ordered.offset(offset).limit(researchers)

            result: list[tables.Researcher] = session.exec(limited).all()  # type: ignore
            return [Researcher.from_table(r) for r in result]
