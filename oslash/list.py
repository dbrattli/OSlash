"""List monad implementation.

An immutable list implementation using lambda expressions, providing
a functional programming approach to list operations.
"""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable, Iterable, Iterator, Sized
from functools import partial, reduce
from typing import Any, cast

from .typing import Applicative, Functor, Monad, Monoid

# Type alias for list selector function
# Any: Selector function type varies by usage and cannot be
# statically determined without higher-kinded types
type ListSelector[T] = Callable[[T, List[T]], T | List[T]]


class List[T](Iterable[T], Sized):
    """The list monad.

    Wraps an immutable list built from lambda expressions.

    Can be instantiated directly with an iterable:
        >>> List([1, 2, 3])
        [1, 2, 3]
        >>> List()
        []
    """

    def __new__(cls, iterable: Iterable[T] | None = None) -> List[T]:
        """Create a new List from an iterable.

        Args:
            iterable: Optional iterable to create list from. If None, returns empty list.

        Returns:
            A new List instance (either Cons or Nil).
        """
        # Only handle factory creation when called on List itself, not subclasses
        if cls is List:
            if iterable is None:
                # type: ignore here is safe - Nil() returns List[T] at runtime
                return Nil()  # type: ignore[return-value]
            # type: ignore here is safe - from_iterable returns properly typed List[T]
            return cls.from_iterable(iterable)  # type: ignore[return-value]

        # For subclasses (Cons, Nil), use normal object construction
        return object.__new__(cls)

    @classmethod
    def unit(cls, value: T) -> List[T]:
        """Wrap a value within the singleton list."""
        return cls.empty().cons(value)

    pure = unit

    @classmethod
    def empty(cls) -> List[T]:
        """Create an empty list."""
        return Nil()

    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> List[T]:
        """Create list from iterable."""
        iterator = iter(iterable)

        def recurse() -> List[T]:
            try:
                value = next(iterator)
            except StopIteration:
                return cls.empty()
            return cls.unit(value).append(recurse())

        return cls.empty().append(recurse())

    @classmethod
    def concat(cls, xs: Iterable[List[T]]) -> List[T]:
        """mconcat :: [m] -> m

        Fold a list using the monoid. For most types, the default
        definition for mconcat will be used, but the function is
        included in the class definition so that an optimized version
        can be provided for specific types.
        """

        def reducer(a: List[T], b: List[T]) -> List[T]:
            return a + b

        return reduce(reducer, xs, Nil())

    @abstractmethod
    def head(self) -> T:
        """Return the first element of the List."""
        raise NotImplementedError

    @abstractmethod
    def tail(self) -> List[T]:
        """Return tail of List."""
        raise NotImplementedError

    @abstractmethod
    def apply[U](self: List[Callable[[T], U]], something: List[T]) -> List[U]:
        """Applicative apply operation."""
        raise NotImplementedError

    @abstractmethod
    def map[U](self, mapper: Callable[[T], U]) -> List[U]:
        """Functor map operation."""
        raise NotImplementedError

    @abstractmethod
    def bind[U](self, fn: Callable[[T], List[U]]) -> List[U]:
        """Monad bind operation."""
        raise NotImplementedError

    @abstractmethod
    def cons(self, element: T) -> List[T]:
        """Add element to front of List."""
        raise NotImplementedError

    @abstractmethod
    def append(self, other: List[T]) -> List[T]:
        """Append other list to this list."""
        raise NotImplementedError

    @abstractmethod
    def null(self) -> bool:
        """Return True if List is empty."""
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other: List[T]) -> List[T]:
        """Monoid append operation."""
        raise NotImplementedError


