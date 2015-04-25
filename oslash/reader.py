from functools import partial

from typing import Any, Callable

from .abc import Functor
from .abc import Monad
from .abc import Applicative


class Reader(Monad, Applicative, Functor):

    """The Reader monad.

    The Reader monad pass the state you want to share between functions.
    Functions may read that state, but can't change it. The reader monad
    lets us access shared immutable state within a monadic context.

    The Reader is just a fancy name for a wrapped function, so this
    monad could also be called the Function monad, or perhaps the
    Callable monad. Reader is all about composing wrapped functions.
    """

    def __init__(self, fn: Callable):
        r"""Initialize a new reader.

        """
        self.fn = fn

    @classmethod
    def unit(cls, value: Any) -> "Reader":
        """The return function creates a Reader that ignores the
        environment and produces the given value.

        return a = Reader $ \_ -> a
        """
        return cls(lambda _: value)

    @classmethod
    def pure(cls, fn: Callable) -> 'Reader':
        return cls.unit(fn)

    def map(self, fn: Callable[[Any], Any]) -> "Reader":
        r"""Map a function over the Reader.

        Haskell:
        fmap f m = Reader $ \r -> f (runReader m r).
        fmap f g = (\x -> f (g x))
        """
        def _compose(x):
            try:
                ret = fn(self(x))
            except TypeError:
                ret = partial(fn, self(x))
            return ret
        return Reader(_compose)

    def bind(self, fn: "Callable[[Any], Reader]") -> "Reader":
        r"""Bind a monadic function to the Reader.

        Haskell:
        Reader: m >>= k  = Reader $ \r -> runReader (k (runReader m r)) r
        Function: h >>= f = \w -> f (h w) w
        """
        return Reader(lambda x: fn(self(x))(x))

    def apply(self, something: "Reader") -> "Reader":
        r"""(<*>) :: f (a -> b) -> f a -> f b.

        Haskell: f <*> g = \x -> f x (g x)

        Apply (<*>) is a beefed up map. It takes a Reader that
        has a function in it and another Reader, and extracts that
        function from the first Reader and then maps it over the second
        one (composes the two functions).
        """

        def _compose(x):
            f = self(x)
            try:
                ret = f(something(x))
            except TypeError:
                ret = partial(f, something(x))
            return ret

        return Reader(_compose)

    def run(self, *args, **kwargs) -> Callable:
        """Return wrapped function.

        Haskell: runReader :: Reader r a -> r -> a

        This is the inverse of unit and returns the wrapped function.
        """
        return self(*args, **kwargs)

    def __call__(self, *args, **kwargs) -> Any:
        """Call the wrapped function."""
        return self.fn(*args, **kwargs) if args or kwargs else self.fn

    def __eq__(self, other) -> bool:
        environment = 42  # Can't be wrong!
        try:
            equal = self(environment) == other(environment)
        except Exception:
            equal = False
        return equal

    def __str__(self) -> str:
        return "Reader(%s)" % repr(self.fn)

    def __repr__(self) -> str:
        return str(self)


class MonadReader(Reader):

    """The MonadReader class.

    The MonadReader class provides a number of convenience functions
    that are very useful when working with a Reader monad.
    """

    @classmethod
    def ask(cls) -> Reader:
        r"""Reader $ \x -> x

        Provides a way to easily access the environment.
        ask lets us read the environment and then play with it
        """
        return cls(lambda x: x)

    @classmethod
    def asks(cls, fn: Callable) -> Reader:
        """
        Given a function it returns a Reader which evaluates that
        function and returns the result.

        asks :: (e -> a) -> R e a
        asks f = do
            e <- ask
            return $ f e

        asks sel = ask >>= return . sel
        """
        return cls.ask().bind(Reader(lambda x: cls.unit(fn(x))))

    def local(self, fn) -> Reader:
        r"""local transforms the environment a Reader sees.

        local f c = Reader $ \e -> runReader c (f e)
        """
        return Reader(lambda x: self(fn(x)))
