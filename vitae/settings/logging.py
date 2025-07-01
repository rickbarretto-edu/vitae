from pathlib import Path
import shutil
import sys

from loguru import logger


def erase_logs(path: Path) -> None:
    """Erase log directory."""
    shutil.rmtree(path)


def create_logs(path: Path) -> None:
    """Create log directory."""
    path.mkdir(parents=True, exist_ok=True)


def logging_into(log_file: Path) -> None:
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
