# Test

Tests uses `pytest` as test runner, so see their documentation or make sure you have experience with this tool before proceeding.

## RSpec-ish syntax

I changed Pytest's settings to accept something close to Ruby's RSpec which I simply love.

### Accepted class prefixes

- `Test`
- `Suite`
- `Spec`
- `Describe`

### Accepted function prefixes

- `test_`
- `should_`
- `it_`, `its_`
- `have_`, `has_`
- `is_`, `are_`
- `when_`, `and_`

### Usage

```py

class DescribeCar:

    @staticmethod
    def has_engine(): ...

    @staticmethod
    def and_four_wheels(): ...

    @staticmethod
    def is_drivable(): ...

    @staticmethod
    def when_has_low_fuel_should_not_be_drivable(): ...

    @staticmethod
    def should_emit_sound(): ...

```

**Concrete Example:**

```py
class DescribeGraduationOfEducation:
    def is_graduation(self, researcher, document):
        grad = list(education_from_xml(researcher, document))[0]
        assert grad.category == "GRADUACAO"

    def is_cs_course(self, researcher, document):
        grad = list(education_from_xml(researcher, document))[0]
        assert grad.course == "Computer Science"

    def has_turing_as_advisor(self, researcher, document):
        grad = list(education_from_xml(researcher, document))[0]
        assert grad.advisor == "12345"

    def its_starts_at_2014(self, researcher, document):
        grad = list(education_from_xml(researcher, document))[0]
        assert grad.start == 2010

    def and_ends_at_2014(self, researcher, document):
        grad = list(education_from_xml(researcher, document))[0]
        assert grad.end == 2014

    def its_serviced_by_tech_uni(self, researcher, document):
        grad = list(education_from_xml(researcher, document))[0]
        assert grad.institution.lattes_id == "UNI001"
        assert grad.institution.name == "Tech University"

    def is_cs_field(self, researcher, document):
        grad = list(education_from_xml(researcher, document))[0]
        field = grad.fields[0]

        assert field.major == "Ciências Exatas"
        assert field.area == "Ciência da Computação"
        assert field.sub == None
        assert field.specialty == None

```