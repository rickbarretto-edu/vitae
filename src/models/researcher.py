from sqlmodel import SQLModel, Field, Relationship

from src.models.academic_background import AcademicBackground
from src.models.professional_experience import ProfessionalExperience
from src.models.research_area import ResearchArea


__all__ = ["Researcher"]


class Researcher(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # updated_at: str | None = Field(
    #     default=None, sa_column_kwargs={"default": "now()", "onupdate": "now()"}
    # )
    name: str = Field(nullable=False)
    city: str | None = None
    state: str | None = None
    country: str | None = None
    quotes_names: str | None = None
    orcid: str | None = None
    abstract: str | None = None
    # professional_institution: str | None = None
    # institution_state: str | None = None
    # institution_city: str | None = None

    # academic_background: list[AcademicBackground] = Relationship(
    #     back_populates="researcher",
    #     sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    # )
    # professional_experience: list[ProfessionalExperience] = Relationship(
    #     back_populates="researcher",
    #     sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    # )
    # research_area: list[ResearchArea] = Relationship(
    #     back_populates="researcher",
    #     sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    # )
