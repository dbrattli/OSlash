"""Implementation of IO Actions - "The Gods Must Be Crazy"

Many thanks to Chris Taylor and his excellent blog post "IO Is Pure",
http://chris-taylor.github.io/blog/2013/02/09/io-is-not-a-side-effect/
"""

from .applicative import Applicative
from .functor import Functor
from .monad import Monad

class IO(Monad, Applicative, Functor):
    """IO Actions specify something that can be done. They are not active in
    and of themselves. They need to be "run" to make something happen. Simply
    having an action lying around doesn't make anything happen.
    """

    def __init__(self, value=None):
        """A container for a value"""

        super().__init__()
        self._get_value = lambda: value

    def bind(self, func) -> "IO":
        """IO a -> (a -> IO b) -> IO b"""

        return func(self._get_value())

    def apply(self, something) -> "IO":
        return something.fmap(self._get_value())

    def fmap(self, func) -> "IO":
        return IO(func(self._get_value()))

    def __call__(self, *args, **kwargs):
        """Nothing more to run."""

        return IO(self._get_value())

    def __str__(self, m=0, n=0):
        a = self._get_value()
        return "%sReturn %s" % (ind(m), a)

    def __repr__(self):
        return self.__str__()


class Put(IO):
    """A container holding a string to be printed to stdout, followed by
    another IO Action.
    """

    def __init__(self, text: str, action: IO):
        super().__init__()
        self.print_func = print
        self._get_value = lambda: (text, action)

    def bind(self, func) -> IO:
        """IO a -> (a -> IO b) -> IO b"""

        text, a = self._get_value()
        return Put(text, a.bind(func))

    def fmap(self, func) -> "IO":
        # Put s (fmap f io)
        text, action = self._get_value()
        return Put(text, action.fmap(func))

    def __call__(self, *args, **kwargs):
        """Run IO action"""

        text, action = self._get_value()
        self.print_func("%s" % text)
        return action()

    def __str__(self, m=0, n=0):
        s, io = self._get_value()
        a = io.__str__(m+2,n)
        return '%sPut ("%s",\n%s\n%s)' % (ind(m), s, a, ind(m))


class Get(IO):
    """A container holding a function from string -> IO, which can be
    applied to whatever string is read from stdin.
    """

    def __init__(self, func):
        super().__init__(func)
        self.input_func = input
        self._get_value = lambda: func

    def bind(self, func) -> IO:
        """IO a -> (a -> IO b) -> IO b"""

        g = self._get_value()
        return Get(lambda s: g(s).bind(func))

    def fmap(self, func) -> "IO":
        # Get (\s -> fmap f (g s))
        g = self._get_value()
        return Get(lambda s: g(s).fmap(func))

    def __call__(self, *args, **kwargs):
        """Run IO Action"""

        func = self._get_value()
        action = func(self.input_func())
        return action()

    def __str__(self, m=0, n=0):
        g = self._get_value()
        i = "$%s" % n
        a = (g(i)).__str__(m+2, n+1)
        return '%sGet (%s -> \n%s\n%s)' % (ind(m), i, a, ind(m))

class ReadFile(IO):
    def __init__(self, filename, func):
        super().__init__((filename, func))
        self.open_func = open
        self._get_value = lambda: (filename, func)

    def bind(self, func) -> IO:
        """IO a -> (a -> IO b) -> IO b"""

        filename, g = self._get_value()
        return ReadFile(filename, lambda s: g(s).bind(func))

    def fmap(self, func) -> "IO":
        # Get (\s -> fmap f (g s))
        filename, g = self._get_value()
        return Get(lambda s: g(s).fmap(func))

    def __call__(self, *args, **kwargs):
        """Run IO Action"""

        filename, func = self._get_value()
        f = self.open_func(filename)
        action = func(f.read())
        return action()

    def __str__(self, m=0, n=0):
        filename, g = self._get_value()
        i = "$%s" % n
        a = (g(i)).__str__(m+2, n+1)
        return '%sReadFile ("%s",%s -> \n%s\n%s)' % (ind(m), filename, i, a, ind(m))


def get_line() -> IO:
    return Get(lambda s: IO(s))

def put_line(string=None) -> IO:
    return Put(string, IO(()))

def read_file(filename) -> IO:
    return ReadFile(filename, lambda s: IO(s))

# Utility for indentation
ind = lambda x: ' '*x
