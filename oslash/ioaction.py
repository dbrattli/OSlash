"""Implementation of IO Actions.

Many thanks to Chris Taylor and his excellent blog post "IO Is Pure",
http://chris-taylor.github.io/blog/2013/02/09/io-is-not-a-side-effect/
"""

from typing import Any, Callable, Generic, TypeVar, Tuple

from .abc import Applicative
from .abc import Functor
from .abc import Monad
from .util import Unit, indent as ind


class IO(Monad, Applicative, Functor):
    """A container for a world remaking function.

    IO Actions specify something that can be done. They are not active
    in and of themselves. They need to be "run" to make something
    happen. Simply having an action lying around doesn't make anything
    happen.
    """

    def __init__(self: 'IO', value: Any=None) -> None:
        """Create IO Action."""

        super().__init__()
        self._value = value

    def bind(self: 'IO', func: Callable[[Any], 'IO']) -> 'IO':
        """IO a -> (a -> IO b) -> IO b."""

        return func(self._value)

    def apply(self, something: 'IO') -> 'IO':
        """Apply wrapped function over something."""
        return something.map(self._value)

    def map(self, func: Callable[[Any], Any]) -> 'IO':
        return IO(func(self._value))

    def run(self, world: int) -> Any:
        """Run IO action."""
        return self._value

    def __call__(self, world: int = 0) -> Any:
        """Nothing more to run."""
        return self.run(world)

    def __str__(self, m: int=0, n: int=0) -> str:
        a = self._value
        return "%sReturn %s" % (ind(m), a)

    def __repr__(self) -> str:
        return self.__str__()


class Put(IO):
    """The Put action.

    A container holding a string to be printed to stdout, followed by
    another IO Action.
    """

    def __init__(self, text: str, action: IO) -> None:
        super().__init__((text, action))

    def bind(self, func: Callable[[Any], IO]) -> 'Put':
        """IO a -> (a -> IO b) -> IO b"""

        text, a = self._value
        return Put(text, a.bind(func))

    def map(self, func: Callable[[Any], Any]) -> 'Put':
        # Put s (fmap f io)
        text, action = self._value
        return Put(text, action.map(func))

    def run(self, world: int) -> IO:
        """Run IO action"""

        text, action = self._value
        new_world = pure_print(world, text)
        return action(world=new_world)

    def __call__(self, world: int=0) -> IO:
        return self.run(world)

    def __str__(self, m: int=0, n: int=0) -> str:
        s, io = self._value
        a = io.__str__(m + 1, n)
        return '%sPut ("%s",\n%s\n%s)' % (ind(m), s, a, ind(m))


class Get(IO):
    """A container holding a function from string -> IO, which can
    be applied to whatever string is read from stdin.
    """

    def __init__(self, func: Callable[[str], IO]) -> None:
        super().__init__(func)

    def bind(self, func: Callable[[Any], IO]) -> IO:
        """IO a -> (a -> IO b) -> IO b"""

        g = self._value
        return Get(lambda text: g(text).bind(func))

    def map(self, func: Callable[[Any], Any]) -> 'Get':
        # Get (\s -> fmap f (g s))
        g = self._value
        return Get(lambda s: g(s).map(func))

    def run(self, world: int) -> IO:
        """Run IO Action"""

        func = self._value
        new_world, text = pure_input(world)
        action = func(text)
        return action(world=new_world)

    def __call__(self, world: int=0) -> IO:
        return self.run(world)

    def __str__(self, m: int=0, n: int=0) -> str:
        g = self._value
        i = "x%s" % n
        a = g(i).__str__(m + 1, n + 1)
        return '%sGet (%s => \n%s\n%s)' % (ind(m), i, a, ind(m))


class ReadFile(IO):
    """A container holding a filename and a function from string -> IO,
    which can be applied to whatever string is read from the file.
    """

    def __init__(self, filename: str, func: Callable[[str], IO]) -> None:
        super().__init__((filename, func))
        self.open_func = open
        self._get_value = lambda: (filename, func)

    def bind(self, func: Callable[[Any], IO]) -> IO:
        """IO a -> (a -> IO b) -> IO b"""

        filename, g = self._get_value()
        return ReadFile(filename, lambda s: g(s).bind(func))

    def map(self, func: Callable[[Any], Any]) -> IO:
        # Get (\s -> fmap f (g s))
        filename, g = self._get_value()
        return Get(lambda s: g(s).map(func))

    def run(self, world: int) -> IO:
        """Run IO Action"""

        filename, func = self._get_value()
        f = self.open_func(filename)
        action = func(f.read())
        return action(world=world + 1)

    def __call__(self, world: int=0) -> IO:
        return self.run(world)

    def __str__(self, m: int=0, n: int=0) -> str:
        filename, g = self._get_value()
        i = "x%s" % n
        a = g(i).__str__(m + 2, n + 1)
        return '%sReadFile ("%s",%s => \n%s\n%s)' % (ind(m), filename, i, a, ind(m))


def get_line() -> IO:
    return Get(lambda text: IO(text))


def put_line(string: str=None) -> IO:
    return Put(string, IO(Unit))


def read_file(filename: str) -> IO:
    return ReadFile(filename, lambda text: IO(text))


def pure_print(world: int, text: str) -> int:
    print(text)  # Impure. If you see this line you need to wash your hands
    return world + 1


def pure_input(world: int) -> Tuple[int, str]:
    text = input()  # Impure. If you see this line you need to wash your hands
    return (world + 1, text)
