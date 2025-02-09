import psycopg2
from psycopg2 import sql
from app.utils.loadEnv import loadEnv

class DatabaseCreation:
    def __init__(self):
        self.createDataBase()

    def createDataBase(self):
        try:
            conn = psycopg2.connect(dbname="postgres", user=loadEnv.DatabaseUser, password=loadEnv.DatabasePassword, 
                                    host=loadEnv.DatabaseHost, port=loadEnv.DatabasePort)
            conn.autocommit = True  
            cursor = conn.cursor()

            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(loadEnv.DatabaseName)))

            print(f"Banco de dados '{loadEnv.DatabaseName}' criado com sucesso!")

            cursor.close()
            conn.close()

        except psycopg2.Error as e:
            print(f"Erro ao criar o banco de dados: {e}")

databaseConnection = DatabaseCreation()