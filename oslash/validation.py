"""Validation applicative for collecting independent errors."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast, overload

from .either import Either, Left, Right
from .list import List
from .typing import Applicative, Functor
from .util.apply import apply_callable


class Validation[T, E]:
    """A success or a nonempty list of errors.

    Unlike Either, applying two failed validations preserves both errors.
    Validation has no bind operation because dependent computations cannot
    collect errors from branches that were not run.
    """

    def __init__(self, result: Either[T, List[E]]) -> None:
        """Wrap an Either whose Left contains errors in order."""
        match result:
            case Left(errors) if errors.null():
                raise ValueError("Validation requires at least one error")
            case _:
                pass
        self._result = result

    @classmethod
    def valid(cls, value: T) -> Validation[T, E]:
        """Construct a successful validation."""
        return cls(Right(value))

    @classmethod
    def invalid(cls, error: E) -> Validation[T, E]:
        """Construct a failed validation with one error."""
        return cls(Left(List[E].unit(error)))

    @staticmethod
    def from_either[U, F](result: Either[U, F]) -> Validation[U, F]:
        """Lift an Either failure into a singleton error list."""
        match result:
            case Left(error):
                return Validation[U, F].invalid(error)
            case Right(value):
                return Validation[U, F].valid(value)
            case _:
                raise TypeError("Expected Left or Right")

    def to_either(self) -> Either[T, List[E]]:
        """Return the underlying Either with all accumulated errors."""
        return self._result

    def map[U](self, mapper: Callable[[T], U]) -> Validation[U, E]:
        """Transform a success while preserving any errors."""
        return Validation(self._result.map(mapper))

    @classmethod
    def pure(cls, value: T) -> Validation[T, E]:
        """Wrap a value in a successful validation."""
        return cls.valid(value)

    @overload
    def apply[A, B](self: Validation[Callable[[A], B], E], something: Validation[A, E]) -> Validation[B, E]: ...

    @overload
    def apply[A, B, C](
        self: Validation[Callable[[A, B], C], E], something: Validation[A, E]
    ) -> Validation[Callable[[B], C], E]: ...

    def apply(self: Validation[Callable[..., Any], E], something: Validation[Any, E]) -> Validation[Any, E]:
        """Apply a wrapped function and collect errors from both inputs."""
        match (self._result, something._result):
            case (Left(function_errors), Left(value_errors)):
                return Validation(Left(function_errors + value_errors))
            case (Left(errors), _):
                return Validation(Left(errors))
            case (_, Left(errors)):
                return Validation(Left(errors))
            case (Right(function), Right(value)):
                return Validation(Right(apply_callable(function, value)))
            case _:
                raise TypeError("Expected Left or Right")

    def __eq__(self, other: object) -> bool:
        """Compare validation results and errors."""
        if isinstance(other, Validation):
            other_validation = cast(Validation[Any, Any], other)
            return self._result == other_validation._result
        return NotImplemented

    def __repr__(self) -> str:
        """Show the wrapped Either result."""
        return f"Validation({self._result!r})"


assert isinstance(Validation, Functor)
assert isinstance(Validation, Applicative)
