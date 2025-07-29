from functools import cached_property

import attrs

from vitae.features.researchers import schemes
from vitae.features.researchers.repository import Filters


@attrs.frozen
class LoadFilters:
    filters: Filters

    @cached_property
    def all(self) -> schemes.Filters:
        return {
            "countries": list(self.filters.countries),
            "states": list(self.filters.states),
            "titles": list(self.filters.titles),
            "expertises": list(self.filters.expertises),
        }
