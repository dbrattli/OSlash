"""Identity monad implementation."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Self, cast, overload

from .typing import Applicative, Functor, Monad
from .util.apply import apply_callable


class Identity[T]:
    """Identity monad.

    The Identity monad is the simplest monad, which attaches no
    information to values.
    """

    def __init__(self, value: T) -> None:
        self._value = value

    @classmethod
    def unit(cls, value: T) -> Self:
        """Initialize a new identity."""
        return cls(value)

    def map[U](self, mapper: Callable[[T], U]) -> Identity[U]:
        """Map a function over wrapped values."""
        result = mapper(self._value)
        return Identity(result)

    def bind[U](self, func: Callable[[T], Identity[U]]) -> Identity[U]:
        """Bind a monadic function."""
        return func(self._value)

    @classmethod
    def pure(cls, value: T) -> Self:
        """Wrap a value in the Identity context."""
        return cls(value)

    @overload
    def apply[A, B](self: Identity[Callable[[A], B]], something: Identity[A]) -> Identity[B]: ...

    @overload
    def apply[A, B, C](self: Identity[Callable[[A, B], C]], something: Identity[A]) -> Identity[Callable[[B], C]]: ...

    def apply(self: Identity[Callable[..., Any]], something: Identity[Any]) -> Identity[Any]:
        """Apply a wrapped function, currying it when more arguments remain."""
        return something.map(lambda value: apply_callable(self._value, value))

    def run(self) -> T:
        """Extract the value from the Identity."""
        return self._value

    def __call__(self) -> T:
        """Extract the value from the Identity."""
        return self.run()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Identity):
            other_ = cast(Identity[Any], other)
            return self._value == other_._value
        return NotImplemented

    def __str__(self) -> str:
        return f"Identity({self._value})"

    def __repr__(self) -> str:
        return str(self)


assert isinstance(Identity, Functor)
assert isinstance(Identity, Applicative)
assert isinstance(Identity, Monad)
