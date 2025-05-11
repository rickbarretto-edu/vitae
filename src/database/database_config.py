import os

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.utils.settings import VitaeSettings, vitae

__all__ = ["Model", "database_config"]

Model = declarative_base()

class DatabaseConfig:
    def __init__(self, vitae: VitaeSettings):
        self.engine = create_engine(vitae.postgres.url)

        self.session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def migrate(self):
        current_dir: str = os.path.dirname(__file__)
        ini_file: str = "../../alembic.ini"

        command.upgrade(Config(os.path.join(current_dir, ini_file)), "head")


database_config = DatabaseConfig(vitae)
