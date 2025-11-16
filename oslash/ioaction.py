"""Implementation of IO Actions.

IO Actions represent computations that interact with the outside world
while maintaining functional purity through the IO monad.
"""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable

from .typing import Functor, Monad
from .util import Unit
from .util import indent as ind


class IO[T]:
    """A container for a world remaking function.

    IO Actions specify something that can be done. They are not active
    in and of themselves. They need to be "run" to make something
    happen. Simply having an action lying around doesn't make anything
    happen.
    """

    @classmethod
    def unit(cls, value: T) -> IO[T]:
        """Wrap a value in an IO action."""
        return Return(value)

    @abstractmethod
    def bind[U](self, func: Callable[[T], IO[U]]) -> IO[U]:
        """IO a -> (a -> IO b) -> IO b."""
        raise NotImplementedError

    @abstractmethod
    def map[U](self, func: Callable[[T], U]) -> IO[U]:
        """Map a function over an IO action."""
        raise NotImplementedError

    @abstractmethod
    def run(self, world: int) -> T:
        """Run IO action."""
        raise NotImplementedError

    def __or__[U](self, func: Callable[[T], IO[U]]) -> IO[U]:
        """Use | as operator for bind.

        Provide the | operator instead of the Haskell >>= operator
        """
        return self.bind(func)

    def __rshift__[U](self, next: IO[U]) -> IO[U]:
        """The "Then" operator.

        Sequentially compose two monadic actions, discarding any value
        produced by the first, like sequencing operators (such as the
        semicolon) in imperative languages.

        Haskell: (>>) :: m a -> m b -> m b
        """
        return self.bind(lambda _: next)

    def __call__(self, world: int = 0) -> T:
        """Run io action."""
        return self.run(world)

    @abstractmethod
    def __str__(self, m: int = 0, n: int = 0) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__str__()


class Return[T](IO[T]):
    """Return value wrapped in IO."""

    def __init__(self, value: T) -> None:
        """Create IO Action."""
        self._value = value

    def map[U](self, func: Callable[[T], U]) -> IO[U]:
        """Map function over returned value."""
        return Return(func(self._value))

    def bind[U](self, func: Callable[[T], IO[U]]) -> IO[U]:
        """IO a -> (a -> IO b) -> IO b."""
        return func(self._value)

    def run(self, world: int) -> T:
        """Run IO action."""
        return self._value

    def __str__(self, m: int = 0, n: int = 0) -> str:
        return f"{ind(m)}Return {self._value}"


class Put[T](IO[T]):
    """The Put action.

    A container holding a string to be printed to stdout, followed by
    another IO Action.
    """

    def __init__(self, text: str, io: IO[T]) -> None:
        self._value: tuple[str, IO[T]] = (text, io)

    def bind[U](self, func: Callable[[T], IO[U]]) -> IO[U]:
        """IO a -> (a -> IO b) -> IO b"""
        text, io = self._value
        return Put(text, io.bind(func))

    def map[U](self, func: Callable[[T], U]) -> IO[U]:
        """Put s (fmap f io)"""
        text, action = self._value
        return Put(text, action.map(func))

    def run(self, world: int) -> T:
        """Run IO action"""
        text, action = self._value
        new_world = pure_print(world, text)
        return action(world=new_world)

    def __call__(self, world: int = 0) -> T:
        return self.run(world)

    def __str__(self, m: int = 0, n: int = 0) -> str:
        s, io = self._value
        a = io.__str__(m + 1, n)
        return f'{ind(m)}Put ("{s}",\n{a}\n{ind(m)})'


class Get[T](IO[T]):
    """A container holding a function from string -> IO[T], which can
    be applied to whatever string is read from stdin.
    """

    def __init__(self, fn: Callable[[str], IO[T]]) -> None:
        self._fn = fn

    def bind[U](self, func: Callable[[T], IO[U]]) -> IO[U]:
        """IO a -> (a -> IO b) -> IO b"""
        g = self._fn
        return Get(lambda text: g(text).bind(func))

    def map[U](self, func: Callable[[T], U]) -> IO[U]:
        r"""Get (\s -> fmap f (g s))"""
        g = self._fn
        return Get(lambda s: g(s).map(func))

    def run(self, world: int) -> T:
        """Run IO Action"""
        func = self._fn
        new_world, text = pure_input(world)
        action = func(text)
        return action(world=new_world)

    def __call__(self, world: int = 0) -> T:
        return self.run(world)

    def __str__(self, m: int = 0, n: int = 0) -> str:
        g = self._fn
        i = f"x{n}"
        a = g(i).__str__(m + 1, n + 1)
        return f"{ind(m)}Get ({i} => \n{a}\n{ind(m)})"


class ReadFile(IO[str]):
    """A container holding a filename and a function from string -> IO[str],
    which can be applied to whatever string is read from the file.
    """

    def __init__(self, filename: str, func: Callable[[str], IO[str]]) -> None:
        self.open_func = open
        self._value: tuple[str, Callable[[str], IO[str]]] = (filename, func)

    def bind[U](self, func: Callable[[str], IO[U]]) -> IO[U]:
        """IO a -> (a -> IO b) -> IO b"""
        filename, g = self._value
        # IO: Flexible IO type for file reading
        return ReadFile(filename, lambda s: g(s).bind(func))  # type: ignore

    def map[U](self, func: Callable[[str], U]) -> IO[U]:
        r"""Get (\s -> fmap f (g s))"""
        _, g = self._value
        # IO: Flexible IO type for file reading
        return Get(lambda s: g(s).map(func))  # type: ignore

    def run(self, world: int) -> str:
        """Run IO Action"""
        filename, func = self._value
        with self.open_func(filename) as f:
            action = func(f.read())
        return action(world=world + 1)

    def __call__(self, world: int = 0) -> str:
        return self.run(world)

    def __str__(self, m: int = 0, n: int = 0) -> str:
        filename, g = self._value
        i = f"x{n}"
        a = g(i).__str__(m + 2, n + 1)
        return f'{ind(m)}ReadFile ("{filename}",{i} => \n{a}\n{ind(m)})'


def get_line() -> IO[str]:
    """Read a line from stdin."""
    return Get(Return)


def put_line(text: str) -> IO[tuple[()]]:
    """Print a line to stdout."""
    return Put(text, Return(Unit))


def read_file(filename: str) -> IO[str]:
    """Read a file."""
    return ReadFile(filename, Return)


def pure_print(world: int, text: str) -> int:
    """Impure print function.

    NOTE: If you see this line you need to wash your hands
    """
    print(text)  # Impure side effect
    return world + 1


def pure_input(world: int) -> tuple[int, str]:
    """Impure input function.

    NOTE: If you see this line you need to wash your hands
    """
    text = input()  # Impure side effect
    return (world + 1, text)


# Type assertions for runtime checking
assert isinstance(IO, Functor)
assert isinstance(IO, Monad)

assert isinstance(Put, Functor)
assert isinstance(Put, Monad)

assert isinstance(Get, Functor)
assert isinstance(Get, Monad)

assert isinstance(ReadFile, Functor)
assert isinstance(ReadFile, Monad)
