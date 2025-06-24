from vitae.__setup__ import new_vitae
from vitae.infra.database import Database
from vitae.settings import Vitae

vitae: Vitae = new_vitae()
database = Database(vitae.postgres.engine)
