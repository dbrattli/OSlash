from abc import ABCMeta, abstractmethod
from functools import partial
from typing import Any

from .applicative import Applicative
from .functor import Functor
from .monoid import Monoid
from .monad import Monad


class Maybe(Monad, Monoid, Applicative, Functor, metaclass=ABCMeta):
    """The Maybe type encapsulates an optional value. A value of type Maybe a
    either contains a value of (represented as Just a), or it is empty
    (represented as Nothing). Using Maybe is a good way to deal with errors or
    exceptional cases without resorting to drastic measures such as error.
    """

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

    @property
    def value(self: 'Just') -> Any:
        """Uses fmap to gets internal value of Maybe object
        :param self: Just
        :return: :rtype: Any
        """
        value = None

        def mapper(x):
            nonlocal value
            value = x
        self.fmap(mapper)
        return value

    @abstractmethod
    def __eq__(self, other) -> bool:
        return NotImplemented

    def __repr__(self) -> str:
        return self.__str__()


class Just(Maybe):
    """Represents a value of type Maybe that contains a value (represented as
    Just a).
    """

    def __init__(self, value: Any):
        self._get_value = lambda: value

    def fmap(self, mapper) -> Maybe:
        # fmap f (Just x) = Just (f x)

        value = self._get_value()
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Just(result)

    def apply(self, something: Maybe) -> Maybe:
        return something.fmap(self._get_value())

    def mappend(self, other: Maybe) -> Maybe:
        # m `mappend` Nothing = m
        if isinstance(other, Nothing):
            return self

        other_value = other.value

        # Use + for append if no mappend
        value = self._get_value()
        if not hasattr(other_value, "mappend"):
            return Just(value + other_value)

        # Just m1 `mappend` Just m2 = Just (m1 `mappend` m2)
        return Just(value.mappend(other_value))

    def bind(self, func) -> Maybe:
        """Just x >>= f = f x"""

        value = self._get_value()
        return func(value)

    def __eq__(self: 'Just', other: Maybe) -> bool:
        return self._get_value() == other.value

    def __str__(self) -> str:
        return "Just %s" % self._get_value()


class Nothing(Maybe):
    """Represents an empty Maybe that holds nothing (in which case it has the
    value of Nothing).
    """

    def fmap(self, _) -> Maybe:
        return Nothing()

    def apply(self, _) -> Maybe:
        return Nothing()

    def mappend(self, other: Maybe) -> Maybe:
        return other

    def bind(self, func) -> Maybe:
        """Nothing >>= f = Nothing"""
        return Nothing()

    def __eq__(self, other: Maybe) -> bool:
        return isinstance(other, Nothing)

    def __str__(self) -> str:
        return "Nothing"
