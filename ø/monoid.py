from abc import ABCMeta, abstractmethod
from functools import reduce


class Monoid(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def mempty(cls) -> "Monoid":
        """mempty :: m

        Identity of mappend"""

        return NotImplemented

    @abstractmethod
    def mappend(self, other) -> "Monoid":
        """mappend :: m -> m -> m

        An associative operation"""

        return NotImplemented

    @classmethod
    def mconcat(cls, xs) -> "Monoid":
        """mconcat :: [m] -> m

        Fold a list using the monoid. For most types, the default definition
        for mconcat will be used, but the function is included in the class
        definition so that an optimized version can be provided for specific
        types."""

        reducer = lambda a, b: a.mappend(b)
        return reduce(reducer, xs, cls.mempty())
