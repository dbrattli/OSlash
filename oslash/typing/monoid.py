from abc import abstractmethod
from typing import Protocol, TypeVar
from typing_extensions import runtime_checkable

TSource = TypeVar('TSource')


@runtime_checkable
class Monoid(Protocol[TSource]):
    """The Monoid abstract base class.

    The class of monoids (types with an associative binary operation that
    has an identity). Instances should satisfy the following laws:

    mappend mempty x = x
    mappend x mempty = x
    mappend x (mappend y z) = mappend (mappend x y) z
    mconcat = foldr mappend mempty
    """

    @classmethod
    @abstractmethod
    def empty(cls) -> 'Monoid[TSource]':
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
