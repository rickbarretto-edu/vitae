import pytest

from src.utils.result import Either, Empty, Panic, Some


class DescribeSome:
    def its_default_is_none(self):
        result: Either = Some()

        assert result
        assert result.value is None
        assert result.expected("Be None") is None

    def has_value(self):
        result: Either[str] = Some("Value")

        assert result
        assert "Value" == result.value
        assert "Value" == result.expected("has value")
        assert isinstance(result.value, str)


class DescribeEmpty:
    def should_accept_useless_parameter(self):
        result: Either[str] = Empty("value")

        assert not result
        assert result.value is None

        with pytest.raises(Panic) as panic:
            result.expected("There is no value")
        assert "There is no value" == str(panic.value)

    def has_no_value(self):
        result: Either[str] = Empty()

        assert not result
        assert result.value is None

    def should_raise_to_expected(self):
        result: Either[str] = Empty()

        with pytest.raises(Panic) as panic:
            result.expected("Is there")

        assert "Is there" == str(panic.value)


class TestEither:
    def test_some_variant(self):
        success: Either[str] = Some("Success")
        assert isinstance(success, Some)
        assert not isinstance(success, Empty)

    def test_empty_variant(self):
        failed: Either[str] = Empty()
        assert isinstance(failed, Empty)
        assert not isinstance(failed, Some)

    def test_and(self):
        x, y = "x", "y"

        assert Empty() == (Empty() and Empty())
        assert Empty() == (Empty() and Some(y))
        assert Empty() == (Some(x) and Empty())
        assert Some(y) == (Some(x) and Some(y))

    def test_or(self):
        x, y = "x", "y"

        assert Empty() == (Empty() or Empty())
        assert Some(y) == (Empty() or Some(y))
        assert Some(x) == (Some(x) or Empty())
        assert Some(x) == (Some(x) or Some(y))

    def test_xor(self):
        x, y = "x", "y"

        assert Empty() == (Empty() ^ Empty())
        assert Some(y) == (Empty() ^ Some(y))
        assert Some(x) == (Some(x) ^ Empty())
        assert Empty() == (Some(x) ^ Some(y))
