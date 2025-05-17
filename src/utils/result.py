"""Rust inspired Result type"""

from abc import ABC
from dataclasses import dataclass
from typing import Any, Callable, NoReturn, TypeVar, cast

__all__ = ["Panic", "Either", "Some", "Empty", "Result", "Ok", "Err", "catch"]


class Panic(RuntimeError):
    pass


@dataclass
class IsEither[T](ABC):
    @property
    def value(self) -> T | None:
        """Returns self._value if there is."""
        ...

    def expected(self, message: str) -> T: ...

    def __bool__(self) -> bool:
        """Returns true for Some and false for Empty"""
        ...

    def __and__(self, other: "IsEither") -> "IsEither":
        return other if (bool(self) and bool(other)) else Empty()

    def __or__(self, other: "IsEither") -> "IsEither":
        return self if self else other

    def __xor__(self, other: "IsEither") -> "IsEither":
        if bool(self) == bool(other):
            return Empty()
        else:
            return self if bool(self) else other


class Some[T](IsEither):
    def __init__(self, value: T = None) -> None:
        self._value = value

    @property
    def value(self) -> T:
        return self._value

    def expected(self, message: str) -> T:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Some):
            return self.value == other.value
        return False

    def __bool__(self) -> bool:
        return True


@dataclass
class Empty[T](IsEither):
    def __init__(self, value: T | None = None):
        pass

    @property
    def value(self) -> None:
        return None

    def expected(self, message: str) -> T:
        raise Panic(message)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Empty)

    def __bool__(self) -> bool:
        return False


type Either[T] = Empty[T] | Some[T]


@dataclass
class IsResult[T, E](ABC):
    @property
    def value(self) -> T | None: ...

    @property
    def error(self) -> E | None: ...

    @property
    def as_either(self) -> Either[T]: ...

    def expected(self, message: str) -> T: ...

    def __bool__(self) -> bool: ...

    def __and__(self, other: "IsResult[T, E]") -> "IsResult[T, E]":
        return self if not self else other

    def __or__(self, other: "IsResult[T, E]") -> "IsResult[T, E]":
        return self if self else other


@dataclass
class Ok[T](IsResult):
    def __init__(self, value: T = None):
        self._value: T = value

    @property
    def value(self) -> T:
        return self._value

    @property
    def error(self) -> None:
        pass

    @property
    def as_either(self) -> Either[T]:
        return Some(self.value)

    def expected(self, message: str) -> T:
        return self.value

    def __bool__(self) -> bool:
        return True

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Ok):
            return self.value == other.value
        return False


@dataclass
class Err[E](IsResult):
    def __init__(self, error: E = None):
        self._error: E = error

    @property
    def value(self) -> None:
        pass

    @property
    def error(self) -> E:
        return self._error

    @property
    def as_either(self) -> Either[None]:
        return Empty()

    def expected(self, message: str) -> NoReturn:
        raise Panic(message)

    def __bool__(self) -> bool:
        return False

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Err):
            return self.error == other.error
        return False


type Result[T, E] = Ok[T] | Err[E]


def catch[T, E: BaseException](expression: Callable[[], T]) -> Result[T, E]:
    try:
        return Ok[T](expression())
    except BaseException as e:
        return Err[E](cast(E, e))
