from abc import ABCMeta, abstractmethod
from functools import reduce


class Monoid(metaclass=ABCMeta):
    """The Monoid abstract base class.

    The class of monoids (types with an associative binary operation that
    has an identity). Instances should satisfy the following laws:

    mappend mempty x = x
    mappend x mempty = x
    mappend x (mappend y z) = mappend (mappend x y) z
    mconcat = foldr mappend mempty

    NOTE: the methods in this base class cannot be typed as it would
    require higher kinded polymorphism, aka generics of generics.
    """

    @classmethod
    @abstractmethod
    def empty(cls):
        """Create empty monoid.

        Haskell: mempty :: m

        The empty element and identity of append.
        """

        raise NotImplementedError

    @abstractmethod
    def append(self, other):
        """Append other monoid to monoid.

        Haskell: mappend :: m -> m -> m

        An associative operation
        """

        raise NotImplementedError

    def __add__(self, other):
        """Append other monoid to monoid."""
        return self.append(other)

    @classmethod
    def concat(cls, xs):
        """mconcat :: [m] -> m

        Fold a list using the monoid. For most types, the default
        definition for mconcat will be used, but the function is
        included in the class definition so that an optimized version
        can be provided for specific types.
        """

        def reducer(a, b):
            return a.append(b)

        return reduce(reducer, xs, cls.empty())
