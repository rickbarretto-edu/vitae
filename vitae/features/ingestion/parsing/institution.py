from vitae.features.ingestion.adapters import Institution

from . import _xml as xml

__all__ = ["institution"]


def institution(education_or_experience: xml.Node, extra_data: xml.Node) -> Institution:
    lattes_id: str = education_or_experience["codigo instituicao"] or ""
    found: xml.Node = xml.Node(None)

    for inst in extra_data.all("informacao adicional instituicao"):
        if inst["codigo instituicao"] == lattes_id:
            found = inst
            break

    return Institution(
        lattes_id=lattes_id,
        name=education_or_experience["nome instituicao"],
        country=found["nome pais instituicao"],
        state=found["sigla uf instituicao"],
        abbr=found["sigla instituicao"],
    )
