from functools import partial

from typing import Callable, Any, TypeVar, Generic

from .typing import Functor
from .typing import Monad
from .typing import Applicative

TEnv = TypeVar("TEnv")
TSource = TypeVar("TSource")
TResult = TypeVar("TResult")


class Reader(Generic[TEnv, TSource]):
    """The Reader monad.

    The Reader monad pass the state you want to share between functions.
    Functions may read that state, but can't change it. The reader monad
    lets us access shared immutable state within a monadic context.

    The Reader is just a fancy name for a wrapped function, so this
    monad could also be called the Function monad, or perhaps the
    Callable monad. Reader is all about composing wrapped functions.
    """

    def __init__(self, fn: Callable[[TEnv], TSource]) -> None:
        """Initialize a new reader."""

        self.fn = fn

    @classmethod
    def unit(cls, value: TSource) -> "Reader[TEnv, TSource]":
        r"""The return function creates a Reader that ignores the
        environment and produces the given value.

        return a = Reader $ \_ -> a
        """
        return cls(lambda _: value)

    def map(self, fn: Callable[[TSource], TResult]) -> "Reader[TEnv, TResult]":
        r"""Map a function over the Reader.

        Haskell:
        fmap f m = Reader $ \r -> f (runReader m r).
        fmap f g = (\x -> f (g x))
        """

        def _compose(x: Any) -> Any:
            return fn(self.run(x))

        return Reader(_compose)

    def bind(self, fn: "Callable[[TSource], Reader[TEnv, TResult]]") -> "Reader[TEnv, TResult]":
        r"""Bind a monadic function to the Reader.

        Haskell:
        Reader: m >>= k  = Reader $ \r -> runReader (k (runReader m r)) r
        Function: h >>= f = \w -> f (h w) w
        """
        return Reader(lambda x: fn(self.run(x)).run(x))

    @classmethod
    def pure(cls, fn: Callable[[TSource], TResult]) -> "Reader[TEnv, Callable[[TSource], TResult]]":
        return Reader.unit(fn)

    def apply(
        self: "Reader[TEnv, Callable[[TSource], TResult]]", something: "Reader[TEnv, TSource]"
    ) -> "Reader[TEnv, TResult]":
        r"""(<*>) :: f (a -> b) -> f a -> f b.

        Haskell: f <*> g = \x -> f x (g x)

        Apply (<*>) is a beefed up map. It takes a Reader that
        has a function in it and another Reader, and extracts that
        function from the first Reader and then maps it over the second
        one (composes the two functions).
        """

        def comp(env: TEnv):
            fn: Callable[[TSource], TResult] = self.run(env)

            value: TSource = something.run(env)
            try:
                return fn(value)
            except TypeError:
                return partial(fn, value)

        return Reader(comp)

    def run(self, env: TEnv) -> TSource:
        """Run reader in given environment.

        Haskell: runReader :: Reader r a -> r -> a

        Applies given environment on wrapped function.
        """
        return self.fn(env)

    def __call__(self, env: TEnv) -> TSource:
        """Call the wrapped function."""

        return self.run(env)

    def __str__(self) -> str:
        return "Reader(%s)" % repr(self.fn)

    def __repr__(self) -> str:
        return str(self)


class MonadReader(Reader[TEnv, TSource]):

    """The MonadReader class.

    The MonadReader class provides a number of convenience functions
    that are very useful when working with a Reader monad.
    """

    @classmethod
    def ask(cls) -> Reader[TEnv, TEnv]:
        r"""Reader $ \x -> x

        Provides a way to easily access the environment.
        ask lets us read the environment and then play with it
        """
        return Reader(lambda x: x)

    @classmethod
    def asks(cls, fn: Callable[[TEnv], TSource]) -> Reader[TEnv, TSource]:
        """
        Given a function it returns a Reader which evaluates that
        function and returns the result.

        asks :: (e -> a) -> R e a
        asks f = do
            e <- ask
            return $ f e

        asks sel = ask >>= return . sel
        """

        return cls.ask().bind(lambda env: cls.unit(fn(env)))

    def local(self, fn: Callable[[TEnv], TEnv]) -> Reader[TEnv, TSource]:
        r"""local transforms the environment a Reader sees.

        local f c = Reader $ \e -> runReader c (f e)
        """
        return Reader(lambda env: self.run(fn(env)))


assert isinstance(Reader, Functor)
assert isinstance(Reader, Applicative)
assert isinstance(Reader, Monad)
