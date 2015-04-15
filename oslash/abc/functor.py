from abc import ABCMeta, abstractmethod

from typing import Callable, Any


class Functor(metaclass=ABCMeta):

    """The Functor class is used for types that can be mapped over.

    Instances of Functor should satisfy the following laws:

    Haskell:
    fmap id  ==  id
    fmap (f . g)  ==  fmap f . fmap g

    Python:
    x.map(id) == id(x)
    x.map(compose(f, g)) == x.map(g).map(f)

    The instances of Functor for lists, Maybe and IO satisfy these laws.
    """

    @abstractmethod
    def map(self, fn: Callable[[Any], Any]) -> 'Functor':
        """Map a function over wrapped values.

        Map knows how to apply functions to values that are wrapped in
        a context.
        """
        return NotImplemented

    def __rmod__(self, fn: Callable[[Any], Any]) -> 'Functor':
        r"""Infix version of map.

        Haskell: <$>

        Example:
        >>> (lambda x: x+2) % Just(40)
        42

        Returns a new Functor.
        """
        return self.map(fn)

    @property
    def value(self) -> Any:
        """Get value of Functor.

        Uses map to extract the internal value of the Functor.
        """
        value = None  # type: Any

        def mapper(x):
            nonlocal value
            value = x
        self.map(mapper)
        return value
