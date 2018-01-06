from abc import ABCMeta, abstractmethod
from functools import partial

from typing import Callable, TypeVar, Generic

from oslash.abc import Applicative
from oslash.abc import Functor
from oslash.abc import Monad

A = TypeVar('A')
B = TypeVar('B')
E = TypeVar('E')


class Either(Monad, Applicative, Functor, metaclass=ABCMeta):

    """The Either Monad.

    Represents either a successful computation, or a computation that
    has failed.
    """

    @abstractmethod
    def map(self, _: Callable[[A], B]) -> 'Either':
        return NotImplemented

    @abstractmethod
    def apply(self, something: 'Either') -> 'Either':
        return NotImplemented

    @abstractmethod
    def bind(self, func: Callable[[A], 'Either']) -> 'Either':
        return NotImplemented

    @abstractmethod
    def __eq__(self, other: 'Either') -> bool:
        return NotImplemented


class Right(Either):

    """Represents a successful computation."""

    def __init__(self, value: A) -> None:
        self._value = value

    def map(self, mapper: Callable[[A], B]) -> Either:
        value = self._value
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Right(result)

    def apply(self, something: Either) -> Either:
        return something.map(self._value)

    def bind(self, func: Callable[[A], Either]) -> Either:
        return func(self._value)

    def __eq__(self, other: Either) -> bool:
        return isinstance(other, Right) and self._value == other._value

    def __str__(self) -> str:
        return "Right %s" % self._value


class Left(Either):

    """Represents a computation that has failed."""

    def __init__(self, value: E) -> None:
        self._value = value

    def apply(self, something: Either) -> Either:
        return Left(self._value)

    def map(self, mapper: Callable[[A], B]) -> Either:
        return Left(self._value)

    def bind(self, func: Callable[[A], Either]) -> Either:
        return Left(self._value)

    def __eq__(self, other: Either) -> bool:
        return isinstance(other, Left) and self._value == other._value

    def __str__(self) -> str:
        return "Left %s" % self._value
