import re
from typing import TYPE_CHECKING

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


class AcademicBackground(Orm, table=True):
    id: int | None = Field(default=None, primary_key=True)
    researcher_id: str = Field(foreign_key="researcher.id")
    researcher: "Researcher" = Relationship(
        back_populates="academic_background",
    )

    type: str
    institution: str
    course: str | None = None
    start_year: int | None = None
    end_year: int | None = None

    knowledge_area: list["KnowledgeArea"] = Relationship(
        back_populates="academic_background",
    )


class KnowledgeArea(Orm, table=True):
    id: int | None = Field(default=None, primary_key=True)
    academic_background_id: int = Field(foreign_key="academic_background.id")
    academic_background: "AcademicBackground" = Relationship(
        back_populates="knowledge_area",
    )

    major_knowledge_area: str
    knowledge_area: str | None = None
    sub_knowledge_area: str | None = None
    specialty: str | None = None
