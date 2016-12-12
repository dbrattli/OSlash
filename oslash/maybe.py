from abc import ABCMeta, abstractmethod
from functools import partial

from typing import Any, Callable, TypeVar, Generic

from .abc import Applicative
from .abc import Functor
from .abc import Monoid
from .abc import Monad

A = TypeVar("A")
B = TypeVar("B")


class Maybe(Generic[A], Monad[A], Monoid[A], Applicative[A], Functor[A], metaclass=ABCMeta):

    """Encapsulates an optional value.

    The Maybe type encapsulates an optional value. A value of type
    Maybe a either contains a value of (represented as Just a), or it is
    empty (represented as Nothing). Using Maybe is a good way to deal
    with errors or exceptional cases without resorting to drastic
    measures such as error.
    """

    @abstractmethod
    def bind(self, func: Callable[[A], 'Maybe[B]']) -> 'Maybe[B]':
        return NotImplemented

    @abstractmethod
    def map(self, mapper: Callable[[A], B]) -> 'Maybe[B]':
        return NotImplemented

    @abstractmethod
    def apply(self, something: 'Maybe') -> 'Maybe':
        return NotImplemented

    @classmethod
    def empty(cls) -> 'Maybe[A]':
        return Nothing()

    @abstractmethod
    def append(self, other: 'Maybe[A]') -> 'Maybe[A]':
        return NotImplemented

    @abstractmethod
    def from_just(self) -> A:
        return NotImplemented

    @property
    def is_nothing(self) -> bool:
        return False

    @property
    def is_just(self) -> bool:
        return False

    @abstractmethod
    def from_maybe(self, default: A) -> A:
        return NotImplemented

    @abstractmethod
    def __eq__(self, other: 'Maybe[A]') -> bool:
        return NotImplemented

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        return False


class Just(Generic[A], Maybe[A]):

    """A Maybe that contains a value.

    Represents a Maybe that contains a value (represented as Just a).
    """

    def __init__(self, value: A) -> None:
        self._value = value

    def map(self, mapper: Callable[[A], B]) -> 'Just[B]':
        # fmap f (Just x) = Just (f x)

        value = self._value
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Just(result)

    def apply(self, something: Maybe[A]) -> Maybe[B]:
        return something.map(self._value)

    def append(self, other: Maybe[A]) -> Maybe[A]:
        # m `append` Nothing = m
        if other.is_nothing:
            return self

        other_value = other.from_just()

        # Use + for append if no append
        value = self._value
        if not hasattr(other_value, "append"):
            return Just(value + other_value)

        # Just m1 `append` Just m2 = Just (m1 `append` m2)
        return Just(value.append(other_value))

    def bind(self, func: Callable[[A], Maybe[B]]) -> Maybe[B]:
        """Just x >>= f = f x"""

        value = self._value
        return func(value)

    def from_just(self) -> A:
        return self._value

    def from_maybe(self, default: A) -> A:
        return self._value

    def is_just(self) -> bool:
        return True

    def __bool__(self) -> bool:
        return bool(self._value)

    def __eq__(self, other: Maybe[A]) -> bool:
        if other.is_nothing:
            return False

        return self._value == other.from_just()

    def __str__(self) -> str:
        return "Just %s" % self._value


class Nothing(Generic[A], Maybe[A]):

    """Represents an empty Maybe.

    Represents an empty Maybe that holds nothing (in which case it has
    the value of Nothing).
    """

    def map(self, mapper: Callable[[A], B]) -> Maybe[B]:
        return Nothing()

    def apply(self, other: Maybe) -> Maybe:
        return Nothing()

    def append(self, other: Maybe[A]) -> Maybe[A]:
        return other

    def bind(self, func: Callable[[A], Maybe[B]]) -> Maybe[B]:
        """Nothing >>= f = Nothing

        Nothing in, Nothing out.
        """

        return Nothing()

    def from_just(self) -> A:
        raise Exception("Nothing")

    def from_maybe(self, default: A) -> A:
        return default

    def is_nothing(self) -> bool:
        return True

    def __eq__(self, other: Maybe[A]) -> bool:
        return isinstance(other, Nothing)

    def __str__(self) -> str:
        return "Nothing"
