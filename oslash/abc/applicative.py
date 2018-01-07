from abc import ABCMeta, abstractmethod

from typing import Callable, TypeVar, Generic


class Applicative(metaclass=ABCMeta):
    """Applicative.

    Applicative functors are functors with some extra properties.
    Most importantly, they allow you to apply functions inside the
    functor (hence the name).

    To learn more about Applicative functors:
    * http://www.davesquared.net/2012/05/fp-newbie-learns-applicatives.html

    NOTE: the methods in this base class cannot be typed as it would
    require higher kinded polymorphism, aka generics of generics.
    """

    @abstractmethod
    def apply(self, something):
        """Apply wrapped callable.

        Python: apply(self: Applicative, something: Applicative[Callable[[A], B]]) -> Applicative
        Haskell: (<*>) :: f (a -> b) -> f a -> f b.

        Apply (<*>) is a beefed up fmap. It takes a functor value that
        has a function in it and another functor, and extracts that
        function from the first functor and then maps it over the second
        one.
        """
        raise NotImplementedError

    def __mul__(self, something):
        """(<*>) :: f (a -> b) -> f a -> f b.

        Provide the * as an infix version of apply() since we cannot
        represent the Haskell's <*> operator in Python.
        """
        return self.apply(something)

    def lift_a2(self, func, b):
        """liftA2 :: (Applicative f) => (a -> b -> c) -> f a -> f b -> f c."""

        return func % self * b

    @classmethod
    def pure(cls, x):
        """Applicative functor constructor.

        Use pure if you're dealing with values in an applicative context
        (using them with <*>); otherwise, stick to the default class
        constructor.
        """
        return cls(x)
