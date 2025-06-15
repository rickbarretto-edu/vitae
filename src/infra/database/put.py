"""Put database operations."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from src.infra.database import schema

type Some[T] = T | Iterable[T]


@dataclass
class PutOperations:
    """Operations that put data into the database."""

    engine: Engine

    def researcher(
        self,
        researcher: Some[schema.Researcher],
        experience: Some[schema.ProfessionalExperience],
        background: Some[schema.AcademicBackground],
        area: Some[schema.ResearchArea],
    ) -> bool:
        with Session(self.engine) as session:
            try:
                session.add_all(researcher)
                session.add_all(experience)
                session.add_all(background)
                session.add_all(area)
                session.commit()
            except SQLAlchemyError:
                session.rollback()
                return False

        return True
