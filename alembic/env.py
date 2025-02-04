import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Importar a configuração do banco e os modelos
from database import Base  # Certifique-se de que database.py define `Base`
from models import *  # Importa todos os modelos dentro da pasta models

# Configuração do Alembic
config = context.config

# Configurar logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Definir os metadados para autogeração das migrações
target_metadata = Base.metadata

# Obter a URL do banco da variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("A variável de ambiente DATABASE_URL não está definida!")

def run_migrations_offline() -> None:
    """Executa as migrações no modo offline."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa as migrações no modo online."""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
