import pytest
from src.utils.result import Err, Ok, Panic, Result, Some, catch


class DescribeOk:
    def has_value(self):
        result: Result[str, str] = Ok("I'm here")

        assert result
        assert "I'm here" == result.value
        assert "I'm here" == result.expected("Be there")

    def has_no_error(self):
        result: Result[str, str] = Ok("I'm here")

        assert result.error is None

    def it_should_be_some(self):
        result: Result[str, str] = Ok("I'm here")

        assert Some("I'm here") == result.as_either


class DescribeErr:
    def has_no_value(self):
        result: Result[str, str] = Err("I have no value")

        assert not result
        assert result.value is None

    def should_raise_to_expected(self):
        result: Result[str, str] = Err("I have no value")

        with pytest.raises(Panic) as panic:
            result.expected("Have no value")

        assert "Have no value" == str(panic.value)

    def has_error(self):
        result: Result[str, str] = Err("I'm an error")

        assert "I'm an error" == result.error


class TestResult:
    def test_ok_variant(self):
        result: Result[str, str] = Ok("Success")

        assert isinstance(result, Ok)
        assert not isinstance(result, Err)

    def test_err_variant(self):
        result: Result[str, str] = Err("Fail")

        assert isinstance(result, Err)
        assert not isinstance(result, Ok)


class DescribeCatch:
    def should_be_ok_when_not_raise(self):
        result: Result[int, ZeroDivisionError] = catch(lambda: 1 // 1)

        assert result
        assert 1 == result.value

    def should_be_err_when_raise(self):
        result: Result[int, ZeroDivisionError] = catch(lambda: 1 // 0)

        assert not result
        assert isinstance(result.error, ZeroDivisionError)

    def test_and(self):
        e, d = "e", "d"
        x, y = "x", "y"

        assert Err(e) == (Err(e) and Err(d))
        assert Err(e) == (Err(e) and Ok(y))
        assert Err(d) == (Ok(x) and Err(d))
        assert Ok(y) == (Ok(x) and Ok(y))

    def test_or(self):
        e, d = "e", "d"
        x, y = "x", "y"

        assert Err(d) == (Err(e) or Err(d))
        assert Ok(y) == (Err(e) or Ok(y))
        assert Ok(x) == (Ok(x) or Err(d))
        assert Ok(x) == (Ok(x) or Ok(y))
