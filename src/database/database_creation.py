import psycopg2
from psycopg2 import sql
from src.utils.load_env import load_env

class DatabaseCreation:
    def __init__(self):
        self.create_database()

    def create_database(self):
        try:
            conn = psycopg2.connect(dbname="postgres", user=load_env.database_user, password=load_env.database_password, 
                                    host=load_env.database_host, port=load_env.database_port)
            conn.autocommit = True  
            cursor = conn.cursor()

            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(load_env.database_name)))

            print(f"Banco de dados '{load_env.database_name}' criado com sucesso!")

            cursor.close()
            conn.close()

        except psycopg2.Error as e:
            print(f"Erro ao criar o banco de dados: {e}")

database_connection = DatabaseCreation()