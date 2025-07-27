from dataclasses import dataclass

from sqlalchemy.engine import Engine
from sqlmodel import Session

from .put import PutOperations


@dataclass
class Database:
    engine: Engine

    @property
    def session(self) -> Session:
        """Return a new Database Session."""
        return Session(self.engine)

    @property
    def put(self) -> PutOperations:
        return PutOperations(self.engine)
