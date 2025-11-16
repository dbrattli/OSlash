"""Maybe monad implementation.

The Maybe type encapsulates an optional value, providing a type-safe way
to handle null/None values without exceptions.
"""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from functools import partial, reduce
from typing import Any, Self, cast

from .typing import Applicative, Functor, Monad, Monoid


class Maybe[T]:
    """Encapsulates an optional value.

    The Maybe type encapsulates an optional value. A value of type
    Maybe a either contains a value of (represented as Just a), or it is
    empty (represented as Nothing). Using Maybe is a good way to deal
    with errors or exceptional cases without resorting to drastic
    measures such as error.
    """

    @classmethod
    def empty(cls) -> Maybe[T]:
        """Return the empty Maybe (Nothing)."""
        return Nothing()

    @abstractmethod
    def __add__(self, other: Maybe[T]) -> Maybe[T]:
        """Monoid append operation."""
        raise NotImplementedError

    @abstractmethod
    def map[U](self, mapper: Callable[[T], U]) -> Maybe[U]:
        """Functor map operation."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def pure(cls, value: T) -> Self:
        """Applicative pure operation."""
        raise NotImplementedError

    @abstractmethod
    def apply[U](self: Maybe[Callable[[T], U]], something: Maybe[T]) -> Maybe[U]:
        """Applicative apply operation."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def unit(cls, value: T) -> Self:
        """Monad unit operation."""
        raise NotImplementedError

    @abstractmethod
    def bind[U](self, fn: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """Monad bind operation."""
        raise NotImplementedError

    @classmethod
    def concat(cls, xs: list[Maybe[T]]) -> Maybe[T]:
        """mconcat :: [m] -> m

        Fold a list using the monoid. For most types, the default
        definition for mconcat will be used, but the function is
        included in the class definition so that an optimized version
        can be provided for specific types.
        """

        def reducer(a: Maybe[T], b: Maybe[T]) -> Maybe[T]:
            return a + b

        return reduce(reducer, xs, cls.empty())

    def __rmod__[U](self, fn: Callable[[T], U]) -> Maybe[U]:
        """Infix version of map.

        Haskell: <$>

        Example:
        >>> (lambda x: x+2) % Just(40)
        Just 42

        Returns a new Functor.
        """
        return self.map(fn)


class Just[T](Maybe[T]):
    """A Maybe that contains a value.

    Represents a Maybe that contains a value (represented as Just a).
    """

    __match_args__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    # Monoid Section
    # ==============

    def __add__(self, other: Maybe[T]) -> Maybe[T]:
        """Monoid append for Just.

        m `append` Nothing = m
        Just m1 `append` Just m2 = Just (m1 `append` m2)
        """
        match other:
            case Nothing():
                return self
            case Just(other_value):
                # If the wrapped value supports addition, add them
                if hasattr(self._value, "__add__"):
                    return Just(self._value + other_value)  # type: ignore
                return self
            case _:
                return self

    # Functor Section
    # ===============

    def map[U](self, mapper: Callable[[T], U]) -> Maybe[U]:
        """fmap f (Just x) = Just (f x)"""
        result = mapper(self._value)
        return Just(result)

    # Applicative Section
    # ===================

    @classmethod
    def pure[U](cls, value: U) -> Just[U]:
        """Wrap a value in Just."""
        return Just[U](value)

    def apply[U](self: Just[Callable[[T], U]], something: Maybe[T]) -> Maybe[U]:
        """Apply a wrapped function to a wrapped value."""

        def mapper(other_value: T) -> U:
            try:
                return self._value(other_value)
            except TypeError:
                # Partial application for curried functions
                return partial(self._value, other_value)  # type: ignore

        return something.map(mapper)

    # Monad Section
    # =============

    @classmethod
    def unit(cls, value: T) -> Just[T]:
        """Wrap a value in Just."""
        return cls(value)

    def bind[U](self, fn: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """Just x >>= f = f x."""
        return fn(self._value)

    # Utilities Section
    # =================

    def is_just(self) -> bool:
        """Check if this is a Just value."""
        return True

    def is_nothing(self) -> bool:
        """Check if this is Nothing."""
        return False

    # Operator Overloads Section
    # ==========================

    def __bool__(self) -> bool:
        """Convert Just to bool."""
        return bool(self._value)

    def __eq__(self, other: object) -> bool:
        """Return self == other."""
        match other:
            case Nothing():
                return False
            case Just():
                # Cast: Pattern matching narrows other to Just[T]
                other_just: Just[Any] = cast(Just[Any], other)
                return self._value == other_just._value
            case _:
                return NotImplemented

    def __str__(self) -> str:
        return f"Just {self._value}"

    def __repr__(self) -> str:
        return str(self)


class Nothing[T](Maybe[T]):
    """Represents an empty Maybe.

    Represents an empty Maybe that holds nothing (in which case it has
    the value of Nothing).
    """

    __match_args__ = ()

    # Monoid Section
    # ==============

    def __add__(self, other: Maybe[T]) -> Maybe[T]:
        """Nothing `append` m = m"""
        return other

    # Functor Section
    # ===============

    def map[U](self, mapper: Callable[[T], U]) -> Maybe[U]:
        """fmap f Nothing = Nothing"""
        return Nothing()

    # Applicative Section
    # ===================

    @classmethod
    def pure(cls, value: T) -> Nothing[T]:
        """Nothing cannot be pure, returns Nothing."""
        return cls()

    def apply[U](self: Nothing[Callable[[T], U]], something: Maybe[T]) -> Maybe[U]:
        """Nothing <*> _ = Nothing"""
        return Nothing()

    # Monad Section
    # =============

    @classmethod
    def unit(cls, value: T) -> Nothing[T]:
        """Nothing unit returns Nothing."""
        return cls()

    def bind[U](self, fn: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """Nothing >>= f = Nothing

        Nothing in, Nothing out.
        """
        return Nothing()

    # Utilities Section
    # =================

    def is_just(self) -> bool:
        """Check if this is a Just value."""
        return False

    def is_nothing(self) -> bool:
        """Check if this is Nothing."""
        return True

    # Operator Overloads Section
    # ==========================

    def __eq__(self, other: object) -> bool:
        """Nothing equals Nothing."""
        match other:
            case Nothing():
                return True
            case _:
                return False

    def __str__(self) -> str:
        return "Nothing"

    def __repr__(self) -> str:
        return str(self)


# Type assertions for runtime checking
assert issubclass(Just, Maybe)
assert issubclass(Nothing, Maybe)

assert isinstance(Maybe, Monoid)
assert isinstance(Maybe, Functor)
assert isinstance(Maybe, Applicative)
assert isinstance(Maybe, Monad)

assert isinstance(Just, Monoid)
assert isinstance(Just, Functor)
assert isinstance(Just, Applicative)
assert isinstance(Just, Monad)

assert isinstance(Nothing, Monoid)
assert isinstance(Nothing, Functor)
assert isinstance(Nothing, Applicative)
assert isinstance(Nothing, Monad)
