from dataclasses import dataclass
from typing import List, Dict, Any

from loguru import logger

# from sqlalchemy.dialects.postgresql import insert
# from sqlalchemy.orm import Session
from sqlmodel import create_engine, Session
from sqlalchemy.engine import Engine

from src import models
from src.processing import proxies
from src.settings import VitaeSettings


@dataclass
class UpsertService:
    engine: Engine

    def remove_duplicates(
        self, batch: List[Dict[str, Any]], unique_keys: List[str]
    ) -> List[Dict[str, Any]]:
        seen = set()
        unique_batch = []
        for record in batch:
            key = tuple(record.get(key) for key in unique_keys)
            if key not in seen:
                seen.add(key)
                unique_batch.append(record)
        return unique_batch

    # def filter_existing_researchers(
    #     self, batch: List[Dict[str, Any]]
    # ) -> List[Dict[str, Any]]:
    #     existing_ids = {r[0] for r in self.session.query(Researcher.id).all()}
    #     return [
    #         record
    #         for record in batch
    #         if record.get("researcher_id") in existing_ids
    #     ]

    def upsert_researcher(self, researchers: list[proxies.GeneralData]):
        with Session(self.engine) as session:
            for researcher in researchers:
                logger.trace("Inserting: {}", researcher)
                session.add(
                    models.Researcher(
                        name=researcher["name"] or "Invalid Name",
                        city=researcher["city"],
                        state=researcher["state"],
                        country=researcher["country"],
                        quotes_names=researcher["quotes_names"],
                        orcid=researcher["orcid"],
                        abstract=researcher["abstract"],
                    )
                )

    def upsert_professional_experience(self, batch: List[Dict[str, Any]]):
        # if not batch:
        #     return
        # try:
        #     unique_keys = [
        #         "institution",
        #         "employment_relationship",
        #         "start_year",
        #         "end_year",
        #         "researcher_id",
        #     ]
        #     batch = self.remove_duplicates(batch, unique_keys)
        #     batch = self.filter_existing_researchers(batch)
        #     if not batch:
        #         return
        #     query = insert(ProfessionalExperience).values(batch)
        #     query = query.on_conflict_do_nothing(index_elements=unique_keys)
        #     self.session.execute(query)
        #     self.session.commit()
        # except Exception as e:
        #     logger.error(e)
        #     self.session.rollback()
        #     raise
        pass

    def upsert_research_area(self, batch: List[Dict[str, Any]]):
        # if not batch:
        #     return
        # try:
        #     unique_keys = [
        #         "major_knowledge_area",
        #         "knowledge_area",
        #         "sub_knowledge_area",
        #         "specialty",
        #         "researcher_id",
        #     ]
        #     batch = self.remove_duplicates(batch, unique_keys)
        #     batch = self.filter_existing_researchers(batch)
        #     if not batch:
        #         return
        #     query = insert(ResearchArea).values(batch)
        #     query = query.on_conflict_do_nothing(index_elements=unique_keys)
        #     self.session.execute(query)
        #     self.session.commit()
        # except Exception as e:
        #     logger.error(e)
        #     self.session.rollback()
        #     raise
        pass

    def upsert_knowledge_area(self, batch: List[Dict[str, Any]]):
        # if not batch:
        #     return
        # try:
        #     unique_keys = [
        #         "major_knowledge_area",
        #         "knowledge_area",
        #         "sub_knowledge_area",
        #         "specialty",
        #         "researcher_id",
        #     ]
        #     batch = self.remove_duplicates(batch, unique_keys)
        #     batch = self.filter_existing_researchers(batch)
        #     if not batch:
        #         return
        #     query = insert(KnowledgeArea).values(batch)
        #     query = query.on_conflict_do_nothing(index_elements=unique_keys)
        #     self.session.execute(query)
        #     self.session.commit()
        # except Exception as e:
        #     logger.error(e)
        #     self.session.rollback()
        #     raise
        pass

    def upsert_academic_background(self, batch: List[Dict[str, Any]]):
        # if not batch:
        #     return
        # try:
        #     unique_keys = [
        #         "type",
        #         "institution",
        #         "course",
        #         "start_year",
        #         "end_year",
        #         "researcher_id",
        #     ]
        #     batch = self.remove_duplicates(batch, unique_keys)
        #     batch = self.filter_existing_researchers(batch)
        #     if not batch:
        #         return
        #     query = insert(AcademicBackground).values(batch)
        #     query = query.on_conflict_do_nothing(index_elements=unique_keys)
        #     self.session.execute(query)
        #     self.session.commit()
        # except Exception as e:
        #     logger.error(e)
        #     self.session.rollback()
        #     raise
        pass
