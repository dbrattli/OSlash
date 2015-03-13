from abc import ABCMeta, abstractmethod
from functools import reduce


class Monoid(metaclass=ABCMeta):
    """The class of monoids (types with an associative binary operation that
    has an identity). Instances should satisfy the following laws:

    mappend mempty x = x
    mappend x mempty = x
    mappend x (mappend y z) = mappend (mappend x y) z
    mconcat = foldr mappend mempty
    """

    @classmethod
    @abstractmethod
    def mempty(cls) -> "Monoid":
        """mempty :: m

        The empty element and identity of mappend.
        """

        return NotImplemented

    @abstractmethod
    def mappend(self, other) -> "Monoid":
        """mappend :: m -> m -> m

        An associative operation

        :param self Monoid:
        :param other Monoid:
        :rtype: Monoid
        """

        return NotImplemented

    def __add__(self, other):
        return self.mappend(other)

    @classmethod
    def mconcat(cls, xs) -> "Monoid":
        """mconcat :: [m] -> m

        Fold a list using the monoid. For most types, the default definition
        for mconcat will be used, but the function is included in the class
        definition so that an optimized version can be provided for specific
        types.
        """

        reducer = lambda a, b: a.mappend(b)
        return reduce(reducer, xs, cls.mempty())
