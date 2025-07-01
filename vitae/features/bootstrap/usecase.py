"""Use case for Boostrapping application."""

from dataclasses import dataclass
from pathlib import Path
import shutil

from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlmodel import SQLModel

from vitae.settings.vitae import Vitae


@dataclass
class DatabaseModelNotFound(Exception):
    path: str | None

    def __str__(self):
        return f"Tried to load from {self.path}"


@dataclass
class CouldNotResetDatabase(Exception):
    vitae: Vitae
    msg: str

    def __str__(self):
        postgres = self.vitae.postgres
        return f"Could not reset {postgres.db} by {postgres.user}. Reason: {self.msg}"


@dataclass
class Bootstrap:
    """Bootstrap Vitae, setting a new environment from scratch.

    This resets the database and log directory, be careful.
    """

    vitae: Vitae
    logs: Path = Path("logs")

    def existing(self) -> None:
        """Initialize Project from a running one.

        Instead of bootstrapping the system from scratch,
        this just loads everything needed to operate with
        an already running system.
        """
        self._load_db_models()

    def new(self) -> None:
        """Initialize Vitae Project from scratch."""
        self._load_db_models()
        self._reset_database()
        self._reset_logs()

    def _load_db_models(self) -> None:  # noqa: PLR6301
        """Load database model to Python's memory.

        Since SQLModel/Alchemy works by using metaclasses,
        this just needs to load all models to store it into database's metadata.

        Raises
        ------
        DatabaseModelNotFound

        """
        try:
            import vitae.infra.database.tables  # noqa: F401, PLC0415
        except ImportError as err:
            raise DatabaseModelNotFound(err.name) from err

    def _reset_database(self) -> None:
        """Create a new database from scratch.

        Raises
        ------
        CouldNotResetDatabase

        """
        engine = self.vitae.postgres.engine

        try:
            SQLModel.metadata.drop_all(engine)
            SQLModel.metadata.create_all(engine)
        except (OperationalError, SQLAlchemyError) as err:
            raise CouldNotResetDatabase(self.vitae, str(err)) from err

    def _reset_logs(self) -> None:
        """Reset the logs' directory."""
        shutil.rmtree(self.logs)
        self.logs.mkdir(parents=True, exist_ok=True)
