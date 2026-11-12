"""Writer monad implementation.

The Writer monad allows for computations that produce a stream of data
in addition to the computed values (e.g., logging).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol, cast, overload

from .typing import Functor, Monad

_MISSING = object()


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

    def map[U](self, func: Callable[[T], U]) -> Writer[U, Log]:
        """Map a function func over the Writer value.

        The log is preserved, as required by Functor.map.
        """
        a, w = self.run()
        return Writer(func(a), w)

    def map_with_log[U](self, func: Callable[[tuple[T, Log]], tuple[U, Log]]) -> Writer[U, Log]:
        """Transform the value and log together."""
        return Writer(*func(self.run()))

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

    @overload
    @classmethod
    def unit[U](cls, value: U) -> Writer[U, str]: ...

    @overload
    @classmethod
    def unit[U, EmptyLog](cls, value: U, *, empty_log: EmptyLog) -> Writer[U, EmptyLog]: ...

    @classmethod
    def unit[U](cls: type[Writer[Any, Any]], value: U, *, empty_log: object = _MISSING) -> Writer[U, Any]:
        """Wrap a single value in a Writer.

        The default log is an empty string. Supply empty_log for another
        log type, or use a class created with create().
        """
        # The default writer uses string logs; other log types must supply
        # their own identity element (or use a class created with create()).
        return cls(value, cast(Any, "" if empty_log is _MISSING else empty_log))

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

    @overload
    @staticmethod
    def create(class_name: str) -> WriterFactory[str]: ...

    @overload
    @staticmethod
    def create[FactoryLog](class_name: str, monoid_type: type[FactoryLog]) -> WriterFactory[FactoryLog]: ...

    @staticmethod
    def create(class_name: str, monoid_type: type[Any] = str) -> WriterFactory[Any]:
        """Create a Writer class with a configured log identity.

        The factory's unit(value) uses monoid_type.empty() when available,
        otherwise monoid_type(). Use Writer.unit for an explicit empty_log.
        """

        def unit[U](cls: type[Writer[Any, Any]], value: U) -> Writer[U, Any]:
            log: Any  # Dynamic monoid identity construction.
            if hasattr(monoid_type, "empty"):
                log = monoid_type.empty()
            else:
                log = monoid_type()
            return cls(value, log)

        return cast(WriterFactory[Any], type(class_name, (Writer,), {"unit": classmethod(unit)}))

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


class WriterFactory[Log](Protocol):
    """Callable interface of a dynamically created Writer class.

    A factory fixes the log type, while each call infers its own value type.
    Instances are annotated as Writer[T, Log], not with the factory name.
    """

    def __call__[T](self, value: T, log: Log) -> Writer[T, Log]: ...

    def unit[T](self, value: T) -> Writer[T, Log]: ...


StringWriter: WriterFactory[str] = Writer.create("StringWriter", str)

# Type assertions for runtime checking
assert isinstance(Writer, Functor)
assert isinstance(Writer, Monad)
