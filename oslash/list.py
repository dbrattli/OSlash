from functools import partial, reduce

from typing import Callable, Iterator, TypeVar, Iterable, Sized, Any, cast, Optional

from .typing import Applicative
from .typing import Functor
from .typing import Monoid
from .typing import Monad

TSource = TypeVar("TSource")
TResult = TypeVar("TResult")
TSelector = Callable[[TSource, Optional[Callable]], Any]


class List(Iterable[TSource], Sized):
    """The list monad.

    Wraps an immutable list built from lambda expressions.
    """

    def __init__(self, lambda_list: Optional[Callable[[TSelector], Any]] = None) -> None:
        """Initialize List."""

        self._value = lambda_list

    def cons(self, element: TSource) -> 'List[TSource]':
        """Add element to front of List."""

        tail = self._value
        return List(lambda sel: sel(element, tail))

    def head(self) -> TSource:
        """Retrive first element in List."""

        lambda_list = self._value
        if lambda_list is None:
            raise IndexError("List is empty")

        return cast(TSource, lambda_list(lambda head, _: head))

    def tail(self) -> 'List[TSource]':
        """Return tail of List."""

        lambda_list = self._value
        if lambda_list is None:
            raise IndexError("List is empty")

        return List(lambda_list(lambda _, tail: tail))

    def null(self) -> bool:
        """Return True if List is empty."""
        return not self._value

    @classmethod
    def unit(cls, value: Any) -> 'List':
        """Wrap a value within the singleton list."""
        return List.empty().cons(value)

    pure = unit

    def map(self, mapper: Callable[[TSource], TResult]) -> 'List[TResult]':
        """Map a function over a List."""
        ret = List.from_iterable([mapper(x) for x in self])
        return ret

    def apply(self, something: 'List') -> 'List':
        # fs <*> xs = [f x | f <- fs, x <- xs]
        try:
            xs = [f(x) for f in self for x in something]
        except TypeError:
            xs = [partial(f, x) for f in self for x in something]

        return List.from_iterable(xs)

    @classmethod
    def empty(cls) -> 'List[TSource]':
        """Create an empty list."""
        return cls()

    def append(self, other: 'List') -> 'List':
        """Append other list to this list."""

        if self.null():
            return other
        return (self.tail().append(other)).cons(self.head())

    def bind(self, fn: Callable[[Any], 'List']) -> 'List':
        """Flatten and map the List.

        Haskell: xs >>= f = concat (map f xs)
        """
        return List.concat(self.map(fn))

    @classmethod
    def from_iterable(cls, iterable: Iterable) -> 'List':
        """Create list from iterable."""

        iterator = iter(iterable)

        def recurse() -> List:
            try:
                value = next(iterator)
            except StopIteration:

                return List.empty()
            return List.unit(value).append(recurse())
        return List.empty().append(recurse())

    @classmethod
    def concat(cls, xs):
        """mconcat :: [m] -> m

        Fold a list using the monoid. For most types, the default
        definition for mconcat will be used, but the function is
        included in the class definition so that an optimized version
        can be provided for specific types.
        """

        def reducer(a, b):
            return a + b

        return reduce(reducer, xs, cls.empty())

    def __iter__(self) -> Iterator:
        """Return iterator for List."""

        xs = self  # Don't think we can avoid this mutable local
        while True:
            if xs.null():
                return

            yield xs.head()
            xs = xs.tail()

    def __or__(self, func):
        """Use | as operator for bind.

        Provide the | operator instead of the Haskell >>= operator
        """
        return self.bind(func)

    def __rshift__(self, next):
        """The "Then" operator.

        Sequentially compose two monadic actions, discarding any value
        produced by the first, like sequencing operators (such as the
        semicolon) in imperative languages.

        Haskell: (>>) :: m a -> m b -> m b
        """
        return self.bind(lambda _: next)

    def __add__(self, other):
        return self.append(other)

    def __len__(self) -> int:
        """Return length of List."""

        return 0 if self.null() else (1 + len(self.tail()))

    def __str__(self) -> str:
        """Return string representation of List."""

        return "[%s]" % ", ".join([str(x) for x in self])

    def __repr__(self) -> str:
        """Return string representation of List."""

        return str(self)

    def __eq__(self, other) -> bool:
        """Compare if List is equal to other List."""

        if self.null() or other.null():
            return True if self.null() and other.null() else False
        return self.head() == other.head() and self.tail() == other.tail()


assert(isinstance(List, Monoid))
assert(isinstance(List, Functor))
assert(isinstance(List, Applicative))
assert(isinstance(List, Monad))
