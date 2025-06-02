from pathlib import Path
import shutil
import sys

import eliot
from loguru import logger

from src.settings import VitaeSettings

__all__ = [
    "setup_vitae",
]


def erase_logs(path: Path) -> None:
    """Erase log directory."""
    shutil.rmtree(path)


def create_logs(path: Path) -> None:
    """Create log directory."""
    path.mkdir(parents=True, exist_ok=True)


def redirect_eliot_to(log_file: Path) -> None:
    """Redirect eliot's output to ``log_file``."""
    with log_file.open("w+", encoding="utf-8") as f:
        eliot.to_file(f)


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


def setup_vitae(vitae: VitaeSettings) -> None:
    LOGS = Path("logs")

    if vitae.in_development:
        # Since this will run multiple times, this is better to erase logs
        # to avoid unnecessary confusion with older logs.
        erase_logs(LOGS)

    create_logs(LOGS)

    if vitae.in_development:
        # Eliot is only used for development pupose to traceback actions
        # This should not be used in production, since this will produce huge
        # log files that will never be read.
        redirect_eliot_to(LOGS / "eliot.log")
        logger.info("Eliot enabled to file.")

    redirect_loguru_to(LOGS / "vitae.log")
