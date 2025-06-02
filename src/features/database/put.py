"""Put database operations."""

from collections.abc import Iterable
from dataclasses import dataclass

from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, Session

from src import models


@dataclass
class PutOperations:
    """Operations that puts data on the database."""

    engine: Engine

    def researchers(self, researchers: Iterable[models.Researcher]) -> None:
        """Insert multiple researchers."""
        with Session(self.engine) as session:
            for researcher in researchers:
                session.add(researcher)
                session.commit()

    def researcher(self, researcher: models.Researcher) -> None:
        """Insert a researcher."""
        self._put(researcher)

    def experiences(
        self,
        experiences: Iterable[models.ProfessionalExperience],
    ) -> None:
        """Insert multiple Researcher's Professional Experience."""
        with Session(self.engine) as session:
            for experience in experiences:
                session.add(experience)
                session.commit()

    def experience(self, experience: models.ProfessionalExperience) -> None:
        """Insert a Researcher's Professional Experience."""
        self._put(experience)

    def academic_background(
        self,
        background: models.AcademicBackground,
    ) -> None:
        """Insert a Researcher's Academic Background."""
        self._put(background)

    def research_area(self, area: models.ResearchArea) -> None:
        """Insert a Researcher's Area of Research."""
        self._put(area)

    def _put(self, model: SQLModel) -> None:
        """Insert SQLModel on database and commit it."""
        with Session(self.engine) as session:
            session.add(model)
            session.commit()
