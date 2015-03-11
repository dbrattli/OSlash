"""Implementation of IOActions - "The Gods Must Be Crazy"

Many thanks to Chris Taylor and his excellent blog post "IO Is Pure",
http://chris-taylor.github.io/blog/2013/02/09/io-is-not-a-side-effect/
"""

from .applicative import Applicative
from .functor import Functor
from .monoid import Monoid
from .monad import Monad


class IOAction(Monad, Monoid, Applicative, Functor):

    def __init__(self, value=None):
        super().__init__()
        self._get_value = lambda: value

    def bind(self, func) -> "IOAction":
        """IOAction a -> (a -> IOAction b) -> IOAction b"""

        return func(self._get_value())

    def mappend(self, other) -> "IOAction":
        raise NotImplementedError()

    def apply(self, something) -> "IOAction":
        raise NotImplementedError()

    def fmap(self, func) -> "IOAction":
        raise NotImplementedError()

    @classmethod
    def mempty(cls) -> "IOAction":
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
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

    def __call__(self, *args, **kwargs):
        text, action = self._get_value()
        print("output: %s" % text)
        return action()

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

    def __call__(self, *args, **kwargs):
        g = self._get_value()
        text = input()
        return (g(text))()

    def __str__(self):
        g = self._get_value()
        return "Get(%s)" % g


def get():
    return Get(lambda s: IOAction(s))

def put(string):
    return Put(string, IOAction(()))

if __name__ == "__main__":
    main = get().bind(put)
    main()
