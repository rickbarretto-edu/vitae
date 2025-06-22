"""Adapters are Parsers' Schemas that converts itself to Database Schemas.

The property used for this auto-convertion is `as_table`.
Internal schemas may implement this as a method because this is needed
parent data to complete the Table.
"""

from .academic import Education, StudyField
from .institution import Institution
from .professional import Address, Experience
from .researcher import Expertise, Nationality, Researcher

__all__ = [
    "Address",
    "Education",
    "Experience",
    "Expertise",
    "Institution",
    "Nationality",
    "Researcher",
    "StudyField",
]
