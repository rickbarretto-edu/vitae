from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.utils.load_env import load_env
from alembic.config import Config
from alembic import command
import os

class DatabaseConfig:
    def __init__(self):
        self.url = f'postgresql+psycopg2://{load_env.database_user}:{load_env.database_password}@{load_env.database_host}:{load_env.database_port}/{load_env.database_name}'
        self.engine = create_engine(self.url)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.base = declarative_base()

    def run_migrations(self):
        alembic_config = Config(os.path.join(os.path.dirname(__file__), '../../alembic.ini'))
        command.upgrade(alembic_config, "head")

database_config = DatabaseConfig()