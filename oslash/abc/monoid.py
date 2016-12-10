from abc import ABCMeta, abstractmethod
from functools import reduce  # type: ignore
from typing import Generic, TypeVar

A = TypeVar('A')


class Monoid(Generic[A], metaclass=ABCMeta):
    """The class of monoids (types with an associative binary operation that
    has an identity). Instances should satisfy the following laws:

    mappend mempty x = x
    mappend x mempty = x
    mappend x (mappend y z) = mappend (mappend x y) z
    mconcat = foldr mappend mempty
    """

    @classmethod
    @abstractmethod
    def empty(cls) -> 'Monoid[A]':
        """mempty :: m

        The empty element and identity of append.
        """

        return NotImplemented

    @abstractmethod
    def append(self, other: 'Monoid[A]') -> 'Monoid[A]':
        """mappend :: m -> m -> m

        An associative operation
        """

        return NotImplemented

    def __add__(self, other: 'Monoid[A]') -> 'Monoid[A]':
        return self.append(other)

    @classmethod
    def concat(cls, xs: 'Monoid[A]') -> 'Monoid[A]':
        """mconcat :: [m] -> m

        Fold a list using the monoid. For most types, the default
        definition for mconcat will be used, but the function is
        included in the class definition so that an optimized version
        can be provided for specific types.
        """

        reducer = lambda a, b: a.append(b)
        return reduce(reducer, xs, cls.empty())
