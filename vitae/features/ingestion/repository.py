"""Repository pattern for the Ingestion feature."""

from collections.abc import Iterable
from dataclasses import dataclass
import itertools
from pathlib import Path
from typing import TYPE_CHECKING

import loguru

from vitae.features.ingestion.adapters import Curriculum
from vitae.infra.database import Database, transactions

if TYPE_CHECKING:
    from vitae.features.ingestion.adapters.academic import Education
    from vitae.features.ingestion.adapters.institution import Institution
    from vitae.features.ingestion.adapters.professional import Experience
    from vitae.features.ingestion.adapters.researcher import Researcher


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
        researchers: Iterable[Researcher] = (cv.researcher for cv in batch)
        education: Iterable[Education] = flatten(cv.education for cv in batch)
        experience_batch: Iterable[Experience] = flatten(
            cv.experience for cv in batch
        )
        institutions: Iterable[Institution] = flatten(
            cv.all_institutions for cv in batch
        )

        return self.db.put.batch_transaction(
            transactions.Curricula(
                researchers=transactions.Researchers(
                    researchers=(r.as_table for r in researchers),
                    nationality=(r.nationality_table for r in researchers),
                    expertise=flatten(r.expertise_tables for r in researchers),
                ),
                academic=transactions.Academic(
                    education=(edu.as_table for edu in education),
                    fields=flatten(edu.fields_as_table for edu in education),
                ),
                professional=transactions.Experience(
                    experience=(xp.as_table for xp in experience_batch),
                    address=(cv.address for cv in batch),
                ),
                institutions=(inst.as_table for inst in institutions),
            ),
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
        return self.db.put.batch_transaction(
            transactions.Curricula(
                researchers=transactions.Researchers(
                    researchers=[cv.researcher.as_table],
                    nationality=[cv.researcher.nationality_table],
                    expertise=cv.researcher.expertise_tables,
                ),
                academic=transactions.Academic(
                    education=(edu.as_table for edu in cv.education),
                    fields=flatten(edu.fields_as_table for edu in cv.education),
                ),
                professional=transactions.Experience(
                    experience=(xp.as_table for xp in cv.experience),
                    address=[cv.address],
                ),
                institutions=(inst.as_table for inst in cv.all_institutions),
            ),
        )
