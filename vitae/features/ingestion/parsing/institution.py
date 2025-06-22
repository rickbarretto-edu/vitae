from __future__ import annotations

from vitae.features.ingestion.adapters import Institution

from . import _xml as xml

__all__ = ["institution"]


def institution(
    institution_id: str,
    institution_name: str | None,
    data: xml.Node,
) -> Institution:
    found: xml.Node = xml.Node(None)

    for inst in data.all("informacao adicional instituicao"):
        if inst["codigo instituicao"] == institution_id:
            found = inst
            break

    return Institution(
        lattes_id=institution_id,
        name=institution_name,
        country=found["nome pais instituicao"],
        state=found["sigla uf instituicao"],
        abbr=found["sigla instituicao"],
    )
