from collections.abc import Iterable
from dataclasses import dataclass
import itertools

from src.features.ingestion.schema import Curriculum
from src.infra.database import Database


@dataclass
class Researchers:
    db: Database
    every: int = 50

    def put(self, researchers: Iterable[Curriculum]) -> None:
        for group in itertools.batched(researchers, self.every):
            for researcher in group:
                self.db.put.each(
                    researcher.personal_data,
                    researcher.professional_experiences,
                    researcher.academic_background,
                    researcher.research_areas,
                )
