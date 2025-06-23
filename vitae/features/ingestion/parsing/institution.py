"""Institution related parsing."""

from __future__ import annotations

from vitae.features.ingestion.adapters import Institution

from . import _xml as xml

__all__ = ["institution_from_xml"]


def institution_from_xml(
    institution_id: str | None,
    institution_name: str | None,
    data: xml.Node,
) -> Institution:
    """Extract Institution from XML.

    Notice that we need to pass its ID and name,
    and this function will fetch any aditional information.

    Returns
    -------
    Institution from XML.

    """
    default_value = Institution(
        lattes_id=institution_id,
        name=institution_name,
        country=None,
        state=None,
        abbr=None,
    )

    found: xml.Node = xml.Node(None)

    if not (extra := data.first("dados complementares")).exists:
        return default_value

    if not (
        institutions := extra.first("informacoes adicionais instituicoes")
    ).exists:
        return default_value

    for inst in institutions.all("informacao adicional instituicao"):
        if inst["codigo instituicao"] == institution_id:
            found = inst
            break
    else:
        return default_value

    return Institution(
        lattes_id=institution_id,
        name=institution_name,
        country=found["nome pais instituicao"],
        state=found["sigla uf instituicao"],
        abbr=found["sigla instituicao"],
    )
