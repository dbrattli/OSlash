"""Implementation of IOActions - The Gods Must Be Crazy

Many thanks to Chris Taylor and his blog post "IO Is Pure",
http://chris-taylor.github.io/blog/2013/02/09/io-is-not-a-side-effect/
"""

from functools import partial

from .applicative import Applicative
from .functor import Functor
from .monoid import Monoid
from .monad import Monad


class IOAction(Monad, Monoid, Applicative, Functor, list):

    def __init__(self, value=None):
        super().__init__()
        self._get_value = lambda: value

    def bind(self, func) -> "IOAction":
        """IOAction a -> (a -> IOAction b) -> IOAction b"""

        return func(self._get_value())

    def run(self):
        return self

    def __str__(self):
        value = self._get_value()
        return "IOAction(%s)" % str(value)

    def __repr__(self):
        return self.__str__()

class Put(IOAction):
    def __init__(self, text: str, action: IOAction):
        super().__init__()
        self._get_value = lambda: (text, action)

    def bind(self, func) -> "IOAction":
        """IOAction a -> (a -> IOAction b) -> IOAction b"""

        text, a = self._get_value()
        return Put(text, a.bind(func))

    def run(self):
        text, action = self._get_value()
        print("output: %s" % text)
        return action.run()

    def __str__(self):
        text, action = self._get_value()
        return "Put(%s, %s)" % (text, action)


class Get(IOAction):
    def __init__(self, func):
        super().__init__(func)
        self._get_value = lambda: func

    def bind(self, func) -> "IOAction":
        """IOAction a -> (a -> IOAction b) -> IOAction b"""

        g = self._get_value()
        return Get(lambda s: (g(s)).bind(func))

    def run(self):
        g = self._get_value()
        text = input()
        return (g(text)).run()

    def __str__(self):
        g = self._get_value()
        return "Get(%s)" % g


def get():
    return Get(lambda s: IOAction(s))

def put(string):
    return Put(string, IOAction(()))

