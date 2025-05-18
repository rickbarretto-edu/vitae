from dataclasses import dataclass

from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from src.settings import vitae

__all__ = ["database_config"]


@dataclass
class DatabaseConfig:
    engine: Engine = create_engine(vitae.postgres.url)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def migrate(self):
        command.upgrade(Config(vitae.paths.alembic), "head")


database_config = DatabaseConfig()
