import re
from typing import TYPE_CHECKING, Any

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .researcher import Researcher


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


class AcademicBackground(Orm, table=True):
    id: int | None = key()
    researcher_id: str = foreign("researcher.id")
    researcher: "Researcher" = link("academic_background")

    type: str
    institution: str
    course: str | None = None
    start_year: int | None = None
    end_year: int | None = None

    knowledge_area: list["KnowledgeArea"] = link("academic_background")


class KnowledgeArea(Orm, table=True):
    id: int | None = key()
    academic_background_id: int = foreign("academic_background.id")
    academic_background: "AcademicBackground" = link("knowledge_area")

    major_knowledge_area: str
    knowledge_area: str | None = None
    sub_knowledge_area: str | None = None
    specialty: str | None = None
