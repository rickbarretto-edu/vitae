from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database_config import database_config

class ResearchArea(database_config.base):
    __tablename__ = "research_area"

    id = Column(Integer, primary_key=True, autoincrement=True)
    major_knowledge_area = Column(String, nullable=False)
    knowledge_area = Column(String, nullable=False)
    sub_knowledge_area = Column(String, nullable=True)
    specialty = Column(String, nullable=True)

    researcher_id = Column(Integer, ForeignKey("researcher.id"), nullable=False)
    researcher = relationship("Researcher", back_populates="research_area")