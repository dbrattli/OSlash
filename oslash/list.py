from functools import partial

from typing import Any, Callable

from .abc import Applicative
from .abc import Functor
from .abc import Monoid
from .abc import Monad


class List(Monad, Monoid, Applicative, Functor, tuple):

    """The list monad.

    Wraps an immutable list. This is why it inherits from the Python
    tuple and not list.
    """

    @classmethod
    def unit(cls, *args):
        """ Wraps a value within the singleton list"""
        return cls(args)
    pure = unit

    def map(self, mapper: Callable[[Any], Any]) -> 'List':
        """Map a function over a List."""
        try:
            ret = List([mapper(x) for x in self])
        except TypeError:
            ret = List([partial(mapper, x) for x in self])
        return ret

    def apply(self, something: "List") -> "List":
        # fs <*> xs = [f x | f <- fs, x <- xs]
        try:
            xs = [f(x) for f in self for x in something]
        except TypeError:
            xs = [partial(f, x) for f in self for x in something]

        return List(xs)

    @classmethod
    def empty(cls) -> "List":
        """Create an empty list"""
        return cls([])

    def append(self, other: "List"):
        """Append a list to this list"""
        return List(list(self) + list(other))

    def bind(self, func: Callable[[Any], "List"]) -> "List":
        # xs >>= f = concat (map f xs)
        return List.concat(self.map(func))  # aka flat_map
