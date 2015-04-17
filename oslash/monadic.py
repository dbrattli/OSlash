"""Some useful Monadic functions.

This module contains some useful Monadic functions. Most functions
are extension methods to the Monad class, making them available to
subclasses that inherit from Monad.
"""
from typing import Callable, Any

from .util import extensionmethod, identity
from .abc import Monad


@extensionmethod(Monad, alias="sequence")
def __rshift__(self, next) -> Monad:
    """The "Then" operator.

    Sequentially compose two monadic actions, discarding any value
    produced by the first, like sequencing operators (such as the
    semicolon) in imperative languages.

    Haskell: (>>) :: m a -> m b -> m b
    """
    return self.bind(lambda _: next)


@extensionmethod(Monad)
def join(self) -> Monad:
    """join :: Monad m => m (m a) -> m a

    The join function is the conventional monad join operator. It is
    used to remove one level of monadic structure, projecting its
    bound argument into the outer level."""

    return self.bind(identity)


@extensionmethod(Monad)
def lift(self, func: Callable[[Any], Any]) -> Monad:
    """Map function over monadic value.

    Takes a function and a monadic value and maps the function over the
    monadic value

    Haskell: liftM :: (Monad m) => (a -> b) -> m a -> m b

    This is really the same function as Functor.fmap, but is instead
    implemented using bind, and does not rely on us inheriting from
    Functor.
    """

    return self.bind(lambda x: self.unit(func(x)))


@extensionmethod(Monad, decorator=staticmethod)
def compose(f: Callable[[Any], Monad], g: Callable[[Any], Monad]) -> Callable[[Any], Monad]:
    r"""Monadic compose function.

    Right-to-left Kleisli composition of two monadic functions.

    (<=<) :: Monad m => (b -> m c) -> (a -> m b) -> a -> m c
    f <=< g = \x -> g x >>= f
    """
    return lambda x: g(x).bind(f)
