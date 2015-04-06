from functools import partial

from oslash.abc import Functor
from oslash.abc import Monad
from oslash.abc import Applicative

from oslash.util import compose


class Reader(Monad, Applicative, Functor):

    """The Reader monad.

    The Reader monad pass the data you want to share between functions.
    Functions may read that data, but can't change it. The reader monad
    lets us access shared immutable state within a monadic context.
    """

    def __init__(self, func: "Callable"):
        """Initialize a new reader.

        return a = Reader $ \\_ -> a
        """
        self._get_value = lambda: func

    @classmethod
    def return_(cls, value: "Any") -> "Reader":
        """The return function creates a Reader that ignores the
        environment and produces the given value.
        """
        return cls(lambda _: value)
    pure = return_

    def fmap(self, mapper: "Callable[[Any], Any]") -> "Reader":
        """fmap f m = Reader $ \\r -> f (runReader m r)."""
        func = self.run_reader()

        def _(env):
            try:
                ret = mapper(func(env))
            except TypeError:
                ret = partial(mapper, func(env))
            return ret
        return Reader(_)  # lambda r: mapper(func(r)))

    def bind(self, func: "Callable[[Any], Reader]") -> "Reader":
        """m >>= k  = Reader $ \\r -> runReader (k (runReader m r)) r
        """
        return Reader(lambda r: (func(self.run_reader()(r))).run_reader()(r))

    def apply(self, something: "Reader") -> "Reader":
        """(<*>) :: f (a -> b) -> f a -> f b.

        (R f) <*> (R x) = R $ \e -> (f e) (x e)

        Apply (<*>) is a beefed up fmap. It takes a functor value that
        has a function in it and another functor, and extracts that
        function from the first functor and then maps it over the second
        one.
        """

        func = self.run_reader()
        x = something.run_reader()

        def _(env):
            f = func(env)
            try:
                ret = f(x(env))
            except TypeError:
                ret = partial(f, x(env))
            return ret

        return Reader(_)  # lambda env: f(env)(x(env)))

    def asks(self, func: "Callable") -> "Reader":
        pass

    def run_reader(self) -> "Callable":
        """The inverse of the Reader constructor

        runReader :: Reader r a -> r -> a
        """
        return self._get_value()

    def __call__(self, *args, **kwargs) -> "Any":
        func = self.run_reader()
        return func(*args, **kwargs)

    def __eq__(self, other) -> bool:
        environment = 0
        print(self(environment), other(environment))
        return self(environment) == other(environment)

    def __str__(self) -> str:
        return "Reader(%s)" % self._get_value()

    def __repr__(self) -> str:
        return str(self)


class MonadReader(Reader):
    @classmethod
    def ask(cls):
        """Reader $ \\x -> x

        Provides a way to easily access the environment.
        """
        return cls(lambda x: x)

    def local(self, func):
        """local f c = Reader $ \e -> runReader c (f e)
        """
        return Reader(lambda e: self.run_reader(func(e)))
