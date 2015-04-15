from functools import partial

from typing import Any, Callable, Iterator

from .abc import Applicative
from .abc import Functor
from .abc import Monoid
from .abc import Monad


class List(Monad, Monoid, Applicative, Functor):

    """The list monad.

    Wraps an immutable list built from lambda expressions.
    """

    def __init__(self, xs=None, fn=None):
        if xs and not isinstance(xs, List):
            # Builds List from iterable using cons only
            l = List(xs[1:]).cons(xs[0])
            fn = l._get_value()

        self._get_value = lambda: fn

    def cons(self, value):
        xs = self._get_value()
        return List(fn=lambda fn_: fn_(value, xs))

    def head(self):
        xs = self._get_value()
        return xs(lambda x, _: x)

    def tail(self):
        xs = self._get_value()
        return List(fn=xs(lambda _, xs_: xs_))

    def null(self):
        return not self._get_value()

    @classmethod
    def unit(cls, value):
        """ Wraps a value within the singleton list"""
        return cls().cons(value)
    pure = unit

    def map(self, mapper: Callable[[Any], Any]) -> 'List':
        """Map a function over a List."""
        try:
            ret = List([mapper(x) for x in self])
        except TypeError:
            ret = List([partial(mapper, x) for x in self])
        return ret

    def apply(self, something: 'List') -> 'List':
        # fs <*> xs = [f x | f <- fs, x <- xs]
        try:
            xs = [f(x) for f in self for x in something]
        except TypeError:
            xs = [partial(f, x) for f in self for x in something]

        return List(xs)

    @classmethod
    def empty(cls) -> 'List':
        """Create an empty list"""
        return cls([])

    def append(self, other: 'List'):
        """Append a list to this list"""
        return List(list(self) + list(other))

    def bind(self, func: Callable[[Any], 'List']) -> 'List':
        # xs >>= f = concat (map f xs)
        return List.concat(self.map(func))  # aka flat_map

    def __iter__(self) -> Iterator:
        xs = self  # Don't think we can avoid this mutable local
        while True:
            if xs.null():
                raise StopIteration

            head, xs = xs.head(), xs.tail()
            yield head

    def __str__(self) -> str:
        return "[%s]" % ", ".join([str(x) for x in self])

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: 'List') -> bool:
        return [x for x in self] == [y for y in other]
