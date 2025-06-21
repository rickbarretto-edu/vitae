from sqlmodel import SQLModel

from .academic import AcademicBackground, KnowledgeArea
from .professional import ProfessionalExperience
from .researcher import ResearchArea, Researcher

__all__ = [
    "AcademicBackground",
    "KnowledgeArea",
    "ProfessionalExperience",
    "ResearchArea",
    "Researcher",
    "SQLModel",
]
