from sqlmodel import SQLModel, Field, Relationship


class Researcher(SQLModel, table=True):
    id: str = Field(primary_key=True, nullable=False)
    # updated_at: str | None = Field(
    #     default=None, sa_column_kwargs={"default": "now()", "onupdate": "now()"}
    # )
    name: str = Field(nullable=False, index=True)
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


class ProfessionalExperience(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    institution: str = Field(nullable=False, index=True)
    employment_relationship: str | None = None
    start_year: int | None = None
    end_year: int | None = None

    researcher_id: str = Field(foreign_key="researcher.id", nullable=False)

    # researcher: Researcher | None = Relationship(
    #     back_populates="professional_experience"
    # )
