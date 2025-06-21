

from vitae.__setup__ import new_vitae
from vitae.infra.database import Database
from vitae.settings import VitaeSettings

vitae: VitaeSettings = new_vitae()
database = Database(vitae.postgres.engine)
