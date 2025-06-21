from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .researcher import Researcher


class AcademicBackground(SQLModel, table=True):
    __tablename__: str = "academic_background"
    id: int | None = Field(default=None, primary_key=True)

    # Owner
    researcher_id: str = Field(foreign_key="researcher.id")
    researcher: "Researcher" = Relationship(
        back_populates="academic_background",
    )

    # Data
    type: str
    institution: str
    course: str | None = None
    start_year: int | None = None
    end_year: int | None = None

    knowledge_area: list["KnowledgeArea"] = Relationship(
        back_populates="academic_background",
    )


class KnowledgeArea(SQLModel, table=True):
    __tablename__: str = "knowledge_area"

    # Database Generated
    id: int | None = Field(default=None, primary_key=True)

    # Owner
    academic_background_id: int = Field(foreign_key="academic_background.id")
    academic_background: "AcademicBackground" = Relationship(
        back_populates="knowledge_area",
    )

    major_knowledge_area: str
    knowledge_area: str | None = None
    sub_knowledge_area: str | None = None
    specialty: str | None = None
