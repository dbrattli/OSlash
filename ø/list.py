from functools import partial, reduce

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

    def mempty(cls) -> "List":
        return List([])

    def mappend(self, other: "List"):
        # m `mappend` Nothing = m

        other_value = other.value

        # Use + for append if no mappend
        value = self._get_value()
        if not hasattr(other_value, "mappend"):
            return List(value + other_value)

        # List m1 `mappend` List m2 = List (m1 `mappend` m2)
        return List(value.mappend(other_value))

    def bind(self, func) -> "List":
        # xs >>= f = concat (map f xs)

        xs = self.fmap(func).concat() # aka flat_map
        return xs

    def concat(self):
        if self == List([]):
            return self

        def reducer(x, y):
            if isinstance(y, List):
                return x.mappend(y)
            return x.mappend(List(y))

        return List(reduce(reducer, self))
