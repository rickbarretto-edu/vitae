import datetime as dt

import attrs
from sqlmodel import select

from vitae.infra.database.tables import Researcher
from vitae.features.researchers.model.academic.external import Lattes
from vitae.features.researchers.model.personal import FullName
from vitae.features.researchers.repository import Researchers

type LattesID = str
type CSVContent = str


@attrs.frozen
class LucyLattesRow:
    _lattes: Lattes
    _name: FullName
    _group: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LucyLattesRow):
            return False
        return self.lattes == other.lattes

    @property
    def lattes(self) -> str:
        return self._lattes.id

    @property
    def name(self) -> str:
        return "".join(self._name.each)

    @property
    def group(self) -> str:
        return self._group

    @property
    def as_csv(self) -> str:
        return f"{self.lattes},{self.name},{self.group}"


@attrs.frozen
class LucyLattes:
    associated: list[LucyLattesRow]

    @property
    def as_csv(self) -> CSVContent:
        lucys_header = (
            "# Mantenha como separador a vírgula\n"
            "# Não altere o nome das colunas (linha 5)\n"
            "# Não altere a ordem das colunas e das 5 primeiras linhas\n"
            "# Insira o nome ABREVIADO do pesquisador\n"
            "ID_LATTES,NAME,GROUP"
        )
        return "\n".join(
            [
                lucys_header,
                *[row.as_csv for row in self.associated],
            ]
        )


@attrs.define
class ExportToLucy:
    """Exports Lucy-compatible CSV from a root researcher."""

    _researchers: Researchers

    def csv_of(self, researcher_id: LattesID, depth: int = 5) -> str:
        visited: set[str] = set()
        group_name = dt.datetime.now(dt.UTC).isoformat()

        def rows_from_relations(researcher: Researcher | None, depth: int):
            """Return a flatten list of associated researchers."""
            if depth < 0 or researcher.lattes_id in visited:
                return []

            visited.add(researcher.lattes_id)
            if researcher is None:
                return []

            rows = [
                LucyLattesRow(
                    lattes=Lattes.from_id(researcher.lattes_id),
                    name=FullName(researcher.full_name),
                    group=group_name,
                ),
            ]

            for advising in researcher.student_of:
                rows.extend(rows_from_relations(advising.advisor_id, depth - 1))

            for advising in researcher.advisor_of:
                rows.extend(rows_from_relations(advising.student_id, depth - 1))

            return rows

        with self._researchers.session() as session:
            statement = select(Researcher).where(Researcher.lattes_id == researcher_id)
            researcher = session.exec(statement).first()

            rows = rows_from_relations(researcher, depth)
            return LucyLattes(associated=rows).as_csv
