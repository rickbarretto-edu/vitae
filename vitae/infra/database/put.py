"""Put database operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel, Session

from vitae.infra.database.tables.institution import Institution

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

    from .transactions import Curricula, Institutions


@dataclass
class PutOperations:
    """Operations that put data into the database."""

    engine: Engine

    def batch_transaction(
        self,
        institutions: Institutions,
        curricula: Curricula,
    ) -> bool:
        """Put a batch of Curriulum into database.

        Use this method when you need to push a huge amount of data.
        Group them into `Curricula`.

        Returns
        -------
        If could put every single value into database.

        """
        with Session(self.engine) as session:
            try:
                print(list(institutions))
                for institution in institutions:
                    session.execute(
                        postgresql.insert(Institution)
                        .values(
                            **institution.model_dump(),
                        )
                        .on_conflict_do_nothing()
                    )

                session.add_all(
                    table for table in curricula if isinstance(table, SQLModel)
                )
                session.commit()
            except SQLAlchemyError:
                session.rollback()
                return False

        return True
