"""Put database operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

    from .transactions import Curricula


@dataclass
class PutOperations:
    """Operations that put data into the database."""

    engine: Engine

    def batch_transaction(self, curricula: Curricula) -> bool:
        """Put a batch of Curriulum into database.

        Use this method when you need to push a huge amount of data.
        Group them into `Curricula`.

        Returns
        -------
        If could put every single value into database.

        """
        with Session(self.engine) as session:
            try:
                session.add_all(curricula)
                session.commit()
            except SQLAlchemyError:
                session.rollback()
                return False

        return True
