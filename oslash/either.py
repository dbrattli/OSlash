from abc import ABCMeta, abstractmethod
from functools import partial

from typing import Any, Callable

from oslash.abc import Applicative
from oslash.abc import Functor
from oslash.abc import Monad


class Either(Monad, Applicative, Functor, metaclass=ABCMeta):

    """The Either Monad.

    Represents either a successful computation, or a computation that
    has failed.
    """

    @abstractmethod
    def map(self, _) -> "Either":
        return NotImplemented

    @abstractmethod
    def apply(self, something: "Either") -> "Either":
        return NotImplemented

    @abstractmethod
    def bind(self, func: Callable[[Any], "Either"]) -> "Either":
        return NotImplemented

    @abstractmethod
    def __eq__(self, other: "Either") -> bool:
        return NotImplemented


class Right(Either):

    """Represents a successful computation."""

    def __init__(self, value):
        self._get_value = lambda: value

    def map(self, mapper: Callable[[Any], Any]) -> Either:
        value = self._get_value()
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Right(result)

    def apply(self, something: Either) -> Either:
        return something.map(self._get_value())

    def bind(self, func: Callable[[Any], Either]) -> Either:
        return func(self._get_value())

    def __eq__(self, other) -> bool:
        return isinstance(other, Right) and self._get_value() == other.value

    def __str__(self) -> str:
        return "Right %s" % self._get_value()


class Left(Either):

    """Represents a computation that has failed."""

    def apply(self, something: Either) -> Either:
        return Left(self._get_value())

    def __init__(self, value: Any):
        self._get_value = lambda: value

    def map(self, mapper: Callable[[Any], Any]) -> Either:
        try:
            mapper(self._get_value())  # TODO: fixme
        except TypeError:
            pass
        return Left(self._get_value())

    def bind(self, func: Callable[[Any], Either]) -> Either:
        return Left(self._get_value())

    def __eq__(self, other: Either) -> bool:
        return isinstance(other, Left) and self._get_value() == other.value

    def __str__(self) -> str:
        return "Left %s" % self._get_value()
