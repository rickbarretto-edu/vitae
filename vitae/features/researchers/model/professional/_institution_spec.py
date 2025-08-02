
from vitae.infra.database import tables

from .institution import LinkedInstitution

class DescribeLinkedInstitution:
    def has_name_as_title_case(self):
        inst = LinkedInstitution("universidade federal de são paulo")
        assert inst.name == "Universidade Federal De São Paulo"

    def is_casted_to_string(self):
        inst = LinkedInstitution("instituto nacional de pesquisas")
        assert str(inst) == "Instituto Nacional De Pesquisas"

    def is_created_from_table_with_institution(self):
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
