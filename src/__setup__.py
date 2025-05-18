from dataclasses import dataclass
import os
import sys

import eliot
from loguru import logger

from src.settings import VitaeSettings


@dataclass
class VitaeSetup:
    vitae: VitaeSettings

    def setup_logging(self) -> None:
        self._eliot_for_development()
        self._loguru()

    def _eliot_for_development(self) -> None:
        """Setups Eliot for development mode.
        
        Eliot is very good for debugging when used with eliot-tree.
        But I don't think this is a good idea for using it 
        in production for my specific case, due to the amount of data.

        Note
        ----
        I'm not passing encoding="utf-8" because this was causing
        encoding errors even after processing the XML to be UTF-8.
        """
        if self.vitae.in_development:
            eliot.to_file(open("logs/eliot.log", "w+"))
            eliot.add_destinations(sys.stdout)
            logger.info("Eliot logging to file and stdout")
        else:
            logger.warning("Eliot disabled for production")

    def _loguru(self) -> None:
        """Setups Loguru
        
        - Writes logs to vitae.log with rotation of 200 MB.
        - Writes trace in stdout on development mode.
        - Writes exceptions to exceptions/ folder.
        """
        os.makedirs("logs", exist_ok=True)
        logger.add(
            "logs/vitae.log", rotation="200 MB", encoding="utf-8", enqueue=True
        )

        if self.vitae.in_development:
            logger.add(sys.stdout, level="TRACE", colorize=True)

        os.makedirs("logs/exceptions", exist_ok=True)

        def exception_filter(record):
            return record["exception"] is not None and record["level"].name in {
                "ERROR",
                "CRITICAL",
            }

        logger.add(
            "logs/exceptions/{{time:YYYY-MM-DD_HH-mm-ss}}_{{process}}_{{thread}}.log",
            level="ERROR",
            backtrace=True,
            diagnose=True,
            encoding="utf-8",
            enqueue=True,
            filter=exception_filter,
        )
