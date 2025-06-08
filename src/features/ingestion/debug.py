import pprint

from sqlmodel import Session, create_engine, select

from src.infra.database.models import Researcher
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

        print(
            "##############################################################################",
        )

        for researcher in researchers:
            pprint.pp(researcher)

            for experience in researcher.professional_experience:
                pprint.pp(experience)

            for area in researcher.research_area:
                pprint.pp(area)

            for background in researcher.academic_background:
                pprint.pp(background)

                for knowledge in background.knowledge_area:
                    pprint.pp(knowledge)

            print("-------------------------------------------------------")
