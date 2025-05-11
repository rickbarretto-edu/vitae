from dataclasses import dataclass
import os

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
    session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    def migrate(self):
        current_dir: str = os.path.dirname(__file__)
        ini_file: str = "../../alembic.ini"

        command.upgrade(Config(os.path.join(current_dir, ini_file)), "head")


database_config = DatabaseConfig()
