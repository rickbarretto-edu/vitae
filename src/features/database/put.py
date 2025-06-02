from collections.abc import Iterable
from dataclasses import dataclass

from loguru import logger
from sqlalchemy.engine import Engine
from sqlmodel import Session

from src import models


@dataclass
class PutOperations:
    engine: Engine

    def researchers(self, researchers: Iterable[models.Researcher]) -> None:
        with Session(self.engine) as session:
            for researcher in researchers:
                session.add(researcher)
                session.commit()

    def researcher(self, researcher: models.Researcher) -> None:
        with Session(self.engine) as session:
            session.add(researcher)
            session.commit()

    def experiences(
        self,
        experiences: Iterable[models.ProfessionalExperience],
    ) -> None:
        with Session(self.engine) as session:
            for experience in experiences:
                session.add(experience)
                session.commit()

    def experience(self, experience: models.ProfessionalExperience) -> None:
        with Session(self.engine) as session:
            session.add(experience)
            session.commit()

    def academic_background(
        self, background: models.AcademicBackground,
    ) -> None:
        with Session(self.engine) as session:
            session.add(background)
            session.commit()
