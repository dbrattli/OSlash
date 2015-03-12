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

    def __str__(self):
        return self.go(0, 0)

    def __repr__(self):
        return self.__str__()

    def go(self, m, n):
        a = self._get_value()
        return " "*m + "Return " + str(a)

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

    def go(self, m, n):
        s, io = self._get_value()
        return ' '*m + 'Put "' + s + '" (\n' + io.go(m+2,n) + '\n' + ' '*m+ ')'

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

    def go(self, m, n):
        g = self._get_value()
        i = "$%s" % n
        return " "*m + 'Get (' + i + ' -> \n' + (g(i)).go(m+2, n+1)  + '\n' + ' '*m+')'

def get():
    return Get(lambda s: IOAction(s))

def put(string):
    return Put(string, IOAction(()))
