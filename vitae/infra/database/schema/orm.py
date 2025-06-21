import re
from typing import Any

from sqlmodel import Field, Relationship, SQLModel

__all__ = ["Orm", "foreign", "key", "link"]


def to_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


class TableNameMeta(type(SQLModel)):
    def __new__(cls, name, bases, namespace, **kwargs):
        if "__tablename__" not in namespace:
            namespace["__tablename__"] = to_snake(name)
        return super().__new__(cls, name, bases, namespace, **kwargs)


class Orm(SQLModel, metaclass=TableNameMeta):
    pass


def link(back: str) -> Any:
    return Relationship(back_populates=back)


def key() -> Any:
    return Field(default=None, primary_key=True)


def foreign(key: str) -> Any:
    return Field(foreign_key=key)
