import pytest

from vitae.lib.result import Err, Ok, Panic, Result, Some, catch
from tests.utils import should


class DescribeOk:
    def it_has_value(self) -> None:
        result: Result[str, str] = Ok("I'm here")

        assert result
        assert result.value == "I'm here"
        assert result.expected("Be there") == "I'm here"

    def it_has_no_error(self) -> None:
        result: Result[str, str] = Ok("I'm here")

        assert result.error is None

    @should("be Some")
    def when_as_either(self) -> None:
        result: Result[str, str] = Ok("I'm here")

        assert Some("I'm here") == result.as_either


class DescribeErr:
    def it_has_no_value(self) -> None:
        result: Result[str, str] = Err("I have no value")

        assert not result
        assert result.value is None

    def it_has_error(self) -> None:
        result: Result[str, str] = Err("I'm an error")

        assert result.error == "I'm an error"

    @should("Panic")
    def when_expected_value_is_not_there(self) -> None:
        result: Result[str, str] = Err("I have no value")

        with pytest.raises(Panic) as panic:
            result.expected("Have no value")

        assert str(panic.value) == "Have no value"


class TestResult:
    @should("be instance of Ok")
    def when_comes_from_ok(self) -> None:
        result: Result[str, str] = Ok("Success")

        assert isinstance(result, Ok)
        assert not isinstance(result, Err)

    @should("be instance of Err")
    def when_comes_from_err(self) -> None:
        result: Result[str, str] = Err("Fail")

        assert isinstance(result, Err)
        assert not isinstance(result, Ok)


class DescribeCatch:
    @should("return Ok")
    def when_expression_not_raises(self) -> None:
        result: Result[int, ZeroDivisionError] = catch(lambda: 1 // 1)

        assert result
        assert result.value == 1

    @should("return Err")
    def when_expression_raises(self) -> None:
        result: Result[int, ZeroDivisionError] = catch(lambda: 1 // 0)

        assert not result
        assert isinstance(result.error, ZeroDivisionError)

    def test_and(self) -> None:
        e, d = "e", "d"
        x, y = "x", "y"

        assert Err(e) == (Err(e) and Err(d))
        assert Err(e) == (Err(e) and Ok(y))
        assert Err(d) == (Ok(x) and Err(d))
        assert Ok(y) == (Ok(x) and Ok(y))

    def test_or(self) -> None:
        e, d = "e", "d"
        x, y = "x", "y"

        assert Err(d) == (Err(e) or Err(d))
        assert Ok(y) == (Err(e) or Ok(y))
        assert Ok(x) == (Ok(x) or Err(d))
        assert Ok(x) == (Ok(x) or Ok(y))
