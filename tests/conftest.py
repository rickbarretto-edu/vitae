import pytest
import jinjax

@pytest.fixture(scope="session")
def catalog():
    catalog = jinjax.Catalog()
    catalog.add_folder("vitae/features/researchers/templates")
    return catalog
