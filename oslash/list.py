import collections
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

    def __init__(self, lambda_list: Callable[[Callable], Any]=None):
        """Initialize List."""

        # Accept building List from a Python iterable
        if isinstance(lambda_list, collections.Iterable):
            # Partially build List from iterable using cons only
            l = List(lambda_list[1:]).cons(lambda_list[0]) if lambda_list else List()
            lambda_list = l._get_value()

        self._get_value = lambda: lambda_list

    def cons(self, element: Any) -> 'List':
        """Append element to List."""
        tail = self._get_value()
        return List(lambda sel: sel(element, tail))

    def head(self) -> Any:
        """Retrive first element in List."""
        lambda_list = self._get_value()
        return lambda_list(lambda head, _: head)

    def tail(self) -> 'List':
        """Return tail of List."""
        lambda_list = self._get_value()
        return List(lambda_list(lambda _, tail: tail))

    def null(self) -> bool:
        """Return True if List is emtpty."""
        return not self._get_value()

    @classmethod
    def unit(cls, value: Any):
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
        """Create an empty list."""
        return cls()

    def append(self, other: 'List'):
        """Append a list to this list."""
        return List(list(self) + list(other))

    def bind(self, fn: Callable[[Any], 'List']) -> 'List':
        """Flatten and map the List.

        Haskell: xs >>= f = concat (map f xs)
        """
        return List.concat(self.map(fn))

    def __iter__(self) -> Iterator:
        """Return iterator for List."""
        xs = self  # Don't think we can avoid this mutable local
        while True:
            if xs.null():
                raise StopIteration

            head, xs = xs.head(), xs.tail()
            yield head

    def __len__(self) -> int:
        """Return length of List."""
        return 0 if self.null() else (1 + len(self.tail()))

    def __str__(self) -> str:
        return "[%s]" % ", ".join([str(x) for x in self])

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: 'List') -> bool:
        """Compare if List is equal to other List."""
        return [x for x in self] == [y for y in other]
