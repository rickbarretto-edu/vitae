import attrs

from vitae.features.researchers.model.academic.external import Lattes
from vitae.features.researchers.model.personal import FullName

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
class LucyLattesCSV:
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
            lucys_header,
            *[row.as_csv for row in self.associated],
        )
