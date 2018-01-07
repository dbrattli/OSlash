r"""The Monad abstract base class.

All instances of the Monad typeclass should obey the three monad laws:

    1) Left identity: return a >>= f = f a
    2) Right identity: m >>= return = m
    3) Associativity: (m >>= f) >>= g = m >>= (\x -> f x >>= g)
"""

from abc import ABCMeta, abstractmethod
from oslash.util import identity


class Monad(metaclass=ABCMeta):
    """Monad abstract base class.

    NOTE: the methods in this base class cannot be typed as it would
    require higher kinded polymorphism, aka generics of generics.
    """

    @abstractmethod
    def bind(self, fn):
        """Monad bind method.

        Python: bind(self: Monad[A], func: Callable[[A], Monad[B]]) -> Monad[B]
        Haskell: (>>=) :: m a -> (a -> m b) -> m b

        This is the mother of all methods. It's hard to describe what it
        does, because it can be used for pretty much anything:

        * Transformation, for projecting Monadic values and functions.
        * Composition, for composing monadic functions.
        * Chaining, for chaining of functions as a monadic value.
        * Combining, for combining monadic values.
        * Sequencing, of Monadic functions.
        * Flattening, of nested Monadic values.
        * Variable substitution, assign values to variables.

        The Monad doesn’t specify what is happening, only that whatever
        is happening satisfies the laws of associativity and identity.

        Returns a new Monad.
        """
        raise NotImplementedError

    @classmethod
    def unit(cls, value):
        """Wrap a value in a default context.

        Haskell: return :: a -> m a .

        Inject a value into the monadic type. Since return is a reserved
        word in Python, we align with Scala and use the name unit
        instead.
        """
        return cls(value)

    def lift(self, func):
        """Map function over monadic value.

        Takes a function and a monadic value and maps the function over the
        monadic value

        Haskell: liftM :: (Monad m) => (a -> b) -> m a -> m b

        This is really the same function as Functor.fmap, but is instead
        implemented using bind, and does not rely on us inheriting from
        Functor.
        """

        return self.bind(lambda x: self.unit(func(x)))


    def join(self):
        """join :: Monad m => m (m a) -> m a

        The join function is the conventional monad join operator. It is
        used to remove one level of monadic structure, projecting its
        bound argument into the outer level."""

        return self.bind(identity)

    def __or__(self, func):
        """Use | as operator for bind.

        Provide the | operator instead of the Haskell >>= operator
        """
        return self.bind(func)

    def __rshift__(self, next):
        """The "Then" operator.

        Sequentially compose two monadic actions, discarding any value
        produced by the first, like sequencing operators (such as the
        semicolon) in imperative languages.

        Haskell: (>>) :: m a -> m b -> m b
        """
        return self.bind(lambda _: next)
