from abc import ABCMeta, abstractmethod
from functools import partial
from typing import Any

from .applicative import Applicative
from .functor import Functor
from .monoid import Monoid
from .monad import Monad


def get_value(maybe: 'Maybe') -> Any:
    """
    Uses fmap to gets internal value of Maybe type
    :param maybe: Maybe
    :return: :rtype: Any
    """
    value = None

    def mapper(x):
        nonlocal value
        value = x
    maybe.fmap(mapper)
    return value


class Maybe(Monad, Monoid, Applicative, Functor, metaclass=ABCMeta):

    @abstractmethod
    def bind(self, func) -> "Maybe":
        return NotImplemented

    @abstractmethod
    def fmap(self, _) -> "Maybe":
        return NotImplemented

    @abstractmethod
    def apply(self, something) -> "Maybe":
        return NotImplemented

    @classmethod
    def mempty(cls) -> "Maybe":
        return Nothing()

    @abstractmethod
    def mappend(self, other) -> "Maybe":
        return NotImplemented

    @abstractmethod
    def __eq__(self, other) -> bool:
        return NotImplemented


class Just(Maybe):

    def __init__(self, value: Any):
        self._value = lambda: value

    def fmap(self, mapper) -> Maybe:
        # fmap f (Just x) = Just (f x)

        value = self._value()
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Just(result)

    def apply(self, something: Maybe) -> Maybe:
        return something.fmap(self._value())

    def mappend(self, other: Maybe) -> Maybe:
        # m `mappend` Nothing = m
        if isinstance(other, Nothing):
            return self

        other_value = get_value(other)

        # Use + for append if no mappend
        value = self._value()
        if not hasattr(other_value, "mappend"):
            return Just(value + other_value)

        # Just m1 `mappend` Just m2 = Just (m1 `mappend` m2)
        return Just(value.mappend(other_value))

    def bind(self, func) -> "Maybe":
        """Just x >>= f  = f x"""

        value = self._value()
        return func(value)

    def __eq__(self: 'Just', other: Maybe) -> bool:
        other_value = get_value(other)
        result = self._value() == other_value
        return result

    def __str__(self) -> str:
        return "Just %s" % self._value()

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def pure(cls, x: Any) -> Maybe:
        return Just(x)


class Nothing(Maybe):

    def fmap(self, _) -> Maybe:
        return Nothing()

    def apply(self, _) -> Maybe:
        return Nothing()

    def mappend(self, other: Maybe) -> Maybe:
        return other

    def bind(self, func) -> "Maybe":
        """Nothing >>= f = Nothing"""
        return Nothing()

    def __eq__(self, other: Maybe) -> bool:
        return isinstance(other, Nothing)

    def __str__(self) -> str:
        return "Nothing"

    def __repr__(self) -> str:
        return "Nothing"

    @classmethod
    def pure(cls, _) -> Maybe:
        return Nothing()
