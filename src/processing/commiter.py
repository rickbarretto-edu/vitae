from typing import Iterable

from loguru import logger

# from sqlalchemy.dialects.postgresql import insert
# from sqlalchemy.orm import Session
from sqlmodel import Session
from sqlalchemy.engine import Engine

from src import models
from src.processing import proxies


def upsert_researchers(
    engine: Engine, researchers: Iterable[proxies.GeneralData]
):
    with Session(engine) as session:
        for researcher in researchers:
            table = models.Researcher(
                id=researcher["id"],
                name=researcher["name"] or "Invalid Name",
                city=researcher["city"],
                state=researcher["state"],
                country=researcher["country"],
                quotes_names=researcher["quotes_names"],
                orcid=researcher["orcid"],
                abstract=researcher["abstract"],
                professional_institution=researcher["professional_institution"],
                institution_state=researcher["institution_state"],
                institution_city=researcher["institution_city"],
            )
            session.add(table)
            logger.trace("Upserted: {}", table)
        session.commit()


def upsert_experiences(
    engine: Engine, experiences: Iterable[proxies.ProfessionalExperience]
):
    with Session(engine) as session:
        for experience in experiences:
            table = models.ProfessionalExperience(
                researcher_id=experience["researcher_id"],
                institution=experience["institution"] or "Unknown Institution",
                employment_relationship=experience["employment_relationship"],
                start_year=experience["start_year"],
                end_year=experience["end_year"],
            )
            session.add(table)
            logger.trace("Upserted: {}", table)
        session.commit()
