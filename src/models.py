from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint


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
    professional_institution: str | None = None
    institution_state: str | None = None
    institution_city: str | None = None

    academic_background: list["AcademicBackground"] = Relationship(
        back_populates="researcher",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    professional_experience: list["ProfessionalExperience"] = Relationship(
        back_populates="researcher",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    research_area: list["ResearchArea"] = Relationship(
        back_populates="researcher",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class ProfessionalExperience(SQLModel, table=True):
    __tablename__: str = "professional_experience"

    id: int | None = Field(default=None, primary_key=True)
    institution: str = Field(nullable=False, index=True)
    employment_relationship: str | None = None
    start_year: int | None = None
    end_year: int | None = None

    researcher_id: str = Field(foreign_key="researcher.id", nullable=False)
    researcher: Researcher | None = Relationship(
        back_populates="professional_experience",
    )


class AcademicBackground(SQLModel, table=True):
    __tablename__: str = "academic_background"

    id: int | None = Field(default=None, primary_key=True)
    type: str
    institution: str
    course: str | None = None
    start_year: int | None = None
    end_year: int | None = None
    researcher_id: str = Field(foreign_key="researcher.id")

    researcher: "Researcher" = Relationship(
        back_populates="academic_background",
    )
    knowledge_area: list["KnowledgeArea"] = Relationship(
        back_populates="academic_background",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    __table_args__ = (
        UniqueConstraint(
            "type",
            "institution",
            "course",
            "start_year",
            "end_year",
            "researcher_id",
            name="unique_academic_background",
        ),
    )


class KnowledgeArea(SQLModel, table=True):
    __tablename__: str = "knowledge_area"

    id: int | None = Field(default=None, primary_key=True)
    major_knowledge_area: str
    knowledge_area: str | None = None
    sub_knowledge_area: str | None = None
    specialty: str | None = None
    academic_background_id: int = Field(foreign_key="academic_background.id")

    academic_background: "AcademicBackground" = Relationship(
        back_populates="knowledge_area",
    )

    __table_args__ = (
        UniqueConstraint(
            "major_knowledge_area",
            "knowledge_area",
            "sub_knowledge_area",
            "specialty",
            "academic_background_id",
            name="unique_knowledge_area",
        ),
    )


class ResearchArea(SQLModel, table=True):
    __tablename__: str = "research_area"

    id: int | None = Field(default=None, primary_key=True)
    major_knowledge_area: str
    knowledge_area: str | None = None
    sub_knowledge_area: str | None = None
    specialty: str | None = None
    researcher_id: str = Field(foreign_key="researcher.id")

    researcher: "Researcher" = Relationship(back_populates="research_area")

    __table_args__ = (
        UniqueConstraint(
            "major_knowledge_area",
            "knowledge_area",
            "sub_knowledge_area",
            "specialty",
            "researcher_id",
            name="unique_research_area",
        ),
    )
