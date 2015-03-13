"""Implementation of IOActions - "The Gods Must Be Crazy"

Many thanks to Chris Taylor and his excellent blog post "IO Is Pure",
http://chris-taylor.github.io/blog/2013/02/09/io-is-not-a-side-effect/
"""

from .applicative import Applicative
from .functor import Functor
from .monad import Monad


class IOAction(Monad, Applicative, Functor):

    def __init__(self, value=None):
        """A container for a value"""

        super().__init__()
        self._get_value = lambda: value

    def bind(self, func) -> "IOAction":
        """IOAction a -> (a -> IOAction b) -> IOAction b"""

        return func(self._get_value())

    def apply(self, something) -> "IOAction":
        return something.fmap(self._get_value())

    def fmap(self, func) -> "IOAction":
        return IOAction(func(self._get_value()))

    def __call__(self, *args, **kwargs):
        """Run IO action. Nothing more to run."""

        return

    def __str__(self, m=0, n=0):
        a = self._get_value()
        return "%sReturn %s" % (ind(m), a)

    def __repr__(self):
        return self.__str__()


class Put(IOAction):
    """A container holding a string to be printed to stdout, followed by
    another IOAction.
    """

    def __init__(self, text: str, action: IOAction):
        super().__init__()
        self._get_value = lambda: (text, action)

    def bind(self, func) -> IOAction:
        """IOAction a -> (a -> IOAction b) -> IOAction b"""

        text, a = self._get_value()
        return Put(text, a.bind(func))

    def fmap(self, func) -> "IOAction":
        # Put s (fmap f io)
        text, action = self._get_value()
        return Put(text, action.fmap(func))

    def __call__(self, *args, **kwargs):
        """Run IO action"""

        text, action = self._get_value()
        print("output: %s" % text)
        return action()

    def __str__(self, m=0, n=0):
        s, io = self._get_value()
        a = io.__str__(m+2,n)
        return '%sPut ("%s",\n%s\n%s)' % (ind(m), s, a, ind(m))


class Get(IOAction):
    """A container holding a function from string -> IOAction, which can be
    applied to whatever string is read from stdin.
    """

    def __init__(self, func):
        super().__init__(func)
        self._get_value = lambda: func

    def bind(self, func) -> IOAction:
        """IOAction a -> (a -> IOAction b) -> IOAction b"""

        g = self._get_value()
        return Get(lambda s: g(s).bind(func))

    def fmap(self, func) -> "IOAction":
        # Get (\s -> fmap f (g s))
        g = self._get_value()
        return Get(lambda s: g(s).fmap(func))

    def __call__(self, *args, **kwargs):
        """Run IO action"""

        func = self._get_value()
        text = input()
        action = func(text)
        return action()

    def __str__(self, m=0, n=0):
        g = self._get_value()
        i = "$%s" % n
        a = (g(i)).__str__(m+2, n+1)
        return '%sGet (%s -> \n%s\n%s)' % (ind(m), i, a, ind(m))

def get():
    return Get(lambda s: IOAction(s))

def put(string):
    return Put(string, IOAction(()))

ind = lambda x: ' '*x
