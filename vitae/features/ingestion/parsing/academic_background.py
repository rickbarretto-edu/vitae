from collections.abc import Iterator

from vitae.features.ingestion.adapters.schema import AcademicBackground

from . import _xml as xml

__all__ = ["academic_background"]


def academic_background(
    researcher_id: str,
    data: xml.Node,
) -> Iterator[AcademicBackground]:
    """Extract academic background information from a Lattes curriculum XML.

    Academic Backgound is a section of general data.
    This contains all the Researcher's academic data such as courses
    and graduations.

    Yields
    ------
    Researcher's Academic backgrounds.

    XML Schema
    ----------
        formacao-academica-titulacao: [
            graduacao: {
                sequencia-formacao: integer
                nivel: integer
                titulo-do-trabalho-de-conclusao-de-curso: string
                nome-do-orientador: string
                codigo-instituicao: string
                nome-instituicao: string
                codigo-orgao: string
                nome-orgao: string
                curso-codigo: string
                nome-curso: string
                codigo-area-curso: string
                status-do-curso: string
                ano-de-inicio: integer
                ano-de-conclusao: integer
                flag-bolsa: boolean
                codigo-agencia-financiadora: string
                nome-agencia: string
                numero-id-orientador: string
                codigo-curso-capes: string
                formacao-academica-titulacao: string
                ...
            },
            especializacao: {
                sequencia-formacao: integer
                nivel: integer
                titulo-da-monografia: string
                nome-do-orientador: string
                codigo-instituicao: string
                nome-instituicao: string
                codigo-orgao: string
                nome-orgao: string
                codigo-curso: string
                nome-curso: string
                status-do-curso: string
                ano-de-inicio: integer
                ano-de-conclusao: integer
                flag-bolsa: boolean
                codigo-agencia-financiadora: string
                nome-agencia: string
                carga-horaria: integer
            }

            mestrado | doutorado: {
                sequencia-formacao: integer
                nivel: integer
                codigo-instituicao: string
                nome-instituicao: string
                codigo-orgao: string
                nome-orgao: string
                codigo-curso: string
                nome-curso: string
                codigo-area-curso: string
                status-do-curso: string
                ano-de-inicio: integer
                ano-de-conclusao: integer
                flag-bolsa: boolean
                codigo-agencia-financiadora: string
                nome-agencia: string
                ano-de-obtencao-do-titulo: integer
                titulo-da-dissertacao-tese: string
                nome-completo-orientador: string
                tipo-mestrado: string
                numero-id-orientador: string
                codigo-curso-capes: string
                nome-do-co-orientador: string

                tipo-doutorado: string
                codigo-instituicao-dout: string
                nome-instituicao-dout: string
                codigo-instituicao-outra-dout: string
                nome-instituicao-outra-dout: string
                nome-orientador-dout: string
                nome-do-co-orientador: string
                nome-do-orientador-sanduiche: string
                nome-do-orientador-co-tutela: string
                codigo-instituicao-co-tutela: string
                codigo-instituicao-sanduiche: string
                codigo-instituicao-outra-co-tutela: string
                codigo-instituicao-outra-sanduiche: string
                ...
            }
        ]

    """
    for background in (
        xml.find(data.element, "formacao academica titulacao") or []
    ):
        institution = xml.attribute(background, "nome instituicao")
        if institution is None:
            institution = "Unknown Institution"

        yield AcademicBackground(
            researcher_id=researcher_id,
            type=background.tag,
            institution=institution,
            course=xml.attribute(background, "nome curso"),
            start_year=xml.as_int(xml.attribute(background, "ano de inicio")),
            end_year=xml.as_int(xml.attribute(background, "ano de conclusao")),
        )
