"""Conversion functions from parsed to Model."""

from src.infra.database import models as infra

from . import schema as parsed

__all__ = [
    "academic_background_from",
    "professional_experience_from",
    "research_area_from",
    "researcher_from",
]


def researcher_from(data: parsed.GeneralData) -> infra.Researcher:  # noqa: D103
    return infra.Researcher(
        id=data["id"],
        name=data["name"] or "Invalid Name",
        city=data["city"],
        state=data["state"],
        country=data["country"],
        quotes_names=data["quotes_names"],
        orcid=data["orcid"],
        abstract=data["abstract"],
        professional_institution=data["professional_institution"],
        institution_state=data["institution_state"],
        institution_city=data["institution_city"],
    )


def academic_background_from(  # noqa: D103
    data: parsed.AcademicBackground,
) -> infra.AcademicBackground:
    return infra.AcademicBackground(
        researcher_id=data["researcher_id"],
        type=data["type"] or "Unknown Type",
        institution=data["institution"] or "Unknown Institution",
        course=data["course"],
        start_year=data["start_year"],
        end_year=data["end_year"],
    )


def professional_experience_from(  # noqa: D103
    data: parsed.ProfessionalExperience,
) -> infra.ProfessionalExperience:
    return infra.ProfessionalExperience(
        researcher_id=data["researcher_id"],
        institution=data["institution"] or "Unknown Institution",
        employment_relationship=data["employment_relationship"]
        or "Unknown Relationship",
        start_year=data["start_year"] or 0,
        end_year=data["end_year"] or 0,
    )


def research_area_from(data: parsed.ResearchArea) -> infra.ResearchArea:  # noqa: D103
    return infra.ResearchArea(
        researcher_id=data["researcher_id"],
        major_knowledge_area=data["major_knowledge_area"]
        or "Unknown Major Area",
        knowledge_area=data["knowledge_area"],
        sub_knowledge_area=data["sub_knowledge_area"],
        specialty=data["specialty"],
    )
