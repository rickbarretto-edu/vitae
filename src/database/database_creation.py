import psycopg
from psycopg.sql import SQL, Identifier

from src.settings import VitaeSettings


def new_database(vitae: VitaeSettings) -> None:
    """Creates a new database if it not exist.

    All database settings is read from ``.env`` file.

    Note
    ----
    By default the database will be called "vitae" if ``DATABASE_NAME`` is not defined.
    """

    database = vitae.postgres.db
    user = vitae.postgres.user

    with psycopg.connect(
        dbname="postgres",
        user=user.name,
        password=user.password,
        host=database.host,
        port=database.port,
        client_encoding="UTF-8",
        autocommit=True,
    ) as connection:
        with connection.cursor() as cursor:
            query = SQL("create database {}").format(Identifier(database.name))
            try:
                cursor.execute(query)
                print(f"{database.name} database was created!")
            except psycopg.Error as error:
                # When no serious error occur, this will report that the database already exist
                print(error)
