"""Applicative Protocol."""

from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class Applicative[T, Arg, Result](Protocol):
    """Applicative.

    Applicative functors are functors with some extra properties.
    Most importantly, they allow you to apply functions inside the
    functor (hence the name).

    To learn more about Applicative functors:
    * http://www.davesquared.net/2012/05/fp-newbie-learns-applicatives.html
    """

    @abstractmethod
    def apply(self, something: Arg, /) -> Result:
        """Apply wrapped callable.

        Python: apply(self: Applicative[Callable[[A], B], F[A], F[B]], something: F[A]) -> F[B]
        Haskell: (<*>) :: f (a -> b) -> f a -> f b.

        Apply (<*>) is a beefed up fmap. It takes a functor value that
        has a function in it and another functor, and extracts that
        function from the first functor and then maps it over the second
        one.
        """
        ...

    @classmethod
    @abstractmethod
    def pure(cls, value: T, /) -> Applicative[T, Arg, Result]:
        """Applicative functor constructor.

        Use pure if you're dealing with values in an applicative context
        (using them with <*>); otherwise, stick to the default class
        constructor.
        """
        ...
