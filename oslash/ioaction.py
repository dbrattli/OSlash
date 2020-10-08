"""Implementation of IO Actions."""

from abc import abstractmethod
from typing import Any, Callable, Generic, TypeVar, Tuple

from .typing import Functor
from .typing import Monad
from .util import indent as ind, Unit

TSource = TypeVar("TSource")
TResult = TypeVar("TResult")


class IO(Generic[TSource]):
    """A container for a world remaking function.

    IO Actions specify something that can be done. They are not active
    in and of themselves. They need to be "run" to make something
    happen. Simply having an action lying around doesn't make anything
    happen.
    """

    @classmethod
    def unit(cls, value: TSource):
        return Return(value)

    @abstractmethod
    def bind(self, func: Callable[[TSource], "IO[TResult]"]) -> "IO[TResult]":
        """IO a -> (a -> IO b) -> IO b."""

        raise NotImplementedError

    @abstractmethod
    def map(self, func: Callable[[TSource], TResult]) -> "IO[TResult]":
        raise NotImplementedError

    @abstractmethod
    def run(self, world: int) -> TSource:
        """Run IO action."""
        raise NotImplementedError

    def __or__(self, func):
        """Use | as operator for bind.

        Provide the | operator instead of the Haskell >>= operator
        """
        return self.bind(func)

    def __rshift__(self, next: 'IO[TResult]') -> 'IO[TResult]':
        """The "Then" operator.
        Sequentially compose two monadic actions, discarding any value
        produced by the first, like sequencing operators (such as the
        semicolon) in imperative languages.
        Haskell: (>>) :: m a -> m b -> m b
        """
        return self.bind(lambda _: next)

    def __call__(self, world: int = 0) -> Any:
        """Run io action."""
        return self.run(world)

    @abstractmethod
    def __str__(self, m: int = 0, n: int = 0) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__str__()


class Return(IO[TSource]):
    def __init__(self, value: TSource) -> None:
        """Create IO Action."""

        self._value = value

    def map(self, func: Callable[[TSource], TResult]) -> "IO[TResult]":
        return Return(func(self._value))

    def bind(self, func: Callable[[TSource], "IO[TResult]"]) -> "IO[TResult]":
        """IO a -> (a -> IO b) -> IO b."""

        return func(self._value)

    def run(self, world: int) -> TSource:
        """Run IO action."""
        return self._value

    def __str__(self, m: int = 0, n: int = 0) -> str:
        a = self._value
        return f"{ind(m)}Return {a}"


class Put(IO[TSource]):
    """The Put action.

    A container holding a string to be printed to stdout, followed by
    another IO Action.
    """

    def __init__(self, text: str, io: IO) -> None:
        self._value = text, io

    def bind(self, func: Callable[[TSource], IO[TResult]]) -> 'IO[TResult]':
        """IO a -> (a -> IO b) -> IO b"""

        text, io = self._value
        return Put(text, io.bind(func))

    def map(self, func: Callable[[TSource], TResult]) -> "IO[TResult]":
        # Put s (fmap f io)
        assert self._value is not None
        text, action = self._value
        return Put(text, action.map(func))

    def run(self, world: int) -> TSource:
        """Run IO action"""

        assert self._value is not None
        text, action = self._value
        new_world = pure_print(world, text)
        return action(world=new_world)

    def __call__(self, world: int = 0) -> TSource:
        return self.run(world)

    def __str__(self, m: int = 0, n: int = 0) -> str:
        s, io = self._value
        a = io.__str__(m + 1, n)
        return '%sPut ("%s",\n%s\n%s)' % (ind(m), s, a, ind(m))


class Get(IO[TSource]):
    """A container holding a function from string -> IO[TSource], which can
    be applied to whatever string is read from stdin.
    """

    def __init__(self, fn: Callable[[str], IO[TSource]]) -> None:
        self._fn = fn

    def bind(self, func: Callable[[TSource], IO[TResult]]) -> IO[TResult]:
        """IO a -> (a -> IO b) -> IO b"""

        g = self._fn
        return Get(lambda text: g(text).bind(func))

    def map(self, func: Callable[[TSource], TResult]) -> IO[TResult]:
        # Get (\s -> fmap f (g s))
        g = self._fn
        return Get(lambda s: g(s).map(func))

    def run(self, world: int) -> TSource:
        """Run IO Action"""

        func = self._fn
        new_world, text = pure_input(world)
        action = func(text)
        return action(world=new_world)

    def __call__(self, world: int = 0) -> TSource:
        return self.run(world)

    def __str__(self, m: int = 0, n: int = 0) -> str:
        g = self._fn
        i = "x%s" % n
        a = g(i).__str__(m + 1, n + 1)
        return "%sGet (%s => \n%s\n%s)" % (ind(m), i, a, ind(m))


class ReadFile(IO[str]):
    """A container holding a filename and a function from string -> IO[str],
    which can be applied to whatever string is read from the file.
    """

    def __init__(self, filename: str, func: Callable[[str], IO]) -> None:
        self.open_func = open
        self._value = filename, func

    def bind(self, func: Callable[[Any], IO]) -> IO:
        """IO a -> (a -> IO b) -> IO b"""

        filename, g = self._value
        return ReadFile(filename, lambda s: g(s).bind(func))

    def map(self, func: Callable[[Any], Any]) -> IO:
        # Get (\s -> fmap f (g s))
        filename, g = self._value
        return Get(lambda s: g(s).map(func))

    def run(self, world: int) -> str:
        """Run IO Action"""

        filename, func = self._value
        f = self.open_func(filename)
        action = func(f.read())
        return action(world=world + 1)

    def __call__(self, world: int = 0) -> str:
        return self.run(world)

    def __str__(self, m: int = 0, n: int = 0) -> str:
        filename, g = self._value
        i = "x%s" % n
        a = g(i).__str__(m + 2, n + 1)
        return '%sReadFile ("%s",%s => \n%s\n%s)' % (ind(m), filename, i, a, ind(m))


def get_line() -> IO[str]:
    return Get(Return)


def put_line(text: str) -> IO:
    return Put(text, Return(Unit))


def read_file(filename: str) -> IO:
    return ReadFile(filename, Return)


def pure_print(world: int, text: str) -> int:
    print(text)  # Impure. NOTE: If you see this line you need to wash your hands
    return world + 1


def pure_input(world: int) -> Tuple[int, str]:
    text = input()  # Impure. NOTE: If you see this line you need to wash your hands
    return (world + 1, text)


assert isinstance(IO, Functor)
assert isinstance(IO, Monad)

assert isinstance(Put, Functor)
assert isinstance(Put, Monad)

assert isinstance(Get, Functor)
assert isinstance(Get, Monad)

assert isinstance(ReadFile, Functor)
assert isinstance(ReadFile, Monad)
