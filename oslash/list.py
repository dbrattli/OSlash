from functools import partial

from oslash.abc import Applicative
from oslash.abc import Functor
from oslash.abc import Monoid
from oslash.abc import Monad


class List(Monad, Monoid, Applicative, Functor, list):

    """The list monad."""

    def __init__(self, x):
        """Initialize a new list."""
        super().__init__()

        if isinstance(x, list):
            self.extend(x)
        else:
            self.append(x)

    def fmap(self, mapper) -> "List":
        """Map a function over a List."""
        try:
            ret = List([mapper(x) for x in self])
        except TypeError:
            ret = List([partial(mapper, x) for x in self])
        return ret

    def apply(self, something) -> "List":
        # fs <*> xs = [f x | f <- fs, x <- xs]
        try:
            xs = [f(x) for f in self for x in something]
        except TypeError:
            xs = [partial(f, x) for f in self for x in something]

        return List(xs)

    @classmethod
    def mempty(cls) -> "List":
        """Create an empty list"""
        return cls([])

    def mappend(self, other: "List"):
        """Append a list to this list"""
        return List(list(self) + list(other))

    def bind(self, func) -> "List":
        # xs >>= f = concat (map f xs)
        return List.mconcat(self.fmap(func))  # aka flat_map
