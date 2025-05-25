from dataclasses import dataclass
from typing import Iterable

from loguru import logger

from sqlmodel import Session
from sqlalchemy.engine import Engine

from src import models


@dataclass
class PutOperations:
    engine: Engine

    def researchers(self, researchers: Iterable[models.Researcher]):
        with Session(self.engine) as session:
            for researcher in researchers:
                session.add(researcher)
                logger.debug("Researcher upserted: {}", researcher)
            session.commit()

    def experiences(
        self, experiences: Iterable[models.ProfessionalExperience]
    ):
        with Session(self.engine) as session:
            for experience in experiences:
                session.add(experience)
                logger.debug("Experience upserted: {}", experience)
            session.commit()
