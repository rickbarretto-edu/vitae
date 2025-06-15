from abc import ABC, abstractmethod
from functools import cached_property


class Entity[Key](ABC):
    id: Key


class Repository[Entity](ABC):
    pass
