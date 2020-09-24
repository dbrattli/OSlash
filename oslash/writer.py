from typing import Callable, Tuple, Any, TypeVar, Generic, Union, cast

from .typing import Functor
from .typing import Monad
from .typing import Monoid

TLog = TypeVar("TLog", str, Monoid)
TSource = TypeVar("TSource")
TResult = TypeVar("TResult")


class Writer(Generic[TSource, TLog]):
    """The writer monad."""

    def __init__(self, value: TSource, log: TLog) -> None:
        """Initialize a new writer.

        value Value to
        """

        self._value: Tuple[TSource, TLog] = (value, log)

    def map(self, func: Callable[[Tuple[TSource, TLog]], Tuple[TResult, TLog]]) -> 'Writer[TResult, TLog]':
        """Map a function func over the Writer value.

        Haskell:
        fmap f m = Writer $ let (a, w) = runWriter m in (f a, w)

        Keyword arguments:
        func -- Mapper function:
        """
        a, w = self.run()
        b, _w = func((a, w))
        return Writer(b, _w)

    def bind(self, func: Callable[[TSource], 'Writer[TResult, TLog]']) -> 'Writer[TResult, TLog]':
        """Flat is better than nested.

        Haskell:
        (Writer (x, v)) >>= f = let
            (Writer (y, v')) = f x in Writer (y, v `append` v')
        """
        a, w = self.run()
        b, w_ = func(a).run()

        w__ = w + w_

        return Writer(b, w__)

    @classmethod
    def unit(cls, value: TSource) -> 'Writer[TSource, TLog]':
        """Wrap a single value in a Writer.

        Use the factory method to create *Writer classes that
        uses a different monoid than str, or use the constructor
        directly.
        """
        return Writer(value, log=cast(TLog, ""))

    def run(self) -> Tuple[TSource, TLog]:
        """Extract value from Writer.

        This is the inverse function of the constructor and converts the
        Writer to s simple tuple.
        """
        return self._value

    @staticmethod
    def apply_log(a: tuple, func: Callable[[Any], Tuple[TSource, TLog]]) -> Tuple[TSource, TLog]:
        """Apply a function to a value with a log.

        Helper function to apply a function to a value with a log tuple.
        """
        value, log = a
        new, entry = func(value)
        return new, log + entry

    @classmethod
    def create(cls, class_name: str, monoid_type=Union[Monoid, str]):
        """Create Writer subclass using specified monoid type. lets us
        create a Writer that uses a different monoid than str for the
        log.

        Usage:
            StringWriter = Writer.create("StringWriter", str)
            IntWriter = Writer.create("IntWriter", int)
            ...
        """

        def unit(cls, value):
            if hasattr(monoid_type, "empty"):
                log = monoid_type.empty()
            else:
                log = monoid_type()

            return cls(value, log)

        return type(class_name, (Writer, ), dict(unit=classmethod(unit)))

    def __eq__(self, other) -> bool:
        return self.run() == other.run()

    def __str__(self) -> str:
        return "%s :: %s" % self.run()

    def __repr__(self) -> str:
        return str(self)


class MonadWriter(Writer[Any, TLog]):

    @classmethod
    def tell(cls, log: TLog) -> 'MonadWriter':
        return cls(None, log)


StringWriter = Writer.create("StringWriter", str)


assert(isinstance(Writer, Functor))
assert(isinstance(Writer, Monad))
