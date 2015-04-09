from abc import ABCMeta, abstractmethod
from functools import partial

from typing import Any, Callable

from .abc import Applicative
from .abc import Functor
from .abc import Monoid
from .abc import Monad


class Maybe(Monad, Monoid, Applicative, Functor, metaclass=ABCMeta):

    """Encapsulates and optional value.

    The Maybe type encapsulates an optional value. A value of type
    Maybe a either contains a value of (represented as Just a), or it is
    empty (represented as Nothing). Using Maybe is a good way to deal
    with errors or exceptional cases without resorting to drastic
    measures such as error.
    """

    @abstractmethod
    def bind(self, func: Callable[[Any], "Maybe"]) -> "Maybe":
        return NotImplemented

    @abstractmethod
    def map(self, mapper: Callable[[Any], Any]) -> "Maybe":
        return NotImplemented

    @abstractmethod
    def apply(self, something: "Maybe") -> "Maybe":
        return NotImplemented

    @classmethod
    def empty(cls) -> "Maybe":
        return Nothing()

    @abstractmethod
    def append(self, other: "Maybe") -> "Maybe":
        return NotImplemented

    @abstractmethod
    def __eq__(self, other: "Maybe") -> bool:
        return NotImplemented

    def __repr__(self) -> str:
        return self.__str__()


class Just(Maybe):

    """A Maybe that contains a value.

    Represents a Maybe that contains a value (represented as Just a).
    """

    def __init__(self, value):
        self._get_value = lambda: value

    def map(self, mapper: Callable[[Any], Any]) -> "Just":
        # fmap f (Just x) = Just (f x)

        value = self._get_value()
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Just(result)

    def apply(self, something: Maybe) -> Maybe:
        return something.map(self._get_value())

    def append(self, other: Maybe) -> Maybe:
        # m `append` Nothing = m
        if isinstance(other, Nothing):
            return self

        other_value = other.value

        # Use + for append if no append
        value = self._get_value()
        if not hasattr(other_value, "append"):
            return Just(value + other_value)

        # Just m1 `append` Just m2 = Just (m1 `append` m2)
        return Just(value.append(other_value))

    def bind(self, func: Callable[[Any], Maybe]) -> Maybe:
        """Just x >>= f = f x"""

        value = self._get_value()
        return func(value)

    def __eq__(self: 'Just', other: Maybe) -> bool:
        return self._get_value() == other.value

    def __str__(self) -> str:
        return "Just %s" % self._get_value()


class Nothing(Maybe):

    """Represents an empty Maybe.

    Represents an empty Maybe that holds nothing (in which case it has
    the value of Nothing).
    """

    def map(self, mapper: Callable[[Any], Any]) -> Maybe:
        return Nothing()

    def apply(self, other: Maybe) -> Maybe:
        return Nothing()

    def append(self, other: Maybe) -> Maybe:
        return other

    def bind(self, func: Callable[[Any], Maybe]) -> Maybe:
        """Nothing >>= f = Nothing

        Nothing in, Nothing out.
        """

        return Nothing()

    def __eq__(self, other: Maybe) -> bool:
        return isinstance(other, Nothing)

    def __str__(self) -> str:
        return "Nothing"
