import psycopg2
from psycopg2 import sql
from utils.loadEnv import *

try:
    conn = psycopg2.connect(dbname="postgres", user=DATABASE_USER, password=DATABASE_PASSWORD, 
                            host=DATABASE_HOST, port=DATABASE_PORT)
    conn.autocommit = True  
    cursor = conn.cursor()

    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DATABASE_NAME)))

    print(f"Banco de dados '{DATABASE_NAME}' criado com sucesso!")

    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print(f"Erro ao criar o banco de dados: {e}")