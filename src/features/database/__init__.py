from dataclasses import dataclass

from sqlalchemy.engine import Engine

from .put import PutOperations


@dataclass
class Database:
    engine: Engine

    @property
    def put(self) -> PutOperations:
        return PutOperations(self.engine)