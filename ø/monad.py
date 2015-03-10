"""
All instances of the Monad typeclass should obey the three monad laws:

Left identity: return a >>= f = f a

Right identity: m >>= return = m

Associativity: (m >>= f) >>= g = m >>= (\\x -> f x >>= g)
"""

from abc import ABCMeta, abstractmethod


class Monad(metaclass=ABCMeta):
    @abstractmethod
    def bind(self, func) -> "Monad":
        """(>>=) :: m a -> (a -> m b) -> m b

        :param Monad[A] self:
        :param Callable[[A], Monad[B]] func:
        :rtype: Monad[B]
        :returns: New Monad wrapping B
        """

        return NotImplemented

    @classmethod
    def return_(cls, a) -> "Monad":
        """return :: a -> m a

        Inject a value into the monadic type."""

        return cls(a)

    def join(self) -> "Monad":
        """join :: Monad m => m (m a) -> m a

        The join function is the conventional monad join operator. It is used
        to remove one level of monadic structure, projecting its bound argument
        into the outer level."""

        raise NotImplementedError()

    def lift_m(self, func):
        """liftM :: (Monad m) => (a -> b) -> m a -> m b

        This is really the same function as Functor.fmap, but is instead
        implemented using bind, and does not rely on us inheriting from
        Functor.
        """

        return self.bind(lambda x: self.return_(func(x)))

    def __rshift__(self, other):
        """Provide the >> operator instead of the Haskell >>= operator"""

        return self.bind(other)
