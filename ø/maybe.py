from abc import ABCMeta, abstractmethod
from functools import partial

from .applicative import IApplicative
from .functor import IFunctor


class IMaybe(IApplicative, IFunctor, metaclass=ABCMeta):
    @abstractmethod
    def apply(self, something) -> "IMaybe":
        return NotImplemented

    @abstractmethod
    def fmap(self, _) -> "IMaybe":
        return NotImplemented

    @abstractmethod
    def __eq__(self, other):
        return NotImplemented


class Just(IMaybe):
    def __init__(self, value):

        self._value = lambda: value

    def fmap(self, mapper) -> IMaybe:
        # fmap f (Just x) = Just (f x)

        value = self._value()
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Just(result)

    def apply(self, something) -> IMaybe:
        return something.fmap(self._value())

    def __eq__(self: "Just", other: IMaybe) -> bool:
        other_value = None

        def mapper(x):
            nonlocal other_value
            other_value = x
        other.fmap(mapper)
        result = self._value() == other_value
        return result

    def __str__(self) -> str:
        return "Just %s" % self._value()

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def pure(cls, x) -> IMaybe:
        return Just(x)


class Nothing(IMaybe):
    def fmap(self, _) -> IMaybe:
        return Nothing()

    def apply(self, _) -> IMaybe:
        return Nothing()

    def __eq__(self, other) -> bool:
        return isinstance(other, Nothing)

    def __str__(self) -> str:
        return "Nothing"

    def __repr__(self) -> str:
        return "Nothing"

    @classmethod
    def pure(cls, _) -> IMaybe:
        return Nothing()