class Cons[T](List[T]):
    """The list cons case monad."""

    __match_args__ = ("_list",)

    def __new__(cls, run: Callable[[ListSelector[T]], T | List[T]] | None = None) -> Cons[T]:  # type: ignore[misc]
        """Create new Cons instance.

        Args:
            run: Selector function for list operations.

        Returns:
            A new Cons instance.
        """
        return object.__new__(cls)

    def __init__(self, run: Callable[[ListSelector[T]], T | List[T]] | None = None) -> None:
        """Initialize List with a selector function.

        Args:
            run: Selector function, or None if constructed via List() factory.
        """
        # If _list already exists, we were created by List() factory via __new__
        # Don't overwrite it
        if not hasattr(self, "_list") and run is not None:
            self._list = run

    def cons(self, element: T) -> List[T]:
        """Add element to front of List."""
        return Cons(lambda sel: sel(element, self))

    def head(self) -> T:
        """Retrieve first element in List."""
        run = self._list
        result: T | List[T] = run(lambda head, _: head)
        # Cast: Selector function returns head which is always T
        return cast(T, result)

    def tail(self) -> List[T]:
        """Return tail of List."""
        run = self._list
        result: T | List[T] = run(lambda _, tail: tail)
        # Cast: Selector function returns tail which is always List[T]
        return cast(List[T], result)

    def null(self) -> bool:
        """Return True if List is empty."""
        return False

    def map[U](self, mapper: Callable[[T], U]) -> List[U]:
        """Map a function over a List."""
        return self.tail().map(mapper).cons(mapper(self.head()))

    def apply[U](self: Cons[Callable[[T], U]], something: List[T]) -> List[U]:
        """Apply wrapped functions to wrapped values.

        Haskell: fs <*> xs = [f x | f <- fs, x <- xs]
        """
        try:
            xs = [f(x) for f in self for x in something]
        except TypeError:
            # Partial application for curried functions
            xs = [partial(f, x) for f in self for x in something]  # type: ignore

        return List.from_iterable(xs)  # type: ignore[return-value]

    def append(self, other: List[T]) -> List[T]:
        """Append other list to this list."""
        return self.tail().append(other).cons(self.head())

    def bind[U](self, fn: Callable[[T], List[U]]) -> List[U]:
        """Flatten and map the List.

        Haskell: xs >>= f = concat (map f xs)
        """
        return List.concat(self.map(fn))  # type: ignore[arg-type]

    def __iter__(self) -> Iterator[T]:
        """Return iterator for List."""
        yield self.head()
        yield from self.tail()

    def __rmod__[U](self, fn: Callable[[T], U]) -> List[U]:
        """Infix version of map.

        Haskell: <$>

        Example:
        >>> (lambda x: x+2) % List.from_iterable([1, 2, 3])
        [3, 4, 5]

        Returns a new Functor.
        """
        return self.map(fn)

    def __or__[U](self, func: Callable[[T], List[U]]) -> List[U]:
        """Use | as operator for bind.

        Provide the | operator instead of the Haskell >>= operator
        """
        return self.bind(func)

    def __rshift__[U](self, next: List[U]) -> List[U]:
        """The "Then" operator.

        Sequentially compose two monadic actions, discarding any value
        produced by the first, like sequencing operators (such as the
        semicolon) in imperative languages.

        Haskell: (>>) :: m a -> m b -> m b
        """
        return self.bind(lambda _: next)

    def __add__(self, other: List[T]) -> List[T]:
        """Monoid append."""
        return self.append(other)

    def __len__(self) -> int:
        """Return length of List."""
        return 1 + len(self.tail())

    def __str__(self) -> str:
        """Return string representation of List."""
        return "[{}]".format(", ".join([str(x) for x in self]))

    def __repr__(self) -> str:
        """Return string representation of List."""
        return str(self)

    def __eq__(self, other: object) -> bool:
        """Compare if List is equal to other List."""
        match other:
            case Nil():
                return False
            case Cons():
                # Cast: Pattern matching narrows other to Cons[T]
                other_cons: Cons[Any] = cast(Cons[Any], other)
                return self.head() == other_cons.head() and self.tail() == other_cons.tail()
            case _:
                return NotImplemented


class Nil[T](List[T]):
    """The empty list."""

    __match_args__ = ()

    def __new__(cls, _: None = None) -> Nil[T]:  # type: ignore[misc]
        """Create new Nil instance.

        Args:
            _: Ignored parameter for consistency.

        Returns:
            A new Nil instance.
        """
        return object.__new__(cls)

    def __init__(self, _: None = None) -> None:
        """Initialize empty List.

        Args:
            _: Ignored argument to handle List() factory calls.
        """

    def cons(self, element: T) -> List[T]:
        """Add element to front of List."""
        return Cons(lambda sel: sel(element, Nil()))

    def head(self) -> T:
        """Retrieve first element in List."""
        raise IndexError("List is empty")

    def tail(self) -> List[T]:
        """Return tail of List."""
        raise IndexError("List is empty")

    def null(self) -> bool:
        """Return True if List is empty."""
        return True

    def map[U](self, mapper: Callable[[T], U]) -> List[U]:
        """Map a function over an empty List."""
        return Nil()

    def apply[U](self: Nil[Callable[[T], U]], something: List[T]) -> List[U]:
        """Apply empty list of functions."""
        # fs <*> xs = [f x | f <- fs, x <- xs]
        # Empty list produces empty result
        return Nil()

    def append(self, other: List[T]) -> List[T]:
        """Append other list to this empty list."""
        return other

    def bind[U](self, fn: Callable[[T], List[U]]) -> List[U]:
        """Flatten and map the empty List."""
        return Nil()

    def __iter__(self) -> Iterator[T]:
        """Return iterator for empty List."""
        return iter([])

    def __rmod__[U](self, fn: Callable[[T], U]) -> List[U]:
        """Infix version of map for empty list.

        Haskell: <$>

        Returns an empty list.
        """
        return self.map(fn)

    def __or__[U](self, func: Callable[[T], List[U]]) -> List[U]:
        """Use | as operator for bind."""
        return self.bind(func)

    def __rshift__[U](self, next: List[U]) -> List[U]:
        """The "Then" operator for empty list."""
        return self.bind(lambda _: next)

    def __add__(self, other: List[T]) -> List[T]:
        """Monoid append for empty list."""
        return other

    def __len__(self) -> int:
        """Return length of empty List."""
        return 0

    def __str__(self) -> str:
        """Return string representation of empty List."""
        return "[]"

    def __repr__(self) -> str:
        """Return string representation of empty List."""
        return str(self)

    def __eq__(self, other: object) -> bool:
        """Compare if List is equal to other List."""
        match other:
            case Nil():
                return True
            case _:
                return False


# Type assertions for runtime checking
assert isinstance(List, Monoid)
assert isinstance(List, Functor)
assert isinstance(List, Applicative)
assert isinstance(List, Monad)

assert isinstance(Cons, Monoid)
assert isinstance(Cons, Functor)
assert isinstance(Cons, Applicative)
assert isinstance(Cons, Monad)

assert isinstance(Nil, Monoid)
assert isinstance(Nil, Functor)
assert isinstance(Nil, Applicative)
assert isinstance(Nil, Monad)
