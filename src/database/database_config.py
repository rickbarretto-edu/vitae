from dataclasses import dataclass
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session
from alembic import command
from alembic.config import Config

from src.settings import vitae

__all__ = ["database_config"]


@dataclass
class DatabaseConfig:
    engine: Engine = create_engine(vitae.postgres.url)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

    @property
    def session(self) -> Session:
        return self.session_factory()

    def migrate(self):
        command.upgrade(Config(vitae.paths.alembic), "head")


database_config = DatabaseConfig()
