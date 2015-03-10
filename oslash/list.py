from functools import partial

from .applicative import Applicative
from .functor import Functor
from .monoid import Monoid
from .monad import Monad


class List(Monad, Monoid, Applicative, Functor, list):

    def __init__(self, x):
        super().__init__()

        if isinstance(x, list):
            self.extend(x)
        else:
            self.append(x)

    def fmap(self, mapper) -> "List":
        try:
            ret = List([mapper(x) for x in self])
        except TypeError:
            ret = List([partial(mapper, x) for x in self])
        return ret

    def apply(self, something) -> "List":
        # fs <*> xs = [f x | f <- fs, x <- xs]
        try:
            xs = [ f(x) for f in self for x in something]
        except TypeError:
            xs = [ partial(f, x) for f in self for x in something]

        return List(xs)

    @classmethod
    def mempty(cls) -> "List":
        return cls([])

    def mappend(self, other: "List"):
        return List(list(self) + list(other))

    def bind(self, func) -> "List":
        # xs >>= f = concat (map f xs)
        return List.mconcat(self.fmap(func)) # aka flat_map
