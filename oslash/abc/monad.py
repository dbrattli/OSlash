r"""
All instances of the Monad typeclass should obey the three monad laws:

Left identity: return a >>= f = f a

Right identity: m >>= return = m

Associativity: (m >>= f) >>= g = m >>= (\x -> f x >>= g)
"""

from abc import ABCMeta, abstractmethod

from typing import Callable, Any


class Monad(metaclass=ABCMeta):

    @abstractmethod
    def bind(self, func: Callable[[Any], 'Monad']) -> 'Monad':
        """Monad bind method.

        Haskell: (>>=) :: m a -> (a -> m b) -> m b

        This is the mother of all methods. It's hard to describe what it
        does, because it can be used for anything:

        * Transformation, for projecting Monadic values and functions.
        * Composition, for composing and combining monadic values and
          functions.
        * Sequencing, of Monadic functions.
        * Flattening, of nested Monadic values.

        Returns a new Monad.
        """

        return NotImplemented

    @classmethod
    def return_(cls, *args) -> 'Monad':
        """return :: a -> m a

        Inject a value into the monadic type."""

        return cls(*args)

    def join(self) -> 'Monad':
        """join :: Monad m => m (m a) -> m a

        The join function is the conventional monad join operator. It is
        used to remove one level of monadic structure, projecting its
        bound argument into the outer level."""

        raise NotImplementedError()

    def lift_m(self, func: Callable[[Any], Any]) -> 'Monad':
        """liftM :: (Monad m) => (a -> b) -> m a -> m b

        This is really the same function as Functor.fmap, but is instead
        implemented using bind, and does not rely on us inheriting from
        Functor.
        """

        return self.bind(lambda x: self.return_(func(x)))

    def __rshift__(self, func: Callable[[Any], 'Monad']) -> 'Monad':
        """Provide the >> operator instead of the Haskell >>= operator"""

        return self.bind(func)


def compose(f: Callable[[Any], Monad], g: Callable[[Any], Monad]) -> Callable[[Any], Monad]:
    r"""Monadic compose function.

    Right-to-left Kleisli composition of monads.

    (<=<) :: Monad m => (b -> m c) -> (a -> m b) -> a -> m c
    f <=< g = \x -> g x >>= f
    """
    return lambda x: g(x).bind(f)
