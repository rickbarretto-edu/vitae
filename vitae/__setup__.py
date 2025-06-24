"""Setup the application settings.

The purpose of this module is to handle and abstract all the initialization
of the Application system, such as logging and database.

This module deals with external dependencies,
so the main module should be independent from them.
"""

from pathlib import Path
import shutil
import sys

from loguru import logger
from sqlmodel import SQLModel

from vitae.settings.vitae import Vitae

__all__ = [
    "new_vitae",
]


# =~=~=~ Logging related subroutines ~=~=~=


def erase_logs(path: Path) -> None:
    """Erase log directory."""
    shutil.rmtree(path)


def create_logs(path: Path) -> None:
    """Create log directory."""
    path.mkdir(parents=True, exist_ok=True)


def redirect_loguru_to(log_file: Path) -> None:
    """Redirect loguru's output to ``log_file``."""
    logger.remove()
    logger.add(
        str(log_file),
        rotation="200 MB",
        encoding="utf-8",
        enqueue=True,
    )


def enable_loguru_tracing() -> None:
    """Enable TRACE level.

    I highly recomend to use this for development environment only.
    """
    logger.add(sys.stdout, level="TRACE", colorize=True)


# =~=~=~ Database related subroutines ~=~=~=


def setup_database(vitae: Vitae) -> None:
    """Setups database."""
    # ``models`` module must be evaluated before create or drop it.
    # That is why this imports an unused variable inside this function.
    from vitae.infra.database import tables  # noqa: F401

    if vitae.in_development:
        # Since the dataset for development is far smaller than the production
        # and we run it multiple times to check everything before the ingestion,
        # was decided to rewrite the whole database instead.
        SQLModel.metadata.drop_all(vitae.postgres.engine)

    SQLModel.metadata.create_all(vitae.postgres.engine)


# =~=~=~ Public ~=~=~=


def new_vitae() -> Vitae:
    """Create a new vitae application.

    This function loads Vitae's settings and sets up the whole application,
    such as databases and logging systems.

    Returns
    -------
    New Vitae's Settings from ``vitae.toml``

    """
    vitae = Vitae.from_toml(Path("vitae.toml"))
    setup_vitae(vitae)
    return vitae


def setup_vitae(vitae: Vitae) -> None:
    """Setups Vitae's Logging and database."""
    logs = Path("logs")

    if vitae.in_development:
        # Since this will run multiple times, this is better to erase logs
        # to avoid unnecessary confusion with older logs.
        erase_logs(logs)

    create_logs(logs)
    redirect_loguru_to(logs / "vitae.log")

    setup_database(vitae)
