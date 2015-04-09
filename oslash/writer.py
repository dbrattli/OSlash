from typing import Any, Callable, Tuple

from .abc import Functor
from .abc import Monad
from .abc import Monoid
from .util import Unit, extensionclassmethod


class Writer(Monad, Functor):

    """The writer monad."""

    def __init__(self, value: Any, log: Monoid):
        """Initialize a new writer.

        :param value Any: Value to
        """
        super().__init__()

        self._get_value = lambda: (value, log)

    def fmap(self, func: Callable[[Any], Any]) -> "Writer":
        """Map a function func over the Writer value.

        Haskell:
        fmap f m = Writer $ let (a, w) = runWriter m in (f a, w)

        Keyword arguments:
        func -- Mapper function:
        """
        value, log = self.run_writer()
        return Writer(func(value), log)

    def bind(self, func: Callable[[Any], "Writer"]) -> "Writer":
        """Flat is better than nested.

        Haskell:
        (Writer (x, v)) >>= f = let
            (Writer (y, v')) = f x in Writer (y, v `mappend` v')
        """
        a, w = self.run_writer()
        b, w_ = func(a).run_writer()
        return Writer(b, w + w_)

    def __eq__(self, other: "Writer") -> bool:
        return self.run_writer() == other.run_writer()

    def __str__(self) -> str:
        return "%s :: %s" % self.run_writer()

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def unit(cls, value: "Any") -> "Writer":
        """Wrap a single value in a Writer.

        Use the factory method to create *Writer classes that
        uses a different monoid than str, or use the constructor
        directly.
        """
        return cls(value, log="")

    def run_writer(self) -> tuple:
        """Extract value from Writer.

        This is the inverse function of the constructor and converts the
        Writer to s simple tuple.
        """
        return self._get_value()

    @staticmethod
    def apply_log(a: tuple, func: Callable[[Any], Tuple[Any, Monoid]]) -> tuple:
        """Apply a function to a value with a log.

        Helper function to apply a function to a value with a log tuple.
        """
        value, log = a
        new, entry = func(value)
        return new, log + entry


class MonadWriter(Writer):
        @classmethod
        def tell(cls, log):
            return cls(Unit, log)


@extensionclassmethod(Writer)
def factory(cls, class_name, monoid_type=str):
    """Create Writer subclass using specified monoid type.

    lets us create a Writer that uses a different monoid than str for
    the log.
    """

    def unit(cls, value):
        if hasattr(monoid_type, "mempty"):
            log = monoid_type.mempty()
        else:
            log = monoid_type()

        return cls(value, log)

    return type(class_name, (Writer,), dict(unit=classmethod(unit)))
