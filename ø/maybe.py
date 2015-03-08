from abc import ABCMeta, abstractmethod
from functools import partial

from .applicative import Applicative
from .functor import Functor
from .monoid import Monoid

def get_value(other):
    value = None

    def mapper(x):
        nonlocal value
        value = x
    other.fmap(mapper)
    return value

class Maybe(Monoid, Applicative, Functor, metaclass=ABCMeta):

    @abstractmethod
    def fmap(self, _) -> "IMaybe":
        return NotImplemented

    @abstractmethod
    def apply(self, something) -> "IMaybe":
        return NotImplemented

    @classmethod
    def mempty(cls) -> "IMaybe":
        return Nothing()

    @abstractmethod
    def mappend(self, other) -> "IMaybe":
        return NotImplemented

    @abstractmethod
    def __eq__(self, other):
        return NotImplemented

class Just(Maybe):

    def __init__(self, value):

        self._value = lambda: value

    def fmap(self, mapper) -> Maybe:
        # fmap f (Just x) = Just (f x)

        value = self._value()
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Just(result)

    def apply(self, something) -> Maybe:
        return something.fmap(self._value())

    def mappend(self, other) -> "IMaybe":
        # m `mappend` Nothing = m
        if isinstance(other, Nothing):
            return self

        global get_value
        other_value = get_value(other)

        # Use + for append if no mappend
        value = self._value()
        if not hasattr(other_value, "mappend"):
            return Just(value + other_value)

        # Just m1 `mappend` Just m2 = Just (m1 `mappend` m2)
        return Just(value.mappend(other_value))

    def __eq__(self: "Just", other: Maybe) -> bool:
        global get_value
        other_value = get_value(other)
        result = self._value() == other_value
        return result

    def __str__(self) -> str:
        return "Just %s" % self._value()

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def pure(cls, x) -> Maybe:
        return Just(x)


class Nothing(Maybe):

    def mappend(self, other) -> "IMaybe":
        return other

    def fmap(self, _) -> Maybe:
        return Nothing()

    def apply(self, _) -> Maybe:
        return Nothing()

    def __eq__(self, other) -> bool:
        return isinstance(other, Nothing)

    def __str__(self) -> str:
        return "Nothing"

    def __repr__(self) -> str:
        return "Nothing"

    @classmethod
    def pure(cls, _) -> Maybe:
        return Nothing()
