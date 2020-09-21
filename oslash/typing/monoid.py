from abc import ABCMeta, abstractmethod
from typing import Protocol
from typing_extensions import runtime_checkable


@runtime_checkable
class Monoid(Protocol):
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

    def __add__(self, other):
        """Append other monoid to this monoid.

        Haskell: mappend :: m -> m -> m

        An associative operation
        """
        raise NotImplementedError
