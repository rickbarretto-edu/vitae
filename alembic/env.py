from logging.config import fileConfig
from alembic import context
from src.database.database_config import database_config   # Certifique-se de que database.py define `Base`
from src.models import *  # Importa todos os modelos dentro da pasta models

from src.models.academic_background import AcademicBackground
from src.models.knowledge_area import KnowledgeArea
from src.models.researcher import Researcher
from src.models.research_area import ResearchArea
from src.models.professional_experience import ProfessionalExperience

# Configuração do Alembic
config = context.config

# Configurar logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Definir os metadados para autogeração das migrações
target_metadata = database_config.base.metadata

def run_migrations_offline() -> None:
    """Executa as migrações no modo offline."""
    context.configure(
        url=database_config.url,
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
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
