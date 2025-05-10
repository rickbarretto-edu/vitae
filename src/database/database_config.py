import os

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.utils.load_env import load_env


class DatabaseConfig:
    def __init__(self):
        self.url = self.postgres_url
        self.engine = create_engine(self.postgres_url)

        self.session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.base = declarative_base()

    def migrate(self):
        current_dir: str = os.path.dirname(__file__)
        ini_file: str = "../../alembic.ini"

        command.upgrade(Config(os.path.join(current_dir, ini_file)), "head")

    @property
    def postgres_url(self) -> str:
        """Postgres URL from .env file"""

        host = load_env.database_host
        port = load_env.database_port
        database = load_env.database_name

        user = load_env.database_user
        password = load_env.database_password

        return (
            f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
        )


database_config = DatabaseConfig()
