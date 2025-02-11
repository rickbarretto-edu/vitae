from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database_config import database_config

class ProfessionalExperience(database_config.base):
    __tablename__ = "professional_experience"

    id = Column(Integer, primary_key=True, autoincrement=True)
    institution = Column(String, nullable=False)
    employment_relationship = Column(String)
    start_year = Column(Integer)
    end_year = Column(Integer)
    researcher_id = Column(Integer, ForeignKey("researcher.id", ondelete="CASCADE"), nullable=False)

    researcher = relationship("Researcher", back_populates="professional_experience")
