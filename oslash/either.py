"""Either monad implementation.

The Either type represents values with two possibilities: a value of type
Either a b is either Left a or Right b. The Either type is sometimes used
to represent a value which is either correct or an error.
"""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from functools import partial
from typing import Any, Self, cast

from oslash.typing import Applicative, Functor, Monad


class Either[T, E]:
    """The Either Monad.

    Represents either a successful computation, or a computation that
    has failed.
    """

    @abstractmethod
    def map[U](self, mapper: Callable[[T], U]) -> Either[U, E]:
        """Functor map operation."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def pure(cls, value: T) -> Self:
        """Applicative pure operation."""
        raise NotImplementedError

    @abstractmethod
    def apply[U](self: Either[Callable[[T], U], E], something: Either[T, E]) -> Either[U, E]:
        """Applicative apply operation."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def unit(cls, value: T) -> Right[T, E]:
        """Monad unit operation."""
        raise NotImplementedError

    @abstractmethod
    def bind[U](self, func: Callable[[T], Either[U, E]]) -> Either[U, E]:
        """Monad bind operation."""
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        raise NotImplementedError


class Right[T, E](Either[T, E]):
    """Represents a successful computation."""

    __match_args__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    # Functor Section
    # ===============

    def map[U](self, mapper: Callable[[T], U]) -> Either[U, E]:
        """Map a function over the Right value."""
        result = mapper(self._value)
        return Right(result)

    # Applicative Section
    # ===================

    @classmethod
    def pure(cls, value: T) -> Right[T, E]:
        """Wrap a value in Right."""
        return cls(value)

    def apply[U](self: Right[Callable[[T], U], E], something: Either[T, E]) -> Either[U, E]:
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
    def unit(cls, value: T) -> Right[T, E]:
        """Wrap a value in Right."""
        return cls(value)

    def bind[U](self, func: Callable[[T], Either[U, E]]) -> Either[U, E]:
        """Bind a monadic function."""
        return func(self._value)

    # Operator Overloads
    # ==================

    def __eq__(self, other: object) -> bool:
        """Check equality with another Either."""
        match other:
            case Right():
                # Cast: Pattern matching narrows other to Right[T, E]
                other_right: Right[Any, Any] = cast(Right[Any, Any], other)
                return self._value == other_right._value  # type: ignore[comparison-overlap]
            case Left():
                return False
            case _:
                return NotImplemented

    def __str__(self) -> str:
        return f"Right {self._value}"

    def __repr__(self) -> str:
        return f"Right({self._value!r})"


class Left[T, E](Either[T, E]):
    """Represents a computation that has failed."""

    __match_args__ = ("_error",)

    def __init__(self, error: E) -> None:
        self._error = error

    # Functor Section
    # ===============

    def map[U](self, mapper: Callable[[T], U]) -> Either[U, E]:
        """Left values are not mapped."""
        return Left(self._error)

    # Applicative Section
    # ===================

    @classmethod
    def pure(cls, value: T) -> Either[T, E]:
        """Left cannot be pure, returns Right."""
        return Right(value)

    def apply[U](self: Left[Callable[[T], U], E], something: Either[T, E]) -> Either[U, E]:
        """Left values cannot apply."""
        return Left(self._error)

    # Monad Section
    # =============

    @classmethod
    def unit(cls, value: T) -> Right[T, E]:
        """Left unit returns Right."""
        return Right(value)

    def bind[U](self, func: Callable[[T], Either[U, E]]) -> Either[U, E]:
        """Left values are not bound."""
        return Left(self._error)

    # Operator Overloads
    # ==================

    def __eq__(self, other: object) -> bool:
        """Check equality with another Either."""
        match other:
            case Left():
                # Cast: Pattern matching narrows other to Left[T, E]
                other_left: Left[Any, Any] = cast(Left[Any, Any], other)
                return self._error == other_left._error  # type: ignore[comparison-overlap]
            case Right():
                return False
            case _:
                return NotImplemented

    def __str__(self) -> str:
        return f"Left: {self._error}"

    def __repr__(self) -> str:
        return f"Left({self._error!r})"


# Type assertions for runtime checking
assert isinstance(Either, Functor)
assert isinstance(Either, Applicative)
assert isinstance(Either, Monad)

assert isinstance(Right, Functor)
assert isinstance(Right, Applicative)
assert isinstance(Right, Monad)

assert isinstance(Left, Functor)
assert isinstance(Left, Applicative)
assert isinstance(Left, Monad)
