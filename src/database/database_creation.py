import psycopg
from psycopg import Connection
from psycopg.sql import SQL, Identifier

from src.utils.load_env import load_env


def new_database() -> None:
    connection: Connection = psycopg.connect(
        dbname="postgres",
        user=load_env.database_user,
        password=load_env.database_password,
        host=load_env.database_host,
        port=load_env.database_port,
        client_encoding="UTF-8",
        autocommit=True,
    )

    with connection.cursor() as cursor:
        query = SQL("create database {}").format(
            Identifier(load_env.database_name or "vitae")
        )
        try:
            cursor.execute(query)
            print(
                f"Banco de dados {load_env.database_name} criado com sucesso!"
            )
        except psycopg.Error as error:
            # When no serious error occur, this will report that the database already exist
            print(error)

    connection.close()
