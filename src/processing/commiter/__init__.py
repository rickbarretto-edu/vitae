from loguru import logger
from sqlalchemy.dialects.postgresql import insert

from src.database.database_config import database_config

from src.models import (
    AcademicBackground,
    KnowledgeArea,
    ProfessionalExperience,
    ResearchArea,
    Researcher,
)

# TODO: PostgreSQL is not being updated, probably the issues resides in this module.

# TODO: Exceptions should be logged by using a decorator, as it is for ``parsing.parser``.


class Load:
    def __init__(self, session):
        self.session = session

    # TODO: Probably this logic is being too resource consuming without that much effect.
    # 1st: This checks uniqueness for a small set of data, delimited by the buffer.
    #  So, this is not actually checking a thing really.
    # 2nd: This is an O(N) algorithm that checks each field for 40GB of data.
    #
    # I guess, the only way of having duplicate fields is by having duplicated XML files,
    # so, we just need to check for the researcher ID.
    def remove_duplicates(self, batch, unique_keys):
        """
        Removes duplicates from a batch based on unique keys.
        """
        seen = set()
        unique_batch = []
        for record in batch:
            key = tuple(record[key] for key in unique_keys)
            if key not in seen:
                seen.add(key)
                unique_batch.append(record)
        return unique_batch

    def upsert_researcher(self, batch):
        if not batch:
            return
        try:
            query = insert(Researcher).values(batch)
            update_dict = {
                key: getattr(query.excluded, key)
                for key in batch[0]
                if key != "id"
            }

            query = query.on_conflict_do_update(
                index_elements=["id"], set_=update_dict
            )

            self.session.execute(query)
            self.session.commit()
        except Exception as exception:
            logger.error("Erro no upsert_researcher: {}", exception)
            self.session.rollback()

    def upsert_professional_experience(self, batch):
        if not batch:
            return
        try:
            unique_keys = [
                "institution",
                "employment_relationship",
                "start_year",
                "end_year",
                "researcher_id",
            ]
            batch = self.remove_duplicates(batch, unique_keys)
            query = insert(ProfessionalExperience).values(
                batch
            )  # Corrigido: Agora insere na tabela correta

            update_dict = {
                key: getattr(query.excluded, key)
                for key in batch[0]
                if key != "id"
            }

            query = query.on_conflict_do_update(
                index_elements=[
                    "institution",
                    "employment_relationship",
                    "start_year",
                    "end_year",
                    "researcher_id",
                ],
                set_=update_dict,
            )

            self.session.execute(query)
            self.session.commit()
        except Exception as exception:
            logger.error("Erro no upsert_professional_experience: {}", exception)
            self.session.rollback()

    def upsert_research_area(self, batch):
        if not batch:
            return
        try:
            unique_keys = [
                "major_knowledge_area",
                "knowledge_area",
                "sub_knowledge_area",
                "specialty",
                "researcher_id",
            ]
            batch = self.remove_duplicates(batch, unique_keys)
            query = insert(ResearchArea).values(batch)

            update_dict = {
                key: getattr(query.excluded, key)
                for key in batch[0]
                if key != "id"
            }

            query = query.on_conflict_do_update(
                index_elements=[
                    "major_knowledge_area",
                    "knowledge_area",
                    "sub_knowledge_area",
                    "specialty",
                    "researcher_id",
                ],
                set_=update_dict,
            )

            self.session.execute(query)
            self.session.commit()
        except Exception as exception:
            logger.error("Error when upserting Research Area: {}", exception)
            self.session.rollback()

    def upsert_knowledge_area(self, batch):
        if not batch:
            return
        try:
            unique_keys = [
                "major_knowledge_area",
                "knowledge_area",
                "sub_knowledge_area",
                "specialty",
                "researcher_id",
            ]
            batch = self.remove_duplicates(batch, unique_keys)
            query = insert(KnowledgeArea).values(batch)

            update_dict = {
                key: getattr(query.excluded, key)
                for key in batch[0]
                if key != "id"
            }

            query = query.on_conflict_do_update(
                index_elements=[
                    "major_knowledge_area",
                    "knowledge_area",
                    "sub_knowledge_area",
                    "specialty",
                    "researcher_id",
                ],
                set_=update_dict,
            )

            self.session.execute(query)
            self.session.commit()
        except Exception as exception:
            logger.error("Erro no upsert_knowledge_area: {}", exception)
            self.session.rollback()

    def upsert_academic_background(self, batch):
        if not batch:
            return
        try:
            unique_keys = [
                "type",
                "institution",
                "course",
                "start_year",
                "end_year",
                "researcher_id",
            ]
            batch = self.remove_duplicates(batch, unique_keys)
            query = insert(AcademicBackground).values(batch)

            update_dict = {
                key: getattr(query.excluded, key)
                for key in batch[0]
                if key != "id"
            }

            query = query.on_conflict_do_update(
                index_elements=[
                    "type",
                    "institution",
                    "course",
                    "start_year",
                    "end_year",
                    "researcher_id",
                ],
                set_=update_dict,
            )

            self.session.execute(query)
            self.session.commit()
        except Exception as exception:
            logger.error("Erro no upsert_academic_background: {}", exception)
            self.session.rollback()


# TODO: singleton pattern should be purged from codebase
session = database_config.session_local()
load = Load(session)
