from functools import partial

from typing import Callable, Iterator, Generic, TypeVar, Iterable

from .abc import Applicative
from .abc import Functor
from .abc import Monoid
from .abc import Monad

A = TypeVar('A')
B = TypeVar('B')


class List(Generic[A], Monad[A], Monoid[A], Applicative[A], Functor[A]):

    """The list monad.

    Wraps an immutable list built from lambda expressions.
    """

    def __init__(self, lambda_list: Callable[[Callable], A]=None) -> None:
        """Initialize List."""

        self._get_value = lambda: lambda_list

    def cons(self, element: A) -> 'List[A]':
        """Add element to front of List."""

        tail = self._get_value()
        return List(lambda sel: sel(element, tail))

    def head(self) -> A:
        """Retrive first element in List."""

        lambda_list = self._get_value()
        return lambda_list(lambda head, _: head)

    def tail(self) -> 'List[A]':
        """Return tail of List."""

        lambda_list = self._get_value()
        return List(lambda_list(lambda _, tail: tail))

    def null(self) -> bool:
        """Return True if List is empty."""
        return not self._get_value()

    @classmethod
    def unit(cls, value: A) -> 'List[A]':
        """Wrap a value within the singleton list."""
        return List.empty().cons(value)
    pure = unit

    def map(self, mapper: Callable[[A], B]) -> 'List[B]':
        """Map a function over a List."""
        try:
            ret = List.from_iterable([mapper(x) for x in self])
        except TypeError:
            ret = List.from_iterable([partial(mapper, x) for x in self])
        return ret

    def apply(self, something: 'List[A]') -> 'List[B]':
        # fs <*> xs = [f x | f <- fs, x <- xs]
        try:
            xs = [f(x) for f in self for x in something]
        except TypeError:
            xs = [partial(f, x) for f in self for x in something]

        return List.from_iterable(xs)

    @classmethod
    def empty(cls) -> 'List':
        """Create an empty list."""
        return cls()

    def append(self, other: 'List[A]') -> 'List[A]':
        """Append other list to this list.
        """

        if self.null():
            return other
        return (self.tail().append(other)).cons(self.head())

    def bind(self, fn: Callable[[A], 'List[B]']) -> 'List[B]':
        """Flatten and map the List.

        Haskell: xs >>= f = concat (map f xs)
        """
        return List.concat(self.map(fn))

    @classmethod
    def from_iterable(cls, iterable: Iterable[A]) -> 'List[A]':

        iterator = iter(iterable)

        def recurse() -> List[A]:
            try:
                value = next(iterator)
            except StopIteration:

                return List.empty()
            return List.unit(value).append(recurse())
        return List.empty().append(recurse())

    def __iter__(self) -> Iterator[A]:
        """Return iterator for List."""

        xs = self  # Don't think we can avoid this mutable local
        while True:
            if xs.null():
                raise StopIteration

            yield xs.head()
            xs = xs.tail()

    def __len__(self) -> int:
        """Return length of List."""

        return 0 if self.null() else (1 + len(self.tail()))

    def __str__(self) -> str:
        """Return string representation of List."""

        return "[%s]" % ", ".join([str(x) for x in self])

    def __repr__(self) -> str:
        """Return string representation of List."""

        return str(self)

    def __eq__(self, other: 'List[A]') -> bool:
        """Compare if List is equal to other List."""

        if self.null() or other.null():
            return True if self.null() and other.null() else False
        return self.head() == other.head() and self.tail() == other.tail()

