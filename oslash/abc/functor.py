from abc import ABCMeta, abstractmethod

from typing import TypeVar, Generic

T = TypeVar('T')


class Functor(Generic[T], metaclass=ABCMeta):
    """The Functor class is used for types that can be mapped over.

    Instances of Functor should satisfy the following laws:

    Haskell:
    fmap id  ==  id
    fmap (f . g)  ==  fmap f . fmap g

    Python:
    x.map(id) == id(x)
    x.map(compose(f, g)) == x.map(g).map(f)

    The instances of Functor for lists, Maybe and IO satisfy these laws.

    NOTE: the methods in this base class cannot be typed as it would
    require higher kinded polymorphism, aka generics of generics.
    """

    @abstractmethod
    def map(self, fn):
        """Map a function over wrapped values.

        Map knows how to apply functions to values that are wrapped in
        a context.
        """
        return NotImplemented

    def __rmod__(self, fn):
        """Infix version of map.

        Haskell: <$>

        Example:
        >>> (lambda x: x+2) % Just(40)
        42

        Returns a new Functor.
        """
        return self.map(fn)
