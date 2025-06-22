import re
from typing import Any

from sqlmodel import Field, Relationship, SQLModel

__all__ = ["Orm", "foreign", "index", "key", "link", "required_key"]


def to_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


class TableNameMeta(type(SQLModel)):
    def __new__(cls, name, bases, namespace, **kwargs):  # noqa: ANN001, ANN003, ANN204
        if "__tablename__" not in namespace:
            namespace["__tablename__"] = to_snake(name)
        return super().__new__(cls, name, bases, namespace, **kwargs)


class Orm(SQLModel, metaclass=TableNameMeta):  # noqa: D101
    pass


def link(back: str) -> Any:
    return Relationship(back_populates=back)


def key(**kargs) -> Any:
    return Field(default=None, primary_key=True, **kargs)


def required_key() -> Any:
    return Field(primary_key=True, nullable=False)


def foreign(key: str, **kargs) -> Any:
    return Field(foreign_key=key, **kargs)


def index() -> Any:
    return Field(nullable=False, index=True)
