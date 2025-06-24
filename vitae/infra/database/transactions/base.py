"""Base class for Transactions."""

import abc
from collections.abc import Iterator

from sqlmodel import SQLModel


class Transaction(abc.ABC):
    """Database Transaction abstraction.

    This Abstract Class defines the interface and semantic for
    a Database Transaction. As such, internal types are not defines here
    and each subclass is free to implement this on its own way.

    Its internal types may be of any kind,
    but since this is into `database` package, it should, preferably be,
    database's models composition.

    The transaction must define an iteration method `__iter__`
    that iterates over desired types that returns a database model.
    This makes possible for generic database operations
    with multiple models at once.

    Notice that `Transaction`s must define the right order of insertion.

    Examples
    --------
        class Championship(Transaction):
            teams: list[Team]
            referencees: list[Referencee]
            staff: list[Staff]

            def __iter__(self) -> Iterable[SQLModel]:
                yield from self.teams
                yield from self.referencees
                yield from self.staff

        championship = Championship(
            teams=[Team(...), Team(...), Team(...), ...]
            referencees=[Referencee(...), Referencee(...), ...]
            staff=[Staff(...), Staff(...), Staff(...), ...]
        )
        session.add_all(championship)

    """

    @abc.abstractmethod
    def __iter__(self) -> Iterator[SQLModel]:  # noqa: D105
        pass
