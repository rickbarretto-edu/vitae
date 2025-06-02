from dataclasses import dataclass
from pathlib import Path
import shutil
import sys

import eliot
from loguru import logger

from src.settings import VitaeSettings

__all__ = [
    "VitaeSetup",
]


def erase_logs(path: Path) -> None:
    """Erase log directory."""
    shutil.rmtree(path)


def create_logs(path: Path) -> None:
    """Create log directory."""
    path.mkdir(parents=True, exist_ok=True)


def redirect_eliot_to(log_file: Path) -> None:
    with log_file.open("w+", encoding="utf-8") as f:
        eliot.to_file(f)


def redirect_loguru_to(log_file: Path) -> None:
    logger.remove()
    logger.add(
        str(log_file),
        rotation="200 MB",
        encoding="utf-8",
        enqueue=True,
    )


def enable_loguru_tracing() -> None:
    logger.add(sys.stdout, level="TRACE", colorize=True)


@dataclass
class VitaeSetup:
    """Setup for the project."""

    vitae: VitaeSettings

    def setup_logging(self) -> None:
        """Setups logging settings."""
        logs = Path("logs")

        if self.vitae.in_development:
            erase_logs(logs)

        create_logs(logs)

        if self.vitae.in_development:
            redirect_eliot_to(logs / "eliot.log")
            logger.info("Eliot enabled to file.")

        redirect_loguru_to(logs / "vitae.log")
