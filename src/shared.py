

from src.__setup__ import new_vitae
from src.infra.database import Database
from src.settings import VitaeSettings

vitae: VitaeSettings = new_vitae()
database = Database(vitae.postgres.engine)
