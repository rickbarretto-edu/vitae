from dataclasses import dataclass
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.utils.settings import vitae

__all__ = ["Model", "database_config"]

Model = declarative_base()


@dataclass
class DatabaseConfig:
    engine: Engine = create_engine(vitae.postgres.url)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def migrate(self):
        command.upgrade(Config(vitae.paths.alembic), "head")


database_config = DatabaseConfig()
