from abc import abstractmethod
from functools import partial, reduce

from typing import Callable, Iterator, TypeVar, Iterable, Sized, Any, cast, Union

from .typing import Applicative
from .typing import Functor
from .typing import Monoid
from .typing import Monad

TSource = TypeVar("TSource")
TResult = TypeVar("TResult")
TSelector = Callable[[TSource, 'List[TSource]'], Union[TSource, 'List[TSource]']]


class List(Iterable[TSource], Sized):
    """The list monad.

    Wraps an immutable list built from lambda expressions.
    """

    @classmethod
    def unit(cls, value: Any) -> 'List':
        """Wrap a value within the singleton list."""
        return List.empty().cons(value)

    pure = unit

    @classmethod
    def empty(cls) -> 'List[TSource]':
        """Create an empty list."""
        return Nil()

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

        return reduce(reducer, xs, Nil())

    @abstractmethod
    def head(self) -> TSource:
        raise NotImplementedError

    @abstractmethod
    def tail(self) -> 'List[TSource]':
        """Return tail of List."""
        raise NotImplementedError

    @abstractmethod
    def apply(self, something: 'List') -> 'List':
        raise NotImplementedError

    @abstractmethod
    def map(self, mapper: Callable[[TSource], TResult]) -> 'List[TResult]':
        raise NotImplementedError

    @abstractmethod
    def bind(self, fn: Callable[[TSource], 'List[TResult]']) -> 'List[TResult]':
        raise NotImplementedError

    @abstractmethod
    def cons(self, element: TSource) -> 'List[TSource]':
        raise NotImplementedError

    @abstractmethod
    def append(self, other: 'List[TSource]') -> 'List[TSource]':
        raise NotImplementedError

    @abstractmethod
    def null(self) -> bool:
        """Return True if List is empty."""
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other):
        raise NotImplementedError


class Cons(List[TSource]):
    """The list cons case monad."""

    def __init__(self, run: Callable[[TSelector], Union[TSource, List[TSource]]]) -> None:
        """Initialize List."""

        self._list = run

    def cons(self, element: TSource) -> List[TSource]:
        """Add element to front of List."""

        return Cons(lambda sel: sel(element, self))

    def head(self) -> TSource:
        """Retrive first element in List."""

        run = self._list
        return cast(TSource, run(lambda head, _: head))

    def tail(self) -> 'List[TSource]':
        """Return tail of List."""

        run = self._list
        return cast(List[TSource], run(lambda _, tail: tail))

    def null(self) -> bool:
        """Return True if List is empty."""
        return False

    def map(self, mapper: Callable[[TSource], TResult]) -> List[TResult]:
        """Map a function over a List."""
        return (self.tail().map(mapper)).cons(mapper(self.head()))

    def apply(self, something: 'List') -> 'List':
        # fs <*> xs = [f x | f <- fs, x <- xs]
        try:
            xs = [f(x) for f in self for x in something]
        except TypeError:
            xs = [partial(f, x) for f in self for x in something]

        return List.from_iterable(xs)

    def append(self, other: List[TSource]) -> List[TSource]:
        """Append other list to this list."""

        return (self.tail().append(other)).cons(self.head())

    def bind(self, fn: Callable[[TSource], List[TResult]]) -> List[TResult]:
        """Flatten and map the List.

        Haskell: xs >>= f = concat (map f xs)
        """
        return List.concat(self.map(fn))

    def __iter__(self) -> Iterator:
        """Return iterator for List."""

        yield self.head()
        yield from self.tail()

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

        return 1 + len(self.tail())

    def __str__(self) -> str:
        """Return string representation of List."""

        return "[%s]" % ", ".join([str(x) for x in self])

    def __repr__(self) -> str:
        """Return string representation of List."""

        return str(self)

    def __eq__(self, other) -> bool:
        """Compare if List is equal to other List."""

        if isinstance(other, Nil):
            return False
        return self.head() == other.head() and self.tail() == other.tail()


class Nil(List[TSource]):
    def __init__(self) -> None:
        """Initialize List."""
        pass

    def cons(self, element: TSource) -> 'List[TSource]':
        """Add element to front of List."""

        return Cons(lambda sel: sel(element, Nil()))

    def head(self) -> TSource:
        """Retrive first element in List."""

        raise IndexError("List is empty")

    def tail(self) -> 'List[TSource]':
        """Return tail of List."""

        raise IndexError("List is empty")

    def null(self) -> bool:
        """Return True if List is empty."""
        return True

    def map(self, mapper: Callable[[TSource], TResult]) -> List[TResult]:
        """Map a function over a List."""
        return Nil()

    def apply(self, something: 'List') -> 'List':
        # fs <*> xs = [f x | f <- fs, x <- xs]
        try:
            xs = [f(x) for f in self for x in something]
        except TypeError:
            xs = [partial(f, x) for f in self for x in something]

        return List.from_iterable(xs)

    def append(self, other: List[TSource]) -> List[TSource]:
        """Append other list to this list."""

        if self.null():
            return other
        return (self.tail().append(other)).cons(self.head())

    def bind(self, fn: Callable[[TSource], List[TResult]]) -> List[TResult]:
        """Flatten and map the List.

        Haskell: xs >>= f = concat (map f xs)
        """
        return List.concat(self.map(fn))

    def __iter__(self) -> Iterator:
        """Return iterator for List."""

        while False:
            yield

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

        return 0

    def __str__(self) -> str:
        """Return string representation of List."""

        return "[%s]" % ", ".join([str(x) for x in self])

    def __repr__(self) -> str:
        """Return string representation of List."""

        return str(self)

    def __eq__(self, other) -> bool:
        """Compare if List is equal to other List."""

        return True if isinstance(other, Nil) else False


assert(isinstance(List, Monoid))
assert(isinstance(List, Functor))
assert(isinstance(List, Applicative))
assert(isinstance(List, Monad))

assert(isinstance(Cons, Monoid))
assert(isinstance(Cons, Functor))
assert(isinstance(Cons, Applicative))
assert(isinstance(Cons, Monad))

assert(isinstance(Nil, Monoid))
assert(isinstance(Nil, Functor))
assert(isinstance(Nil, Applicative))
assert(isinstance(Nil, Monad))
