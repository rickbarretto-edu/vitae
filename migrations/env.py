from logging.config import fileConfig

from alembic import context


from src.database.database_config import database_config
from src.models.__core__ import Model
from src.models import *
from src.models.academic_background import AcademicBackground
from src.models.knowledge_area import KnowledgeArea
from src.models.professional_experience import ProfessionalExperience
from src.models.research_area import ResearchArea
from src.models.researcher import Researcher
from src.settings import vitae

# Configuração do Alembic
config = context.config

# Configurar logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Definir os metadados para autogeração das migrações
target_metadata = Model.metadata


def run_migrations_offline() -> None:
    """Executa as migrações no modo offline."""
    context.configure(
        url=vitae.postgres.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa as migrações no modo online."""
    connectable = database_config.engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
