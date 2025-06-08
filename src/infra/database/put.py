"""Put database operations."""

from dataclasses import dataclass

from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, Session

from src.infra.database import schema


@dataclass
class PutOperations:
    """Operations that puts data on the database."""

    engine: Engine

    def researcher(self, researcher: schema.Researcher) -> None:
        """Insert a researcher."""
        self._put(researcher)

    def experience(self, experience: schema.ProfessionalExperience) -> None:
        """Insert a Researcher's Professional Experience."""
        self._put(experience)

    def academic_background(
        self,
        background: schema.AcademicBackground,
    ) -> None:
        """Insert a Researcher's Academic Background."""
        self._put(background)

    def research_area(self, area: schema.ResearchArea) -> None:
        """Insert a Researcher's Area of Research."""
        self._put(area)

    def _put(self, model: SQLModel) -> None:
        """Insert SQLModel on database and commit it."""
        with Session(self.engine) as session:
            session.add(model)
            session.commit()
