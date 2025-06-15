"""Put database operations."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from sqlalchemy.engine import Engine
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
    ) -> None:
        with Session(self.engine) as session:
            session.add(researcher)
            session.add_all(experience)
            session.add_all(background)
            session.add_all(area)
            session.commit()
