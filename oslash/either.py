from abc import abstractmethod
from functools import partial

from typing import Callable, TypeVar, Generic

from oslash.typing import Applicative
from oslash.typing import Functor
from oslash.typing import Monad

TSource = TypeVar("TSource")
TResult = TypeVar("TResult")
TError = TypeVar("TError")


class Either(Generic[TSource, TError]):

    """The Either Monad.

    Represents either a successful computation, or a computation that
    has failed.
    """

    @abstractmethod
    def map(self, _: Callable[[TSource], TResult]) -> "Either[TResult, TError]":
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def pure(cls, value: Callable[[TSource], TResult]) -> "Either[Callable[[TSource], TResult], TError]":
        raise NotImplementedError

    @abstractmethod
    def apply(
        self: "Either[Callable[[TSource], TResult], TError]", something: "Either[TSource, TError]"
    ) -> "Either[TResult, TError]":
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def unit(cls, value: TSource) -> "Right[TSource, TError]":
        raise NotImplementedError

    @abstractmethod
    def bind(self, func: Callable[[TSource], "Either[TResult, TError]"]) -> "Either[TResult, TError]":
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other) -> bool:
        raise NotImplementedError


class Right(Either[TSource, TError]):

    """Represents a successful computation."""

    def __init__(self, value: TSource) -> None:
        self._value = value

    # Functor Section
    # ===============

    def map(self, mapper: Callable[[TSource], TResult]) -> Either[TResult, TError]:
        result = mapper(self._value)
        return Right(result)

    # Applicative Section
    # ===================

    @classmethod
    def pure(cls, value: Callable[[TSource], TResult]) -> "Right[Callable[[TSource], TResult], TError]":
        return Right(value)

    def apply(
        self: "Right[Callable[[TSource], TResult], TError]", something: "Either[TSource, TError]"
    ) -> "Either[TResult, TError]":
        def mapper(other_value):
            try:
                return self._value(other_value)
            except TypeError:
                return partial(self._value, other_value)

        return something.map(mapper)

    # Monad Section
    # =============

    @classmethod
    def unit(cls, value: TSource) -> "Right[TSource, TError]":
        return Right(value)

    def bind(self, func: Callable[[TSource], Either[TResult, TError]]) -> Either[TResult, TError]:
        return func(self._value)

    # Operator Overloads
    # ==================

    def __eq__(self, other) -> bool:
        return isinstance(other, Right) and self._value == other._value

    def __str__(self) -> str:
        return "Right %s" % self._value


class Left(Either[TSource, TError]):

    """Represents a computation that has failed."""

    def __init__(self, error: TError) -> None:
        self._error = error

    @classmethod
    def pure(cls, value: Callable[[TSource], TResult]) -> Either[Callable[[TSource], TResult], TError]:
        return Right(value)

    def apply(self, something: Either) -> Either:
        return Left(self._error)

    def map(self, mapper: Callable[[TSource], TResult]) -> Either[TResult, TError]:
        return Left(self._error)

    @classmethod
    def unit(cls, value: TSource):
        return Right(value)

    def bind(self, func: Callable[[TSource], Either[TResult, TError]]) -> Either[TResult, TError]:
        return Left(self._error)

    def __eq__(self, other) -> bool:
        return isinstance(other, Left) and self._error == other._error

    def __str__(self) -> str:
        return "Left: %s" % self._error


assert(isinstance(Either, Functor))
assert(isinstance(Either, Applicative))
assert(isinstance(Either, Monad))

assert(isinstance(Right, Functor))
assert(isinstance(Right, Applicative))
assert(isinstance(Right, Monad))

assert(isinstance(Left, Functor))
assert(isinstance(Left, Applicative))
assert(isinstance(Left, Monad))
