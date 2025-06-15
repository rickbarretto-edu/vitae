"""Put database operations."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, Session

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
        self.researcher(researcher)
        self.experience(experience)
        self.academic_background(background)
        self.research_area(area)

    def researcher(
        self,
        researcher: schema.Researcher | Iterable[schema.Researcher],
    ) -> None:
        """Insert one or more researchers."""
        self._put(researcher)

    def experience(
        self,
        experience: schema.ProfessionalExperience
        | Iterable[schema.ProfessionalExperience],
    ) -> None:
        """Insert one or more Professional Experiences."""
        self._put(experience)

    def academic_background(
        self,
        background: schema.AcademicBackground
        | Iterable[schema.AcademicBackground],
    ) -> None:
        """Insert one or more Academic Backgrounds."""
        self._put(background)

    def research_area(
        self,
        area: schema.ResearchArea | Iterable[schema.ResearchArea],
    ) -> None:
        """Insert one or more Research Areas."""
        self._put(area)

    def _put(self, data: SQLModel | Iterable[SQLModel]) -> None:
        """Insert SQLModel(s) into the database and commit them."""
        with Session(self.engine) as session:
            if isinstance(data, SQLModel):
                session.add(data)
            else:
                session.add_all(list(data))
            session.commit()
