from functools import partial

from .applicative import Applicative
from .functor import Functor
from .monoid import Monoid
from .monad import Monad


class List(list, Monad, Monoid, Applicative, Functor):

    def __init__(self, x):
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
        pass

    @classmethod
    def mempty(cls) -> "List":
        return List([])

    def mappend(self, other: "List"):
        return List(list(self) + list(other))

    def bind(self, func) -> "List":
        # xs >>= f = concat (map f xs)
        return List.mconcat(self.fmap(func)) # aka flat_map
