"""Repository pattern for the Ingestion feature."""

from collections.abc import Iterable
from dataclasses import dataclass
import itertools
from pathlib import Path

import loguru

from vitae.features.ingestion.adapters import Curriculum
from vitae.infra.database import Database, bulk_transactions


def flatten[T](xs: Iterable[Iterable[T]]) -> Iterable[T]:
    """Unnest nested iterable.

    Returns
    -------
    A flatten Iterable.

    """
    return itertools.chain(*xs)


def log_with(logger, logfile: str, level: str) -> None:  # noqa: ANN001
    """Create logs handlers with strict level policy.

    This allow us to redirect each kind of logging to the right file,
    and at the same time not mixing levels in those files.
    """
    file = Path(f"logs/ingestion/{logfile}.log")

    def restrict_level(record) -> bool:  # noqa: ANN001
        """Create a level strict filter.

        Returns
        -------
        If the record has the same level as defined by the outter function.

        """
        return record["level"].name == level

    logger.add(
        file,
        format="{message}",
        level=level,
        filter=restrict_level,
        enqueue=True,
    )


@dataclass
class Researchers:
    """Researcher's Curriculum Repository."""

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
            if self._try_put_at_once(group):
                self._log_success(group)
            else:
                self._re_insert(group)

    def _log_success(self, batch: Iterable[Curriculum]) -> None:
        for curriculum in batch:
            self.log.info(curriculum.id)

    def _re_insert(self, batch: Iterable[Curriculum]) -> None:
        self._log_fail(batch)
        self._put_each_from(batch)

    def _log_fail(self, batch: Iterable[Curriculum]) -> None:
        ids_to_log: str = ",".join(curriculum.id for curriculum in batch)
        self.log.warning(ids_to_log)

    def _try_put_at_once(self, batch: Iterable[Curriculum]) -> bool:
        """Put all Researchers at once on database.

        Returns
        -------
        If all researchers were sucessfully stored.

        """
        # Prepare lists from the batch for each entity type
        curricula = list(batch)
        researchers = [cv.researcher for cv in curricula]
        education = list(flatten(cv.education for cv in curricula))
        experiences = list(flatten(cv.experience for cv in curricula))
        institutions = list(
            flatten(list(cv.all_institutions) for cv in curricula),
        )

        researcher_tables = [re.as_table for re in researchers]
        nationality_tables = [re.nationality_table for re in researchers]
        expertise_tables = list(
            flatten(re.expertise_tables for re in researchers),
        )
        education_tables = [edu.as_table for edu in education]
        field_tables = list(flatten(edu.fields_as_table for edu in education))
        experience_tables = [xp.as_table for xp in experiences]
        address_tables = [cv.address.as_table for cv in curricula]
        institution_tables = [
            inst.as_table for inst in institutions if inst.lattes_id is not None
        ]

        ct = bulk_transactions.Curricula(
            researchers=bulk_transactions.Researchers(
                researchers=researcher_tables,
                nationality=nationality_tables,
                expertise=expertise_tables,
            ),
            academic=bulk_transactions.Academic(
                education=education_tables,
                fields=field_tables,
            ),
            professional=bulk_transactions.Professional(
                experience=experience_tables,
                address=address_tables,
            ),
        )

        return self.db.put.batch_transaction(
            bulk_transactions.Institutions(institution_tables),
            ct,
        )

    def _put_each_from(self, group: Iterable[Curriculum]) -> None:
        """Put Researchers one by one on database."""
        for researcher in group:
            if self._put_single(researcher):
                self.log.info(researcher.id)
            else:
                self.log.error(researcher.id)

    def _put_single(self, cv: Curriculum) -> bool:
        """Put a single Researcher on database.

        Returns
        -------
        If the researcher was sucessfully stored.

        """
        ct = bulk_transactions.Curricula(
            researchers=bulk_transactions.Researchers(
                researchers=[cv.researcher.as_table],
                nationality=[cv.researcher.nationality_table],
                expertise=cv.researcher.expertise_tables,
            ),
            academic=bulk_transactions.Academic(
                education=(edu.as_table for edu in cv.education),
                fields=flatten(edu.fields_as_table for edu in cv.education),
            ),
            professional=bulk_transactions.Experience(
                experience=(xp.as_table for xp in cv.experience),
                address=[cv.address],
            ),
        )
        return self.db.put.batch_transaction(
            bulk_transactions.Institutions(
                inst.as_table for inst in cv.all_institutions
            ),
            ct,
        )
