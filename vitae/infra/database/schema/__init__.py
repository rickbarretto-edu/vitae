from sqlmodel import SQLModel

from .academic import AcademicBackground, KnowledgeArea
from .professional import ProfessionalExperience
from .researcher import Expertise, Nationality, Researcher

__all__ = [
    "AcademicBackground",
    "Expertise",
    "KnowledgeArea",
    "Nationality",
    "ProfessionalExperience",
    "Researcher",
    "SQLModel",
]
