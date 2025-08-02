
from vitae.infra.database import tables

from .institution import LinkedInstitution

class DescribeLinkedInstitution:
    def has_name_title_cased(self):
        inst = LinkedInstitution("universidade federal de são paulo")
        assert inst.name == "Universidade Federal De São Paulo"

    def supports_str(self):
        inst = LinkedInstitution("instituto nacional de pesquisas")
        assert str(inst) == "Instituto Nacional De Pesquisas"

    def supports_from_table(self):
        address = tables.Address(
            researcher_id="0",
            institution_id="1",
            institution=tables.Institution(
                lattes_id="1",
                name="centro técnico"
            )
        )

        inst = LinkedInstitution.from_table(address)
        assert isinstance(inst, LinkedInstitution)
        assert inst.name == "Centro Técnico"

    def is_none_if_no_institution(self):
        address = tables.Address(
            researcher_id="0",
        )

        inst = LinkedInstitution.from_table(address)
        assert inst is None
