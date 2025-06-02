import pytest

from src.lib.result import Either, Empty, Panic, Some


class DescribeSome:
    def its_default_is_none(self) -> None:
        result: Either = Some()

        assert result
        assert result.value is None
        assert result.expected("Be None") is None

    def has_value(self) -> None:
        result: Either[str] = Some("Value")

        assert result
        assert result.value == "Value"
        assert result.expected("has value") == "Value"
        assert isinstance(result.value, str)


class DescribeEmpty:
    def should_accept_useless_parameter(self) -> None:
        result: Either[str] = Empty("value")

        assert not result
        assert result.value is None

        with pytest.raises(Panic) as panic:
            result.expected("There is no value")
        assert str(panic.value) == "There is no value"

    def has_no_value(self) -> None:
        result: Either[str] = Empty()

        assert not result
        assert result.value is None

    def should_raise_to_expected(self) -> None:
        result: Either[str] = Empty()

        with pytest.raises(Panic) as panic:
            result.expected("Is there")

        assert str(panic.value) == "Is there"


class TestEither:
    def test_some_variant(self) -> None:
        success: Either[str] = Some("Success")
        assert isinstance(success, Some)
        assert not isinstance(success, Empty)

    def test_empty_variant(self) -> None:
        failed: Either[str] = Empty()
        assert isinstance(failed, Empty)
        assert not isinstance(failed, Some)

    def test_and(self) -> None:
        x, y = "x", "y"

        assert Empty() == (Empty() and Empty())
        assert Empty() == (Empty() and Some(y))
        assert Empty() == (Some(x) and Empty())
        assert Some(y) == (Some(x) and Some(y))

    def test_or(self) -> None:
        x, y = "x", "y"

        assert Empty() == (Empty() or Empty())
        assert Some(y) == (Empty() or Some(y))
        assert Some(x) == (Some(x) or Empty())
        assert Some(x) == (Some(x) or Some(y))

    def test_xor(self) -> None:
        x, y = "x", "y"

        assert Empty() == (Empty() ^ Empty())
        assert Some(y) == (Empty() ^ Some(y))
        assert Some(x) == (Some(x) ^ Empty())
        assert Empty() == (Some(x) ^ Some(y))
