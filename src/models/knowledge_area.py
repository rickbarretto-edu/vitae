from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database_config import database_config

class KnowledgeArea(database_config.base):
    __tablename__ = "knowledge_area"

    id = Column(Integer, primary_key=True, autoincrement=True)
    major_knowledge_area = Column(String, nullable=False)
    knowledge_area = Column(String, nullable=False)
    sub_knowledge_area = Column(String, nullable=True)
    specialty = Column(String, nullable=True)

    academic_background_id = Column(Integer, ForeignKey("academic_background.id"), nullable=False)
    academic_background = relationship("AcademicBackground", back_populates="knowledge_area")