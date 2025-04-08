from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.utils.load_env import load_env

class DatabaseConfig:
    def __init__(self):
        self.url = f'postgresql+psycopg2://{load_env.database_user}:{load_env.database_password}@{load_env.database_host}:{load_env.database_port}/{load_env.database_name}'
        self.engine = create_engine(self.url)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.base = declarative_base()

database_config = DatabaseConfig()