"""Repository pattern for the Ingestion feature."""

from collections.abc import Iterable
from dataclasses import dataclass
import itertools
from pathlib import Path

import loguru

from vitae.features.ingestion.adapters import Curriculum
from vitae.infra.database import Database
from vitae.infra.database.transactions import bulk


def flatten[T](xs: Iterable[Iterable[T]]) -> Iterable[T]:
    """Unnest nested iterable.

    Returns
    -------
    A flatten Iterable.

    """
    return itertools.chain(*xs)


def existent[T](xs: Iterable[T | None]) -> list[T]:
    return [x for x in xs if x is not None]


def log_with(into: Path, logger, logfile: str, level: str) -> None:  # noqa: ANN001
    """Create logs handlers with strict level policy.

    This allow us to redirect each kind of logging to the right file,
    and at the same time not mixing levels in those files.
    """
    file = into / f"ingestion/{logfile}.log"

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
    log_directory: Path
    every: int = 50

    def __post_init__(self) -> None:
        """Setups logging.

        There are three levels of logging:
        - INFO: logs stored data.
        - WARN: logs rolledback groups.
        - ERROR: logs failed individual commits.
        """
        self.log = loguru.logger
        log_with(self.log_directory, self.log, "processed", "INFO")
        log_with(self.log_directory, self.log, "rolledback-group", "WARNING")
        log_with(self.log_directory, self.log, "failed", "ERROR")

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
        curricula = list(batch)

        researchers = bulk.Researchers(
            researchers=[cv.researcher.as_table for cv in curricula],
            nationality=[cv.researcher.nationality_table for cv in curricula],
            expertise=flatten(
                [cv.researcher.expertise_tables for cv in curricula],
            ),
        )

        academic = bulk.Academic(
            education=(
                edu.as_table
                for edu in flatten([cv.education for cv in curricula])
            ),
            fields=flatten(
                edu.fields_as_table
                for edu in flatten([cv.education for cv in curricula])
            ),
            advisoring=existent(
                [
                    edu.advisor_as_table
                    for edu in flatten([cv.education for cv in curricula])
                ],
            ),
        )

        professional = bulk.Professional(
            experience=(
                xp.as_table
                for xp in flatten([cv.experience for cv in curricula])
            ),
            address=[
                cv.address.as_table
                for cv in curricula
                if cv.address is not None
            ],
        )

        institutions = [
            inst.as_table
            for inst in flatten(list(cv.all_institutions) for cv in curricula)
            if inst.lattes_id is not None
        ]

        return self.db.put.batch_transaction(
            bulk.Institutions(institutions),
            bulk.Curricula(
                researchers=researchers,
                academic=academic,
                professional=professional,
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
        researchers = bulk.Researchers(
            researchers=[cv.researcher.as_table],
            nationality=[cv.researcher.nationality_table],
            expertise=cv.researcher.expertise_tables,
        )

        academic = bulk.Academic(
            education=(edu.as_table for edu in cv.education),
            fields=flatten(edu.fields_as_table for edu in cv.education),
        )

        professional = bulk.Experience(
            experience=(xp.as_table for xp in cv.experience),
            address=[cv.address],
        )

        return self.db.put.batch_transaction(
            institutions=bulk.Institutions(
                inst.as_table for inst in cv.all_institutions
            ),
            curricula=bulk.Curricula(
                researchers=researchers,
                academic=academic,
                professional=professional,
            ),
        )
