from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.utils.loadEnv import loadEnv

class DatabaseConfig:
    def __init__(self):
        self.engine = create_engine(f'postgresql+psycopg2://{loadEnv.DatabaseUser}:{loadEnv.DatabasePassword}@{loadEnv.DatabaseHost}:{loadEnv.DatabasePort}/{loadEnv.DatabaseName}')
        self.sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.base = declarative_base()

databaseConfig = DatabaseConfig()