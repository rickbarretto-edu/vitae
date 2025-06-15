from pathlib import Path
import pprint

from sqlmodel import Session, create_engine, select

from src.infra.database.schema import Researcher
from src.settings import VitaeSettings

__all__ = ["display_first_20th_data"]


def display_first_20th_data(vitae: VitaeSettings) -> None:
    """Display the first 20th data.

    This function was designed for debugging purposes only.
    And should be used after the ingestion process to ensure correctness.

    Also, this shows all nested relationships, so you can verify
    if they are working.
    """
    engine = create_engine(vitae.postgres.url)
    with Session(engine) as session:
        researchers = session.exec(select(Researcher).limit(20))

        with Path("logs/20th.log").open("+w", encoding="utf-8") as file:

            def pp[T](x: T):
                return pprint.pp(x, file, width=72, indent=4)

            for researcher in researchers:
                pp(researcher)

                for experience in researcher.professional_experience:
                    pp(experience)

                for area in researcher.research_area:
                    pp(area)

                for background in researcher.academic_background:
                    pp(background)

                    for knowledge in background.knowledge_area:
                        pp(knowledge)

                pp(
                    "-------------------------------------------------------",
                )
