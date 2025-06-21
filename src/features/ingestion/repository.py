from collections.abc import Iterable
from dataclasses import dataclass
import itertools
from pathlib import Path

import loguru

from src.core import Repository
from src.features.ingestion.domain import Curriculum
from src.infra.database import Database

flatten = itertools.chain


def log_with[T](logger: loguru.Logger, logfile: str, level: str) -> None:
    """Create logs handlers with strict level policy.

    This allow us to redirect each kind of logging to the right file,
    and at the same time not mixing levels in those files.
    """
    file = Path(f"logs/ingestion/{logfile}.log")

    def restrict_level(record):
        return record["level"].name == level

    logger.add(
        file,
        format="{message}",
        level=level,
        filter=restrict_level,
        enqueue=True,
    )


@dataclass
class Researchers(Repository[Curriculum]):
    db: Database
    every: int = 50

    def __post_init__(self) -> None:
        """Setups logging.

        There are three levels of logging:
        - INFO: logs stored data.
        - WARN: logs rolledback groups.
        - ERROR: logs failed individual commits.
        """
        self.log = loguru.logger
        log_with(self.log, "processed", "INFO")
        log_with(self.log, "rolledback-group", "WARNING")
        log_with(self.log, "failed", "ERROR")

    def put(self, researchers: Iterable[Curriculum]) -> None:
        """Put Researchers on database.

        This function tries to store them in batch each `every` researcher.
        When this is not possible to put them at once, this will rollback and
        try to put one by one, to log the defected one.
        """
        for group in itertools.batched(researchers, self.every):
            if not self._put_all(group):
                self.log.warning(
                    ",".join([r.id for r in group]),
                )
                self._put_each_from(group)
            else:
                for researcher in group:
                    self.log.info(researcher.id)

    def _put_all(self, group: Iterable[Curriculum]) -> bool:
        """Put all Researchers at once on database.

        Returns
        -------
        If all researchers were sucessfully stored.

        """
        personal = (r.personal_data for r in group)
        experiences = (r.professional_experiences for r in group)
        background = (r.academic_background for r in group)
        areas = (r.research_areas for r in group)

        return self.db.put.researcher(
            researcher=personal,
            experience=flatten(*experiences),
            background=flatten(*background),
            area=flatten(*areas),
        )

    def _put_each_from(self, group: Iterable[Curriculum]) -> None:
        """Put Researchers one by one on database."""
        for researcher in group:
            if self._put_single(researcher):
                self.log.info(researcher.id)
            else:
                self.log.error(researcher.id)

    def _put_single(self, researcher: Curriculum) -> bool:
        """Put a single Researcher on database.

        Returns
        -------
        If the researcher was sucessfully stored.

        """
        return self.db.put.researcher(
            researcher=researcher.personal_data,
            experience=researcher.professional_experiences,
            background=researcher.academic_background,
            area=researcher.research_areas,
        )
