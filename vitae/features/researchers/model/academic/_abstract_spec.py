from .abstract import Abstract


class DescribeAbstract:
    def has_full_text(self):
        abstract = Abstract(
            "This is the complete text of the curriculum abstract.",
        )
        assert (
            abstract.full
            == "This is the complete text of the curriculum abstract."
        )

    def has_brief_text_under_limit(self):
        short_text = "This abstract is short."
        abstract = Abstract(short_text, brief_limit=50)
        assert abstract.brief == short_text

    def has_brief_text_exactly_at_limit(self):
        text = "word " * 50
        expected = "word " * 50
        abstract = Abstract(text.strip())
        assert abstract.brief == expected.strip()

    def has_brief_text_over_limit(self):
        text = "word " * 60
        expected = "word " * 50
        abstract = Abstract(text.strip())
        assert abstract.brief == expected.strip() + "..."
