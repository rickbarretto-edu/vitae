"""Put database operations."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

    from vitae.infra.database import tables

type Some[T] = T | Iterable[T]


@dataclass
class PutOperations:
    """Operations that put data into the database."""

    engine: Engine

    def researcher(
        self,
        researcher: Some[tables.Researcher],
        nationality: Some[tables.Nationality],
        experience: Some[tables.ProfessionalExperience],
        background: Some[tables.AcademicBackground],
        expertise: Some[tables.Expertise],
    ) -> bool:
        """Put researcher's data into database.

        Returns
        -------
        If could put every single value into database.

        """
        with Session(self.engine) as session:
            try:
                session.add_all(researcher)
                session.add_all(nationality)
                session.add_all(expertise)
                session.add_all(experience)
                session.add_all(background)
                session.commit()
            except SQLAlchemyError:
                session.rollback()
                return False

        return True
