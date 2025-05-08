from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from src.database.database_config import database_config


class Researcher(database_config.base):
    __tablename__ = "researcher"

    id = Column(Integer, primary_key=True, autoincrement=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    name = Column(String, nullable=False)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    quotes_names = Column(String)
    orcid = Column(String)
    abstract = Column(String)
    professional_institution = Column(String)
    institution_state = Column(String)
    institution_city = Column(String)

    academic_background = relationship(
        "AcademicBackground",
        back_populates="researcher",
        cascade="all, delete-orphan",
    )
    professional_experience = relationship(
        "ProfessionalExperience",
        back_populates="researcher",
        cascade="all, delete-orphan",
    )
    research_area = relationship(
        "ResearchArea",
        back_populates="researcher",
        cascade="all, delete-orphan",
    )
