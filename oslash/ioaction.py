"""Implementation of IO Actions.

Many thanks to Chris Taylor and his excellent blog post "IO Is Pure",
http://chris-taylor.github.io/blog/2013/02/09/io-is-not-a-side-effect/
"""

from typing import Any, Callable, Generic, TypeVar

from .abc import Applicative
from .abc import Functor
from .abc import Monad
from .util import Unit, indent as ind


A = TypeVar('A')
B = TypeVar('B')


class IO(Generic[A], Monad[A], Applicative[A], Functor[A]):
    """IO Actions specify something that can be done. They are not active in
    and of themselves. They need to be "run" to make something happen. Simply
    having an action lying around doesn't make anything happen.
    """

    def __init__(self, func: A=None) -> None:
        """A container for a world remaking function"""

        super().__init__()
        self._get_value = lambda: func or Unit

    def bind(self, func: Callable[[A], 'IO[B]']) -> 'IO[B]':
        """IO a -> (a -> IO b) -> IO b"""

        return func(self._get_value())

    def apply(self, something) -> "IO":
        return something.map(self._get_value())

    def map(self, func: Callable[[A], B]) -> 'IO[B]':
        return IO(func(self._get_value()))

    def run(self, *args, **kwargs) -> 'IO[A]':
        return self._get_value()

    def __call__(self, *args, **kwargs) -> 'IO[A]':
        """Nothing more to run."""
        return self.run(*args, **kwargs)

    def __str__(self, m=0, n=0):
        a = self._get_value()
        return "%sReturn %s" % (ind(m), a)

    def __repr__(self):
        return self.__str__()


class Put(Generic[A], IO[A]):
    """A container holding a string to be printed to stdout, followed by
    another IO Action.
    """

    def __init__(self, text: str, action: IO[A]) -> None:
        super().__init__((text, action))

    def bind(self, func: 'Callable[[A], Put[B]]') -> 'Put[B]':
        """IO a -> (a -> IO b) -> IO b"""

        text, a = self._get_value()
        return Put(text, a.bind(func))

    def map(self, func: Callable[[A], B]) -> 'Put[B]':
        # Put s (fmap f io)
        text, action = self._get_value()
        return Put(text, action.map(func))

    def run(self, *args, **kwargs):
        """Run IO action"""

        world = kwargs.get('world', 0)
        text, action = self._get_value()
        kwargs.get("print", print)("%s" % text)
        return action(world=world + 1)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __str__(self, m=0, n=0):
        s, io, world = self._get_value()
        a = io.__str__(m + 1, n)
        return '%sPut ("%s",\n%s\n%s)' % (ind(m), s, a, ind(m))


class Get(Generic[A], IO[A]):
    """A container holding a function from string -> IO[A], which can
    be applied to whatever string is read from stdin.
    """

    def __init__(self, func: Callable[[str], IO[A]]) -> None:
        super().__init__(func)

        self.input_func = input  # type: Callable[[], str]

    def bind(self, func: 'Callable[[A], Get[B]]') -> 'Get[B]':
        """IO a -> (a -> IO b) -> IO b"""

        g = self._get_value()
        return Get(lambda text: g(text).bind(func))

    def map(self, func: Callable[[A], B]) -> 'Get[B]':
        # Get (\s -> fmap f (g s))
        g = self._get_value()
        return Get(lambda s: g(s).map(func))

    def run(self, *args, **kwargs):
        """Run IO Action"""
        world = kwargs.get('world', 0)
        func = self._get_value()
        action = func(self.input_func())
        return action(world=world + 1)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __str__(self, m: int=0, n: int=0) -> str:
        g = self._get_value()
        i = "$%s" % n
        a = (g(i)).__str__(m + 1, n + 1)
        return '%sGet (%s -> \n%s\n%s)' % (ind(m), i, a, ind(m))


class ReadFile(IO):
    """A container holding a filename and a function from string -> IO,
    which can be applied to whatever string is read from the file.
    """

    def __init__(self, filename: str, func: Callable[[str], IO[str]]) -> None:
        super().__init__((filename, func))
        self.open_func = open
        self._get_value = lambda: (filename, func)

    def bind(self, func: Callable[[Any], "ReadFile"]) -> IO:
        """IO a -> (a -> IO b) -> IO b"""

        filename, g = self._get_value()
        return ReadFile(filename, lambda s: g(s).bind(func))

    def map(self, func: Callable[[Any], Any]) -> IO:
        # Get (\s -> fmap f (g s))
        filename, g = self._get_value()
        return Get(lambda s: g(s).map(func))

    def run(self, *args, **kwargs):
        """Run IO Action"""

        world = kwargs.get('world', 0)
        filename, func = self._get_value()
        f = self.open_func(filename)
        action = func(f.read())
        return action(world=world + 1)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __str__(self, m: int=0, n: int=0) -> str:
        filename, g = self._get_value()
        i = "$%s" % n
        a = (g(i)).__str__(m + 2, n + 1)
        return '%sReadFile ("%s",%s -> \n%s\n%s)' % (ind(m), filename, i, a, ind(m))


def get_line() -> IO[str]:
    return Get(lambda text: IO(text))


def put_line(string: str=None) -> IO[A]:
    return Put(string, IO(Unit))


def read_file(filename: str) -> IO[str]:
    return ReadFile(filename, lambda text: IO(text))
