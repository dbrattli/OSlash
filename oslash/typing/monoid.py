"""Monoid Protocol."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

from typing_extensions import runtime_checkable

if TYPE_CHECKING:
    from typing import Self


@runtime_checkable
class Monoid[T](Protocol):
    """The Monoid Protocol.

    The class of monoids (types with an associative binary operation that
    has an identity). Instances should satisfy the following laws:

    mappend mempty x = x
    mappend x mempty = x
    mappend x (mappend y z) = mappend (mappend x y) z
    mconcat = foldr mappend mempty
    """

    @classmethod
    @abstractmethod
    def empty(cls) -> Self:
        """Create empty monoid.

        Haskell: mempty :: m

        The empty element and identity of append.
        """
        ...

    @abstractmethod
    def __add__(self, other: Monoid[T]) -> Self:
        """Append other monoid to this monoid.

        Haskell: mappend :: m -> m -> m

        An associative operation
        """
        ...
