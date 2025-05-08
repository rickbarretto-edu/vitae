import os

from dotenv import load_dotenv


class LoadEnv:
    def __init__(self):
        load_dotenv()
        self.database_user = os.getenv("DATABASE_USER")
        self.database_password = os.getenv("DATABASE_PASSWORD")
        self.database_host = os.getenv("DATABASE_HOST")
        self.database_port = os.getenv("DATABASE_PORT")
        self.database_name = os.getenv("DATABASE_NAME")


load_env = LoadEnv()
