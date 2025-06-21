from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .researcher import Researcher


class ProfessionalExperience(SQLModel, table=True):
    __tablename__: str = "professional_experience"

    id: int | None = Field(default=None, primary_key=True)
    researcher_id: str = Field(foreign_key="researcher.id")
    researcher: "Researcher" = Relationship(
        back_populates="professional_experience",
    )

    institution: str = Field(nullable=False, index=True)
    employment_relationship: str | None = None
    start_year: int | None = None
    end_year: int | None = None
