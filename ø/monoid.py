from abc import ABCMeta, abstractmethod
from functools import reduce


class Monoid(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def mempty(cls) -> "Monoid":
        """mempty :: m"""
        return NotImplemented

    @abstractmethod
    def mappend(self, other) -> "Monoid":
        """mappend :: m -> m -> m"""
        return NotImplemented

    @classmethod
    def mconcat(cls, xs) -> "Monoid":
        """mconcat :: [m] -> m"""

        reducer = lambda a, b: a.mappend(b)
        return reduce(reducer, xs, cls.mempty())
