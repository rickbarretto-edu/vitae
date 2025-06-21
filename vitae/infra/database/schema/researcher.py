from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

__all__ = ["Researcher"]

if TYPE_CHECKING:
    from .academic import AcademicBackground
    from .professional import ProfessionalExperience


class Researcher(SQLModel, table=True):
    __tablename__: str = "researcher"

    id: str = Field(primary_key=True, nullable=False)

    name: str = Field(nullable=False, index=True)
    city: str | None = None
    state: str | None = None
    country: str | None = None
    quotes_names: str | None = None
    orcid: str | None = None
    abstract: str | None = None
    professional_institution: str | None = None
    institution_state: str | None = None
    institution_city: str | None = None

    professional_experience: list["ProfessionalExperience"] = Relationship(
        back_populates="researcher",
    )
    academic_background: list["AcademicBackground"] = Relationship(
        back_populates="researcher",
    )
    research_area: list["ResearchArea"] = Relationship(
        back_populates="researcher",
    )


class ResearchArea(SQLModel, table=True):
    __tablename__: str = "research_area"

    id: int | None = Field(default=None, primary_key=True)
    researcher_id: str = Field(foreign_key="researcher.id")
    researcher: "Researcher" = Relationship(
        back_populates="research_area",
    )

    major_knowledge_area: str | None = None
    knowledge_area: str | None = None
    sub_knowledge_area: str | None = None
    specialty: str | None = None
