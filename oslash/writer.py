"""Writer monad implementation.

The Writer monad allows for computations that produce a stream of data
in addition to the computed values (e.g., logging).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .typing import Functor, Monad, Monoid


class Writer[T, Log]:
    """The writer monad.

    The Writer monad represents computations that produce a stream of
    data in addition to the computed values.
    """

    def __init__(self, value: T, log: Log) -> None:
        """Initialize a new writer.

        Args:
            value: The wrapped value
            log: The log/accumulated data
        """
        self._value: tuple[T, Log] = (value, log)

    def map[U](self, func: Callable[[tuple[T, Log]], tuple[U, Log]]) -> Writer[U, Log]:
        """Map a function func over the Writer value.

        Haskell:
        fmap f m = Writer $ let (a, w) = runWriter m in (f a, w)
        """
        a, w = self.run()
        b, w_ = func((a, w))
        return Writer(b, w_)

    def bind[U](self, func: Callable[[T], Writer[U, Log]]) -> Writer[U, Log]:
        """Flat is better than nested.

        Haskell:
        (Writer (x, v)) >>= f = let
            (Writer (y, v')) = f x in Writer (y, v `append` v')
        """
        a, w = self.run()
        b, w_ = func(a).run()
        # Log type must support addition (Monoid)
        w__: Log = w + w_  # type: ignore[operator]
        # Any: Log type is generic and determined at runtime
        return Writer(b, w__)  # type: ignore[arg-type]

    @classmethod
    def unit(cls, value: T) -> Writer[T, Log]:
        """Wrap a single value in a Writer.

        Use the factory method to create Writer classes that
        use a different monoid than str, or use the constructor
        directly.
        """
        # Log: Empty log is empty string by default
        return Writer(value, log="")  # type: ignore

    def run(self) -> tuple[T, Log]:
        """Extract value from Writer.

        This is the inverse function of the constructor and converts the
        Writer to a simple tuple.
        """
        return self._value

    @staticmethod
    def apply_log[V](a: tuple[V, Log], func: Callable[[V], tuple[T, Log]]) -> tuple[T, Log]:
        """Apply a function to a value with a log.

        Helper function to apply a function to a value with a log tuple.
        """
        value, log = a
        new, entry = func(value)
        # Log: Monoid append operation
        return new, log + entry  # type: ignore

    @classmethod
    def create(cls, class_name: str, monoid_type: type[Monoid[Log]] | type[str] = str) -> type[Writer[T, Log]]:
        """Create Writer subclass using specified monoid type.

        Lets us create a Writer that uses a different monoid than str for the log.

        Usage:
            StringWriter = Writer.create("StringWriter", str)
            IntWriter = Writer.create("IntWriter", int)
            ...
        """

        def unit(cls: type[Writer[T, Log]], value: T) -> Writer[T, Log]:
            log: Any  # Any: Dynamic monoid type determined at runtime
            if hasattr(monoid_type, "empty"):
                log = monoid_type.empty()  # type: ignore[attr-defined]
            else:
                log = monoid_type()  # type: ignore[misc]

            return cls(value, log)  # type: ignore[arg-type]

        return type(class_name, (Writer,), {"unit": classmethod(unit)})  # type: ignore

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Writer):
            return self.run() == other.run()
        return NotImplemented

    def __str__(self) -> str:
        value, log = self.run()
        return f"{value} :: {log}"

    def __repr__(self) -> str:
        return str(self)


class MonadWriter[Log](Writer[None, Log]):
    """MonadWriter provides tell operation for logging."""

    @classmethod
    def tell(cls, log: Log) -> MonadWriter[Log]:
        """Log a value without returning a result."""
        # None: tell returns no meaningful value
        return cls(None, log)  # type: ignore


# Convenience: Pre-created StringWriter
# Any: Dynamic type creation via type() cannot be statically typed
StringWriter: type[Writer[Any, str]] = Writer.create("StringWriter", str)  # type: ignore[assignment]

# Type assertions for runtime checking
assert isinstance(Writer, Functor)
assert isinstance(Writer, Monad)
