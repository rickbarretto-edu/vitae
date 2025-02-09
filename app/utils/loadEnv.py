import os
from dotenv import load_dotenv

class LoadEnv:
    def __init__(self):
        load_dotenv()
        self.DatabaseUser = os.getenv("DATABASE_USER")
        self.DatabasePassword = os.getenv("DATABASE_PASSWORD")
        self.DatabaseHost = os.getenv("DATABASE_HOST")
        self.DatabasePort = os.getenv("DATABASE_PORT")
        self.DatabaseName = os.getenv("DATABASE_NAME")

loadEnv = LoadEnv()