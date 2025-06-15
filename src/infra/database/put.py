"""Put database operations."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from src.infra.database import schema


@dataclass
class PutOperations:
    """Operations that put data into the database."""

    engine: Engine

    def each(
        self,
        researcher: schema.Researcher | Iterable[schema.Researcher],
        experience: schema.ProfessionalExperience
        | Iterable[schema.ProfessionalExperience],
        background: schema.AcademicBackground
        | Iterable[schema.AcademicBackground],
        area: schema.ResearchArea | Iterable[schema.ResearchArea],
    ) -> bool:
        with Session(self.engine) as session:
            try:
                session.add(researcher)
                session.add_all(experience)
                session.add_all(background)
                session.add_all(area)
                session.commit()
            except SQLAlchemyError:
                session.rollback()
                # TODO: log this somewhere
                return False

        return True
