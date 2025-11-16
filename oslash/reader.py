"""Reader monad implementation.

The Reader monad passes shared immutable state between functions.
Functions may read that state, but can't change it.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import partial

from .typing import Applicative, Functor, Monad


class Reader[Env, T]:
    """The Reader monad.

    The Reader monad pass the state you want to share between functions.
    Functions may read that state, but can't change it. The reader monad
    lets us access shared immutable state within a monadic context.

    The Reader is just a fancy name for a wrapped function, so this
    monad could also be called the Function monad, or perhaps the
    Callable monad. Reader is all about composing wrapped functions.
    """

    def __init__(self, fn: Callable[[Env], T]) -> None:
        """Initialize a new reader."""
        self.fn = fn

    @classmethod
    def unit(cls, value: T) -> Reader[Env, T]:
        r"""The return function creates a Reader that ignores the
        environment and produces the given value.

        return a = Reader $ \_ -> a
        """
        return cls(lambda _: value)

    def map[U](self, fn: Callable[[T], U]) -> Reader[Env, U]:
        r"""Map a function over the Reader.

        Haskell:
        fmap f m = Reader $ \r -> f (runReader m r).
        fmap f g = (\x -> f (g x))
        """

        def compose(x: Env) -> U:
            return fn(self.run(x))

        return Reader(compose)

    def bind[U](self, fn: Callable[[T], Reader[Env, U]]) -> Reader[Env, U]:
        r"""Bind a monadic function to the Reader.

        Haskell:
        Reader: m >>= k  = Reader $ \r -> runReader (k (runReader m r)) r
        Function: h >>= f = \w -> f (h w) w
        """
        return Reader(lambda x: fn(self.run(x)).run(x))

    @classmethod
    def pure(cls, value: T) -> Reader[Env, T]:
        """Wrap a value in Reader context."""
        return cls.unit(value)

    def apply[U](self: Reader[Env, Callable[[T], U]], something: Reader[Env, T]) -> Reader[Env, U]:
        r"""(<*>) :: f (a -> b) -> f a -> f b.

        Haskell: f <*> g = \x -> f x (g x)

        Apply (<*>) is a beefed up map. It takes a Reader that
        has a function in it and another Reader, and extracts that
        function from the first Reader and then maps it over the second
        one (composes the two functions).
        """

        def comp(env: Env) -> U:
            func: Callable[[T], U] = self.run(env)
            value: T = something.run(env)
            try:
                return func(value)
            except TypeError:
                # Partial application for curried functions
                return partial(func, value)  # type: ignore

        return Reader(comp)

    def run(self, env: Env) -> T:
        """Run reader in given environment.

        Haskell: runReader :: Reader r a -> r -> a

        Applies given environment on wrapped function.
        """
        return self.fn(env)

    def __call__(self, env: Env) -> T:
        """Call the wrapped function."""
        return self.run(env)

    def __str__(self) -> str:
        return f"Reader({self.fn!r})"

    def __repr__(self) -> str:
        return str(self)


class MonadReader[Env, T](Reader[Env, T]):
    """The MonadReader class.

    The MonadReader class provides a number of convenience functions
    that are very useful when working with a Reader monad.
    """

    @classmethod
    def ask(cls) -> Reader[Env, Env]:
        r"""Reader $ \x -> x

        Provides a way to easily access the environment.
        ask lets us read the environment and then play with it
        """
        return Reader(lambda x: x)

    @classmethod
    def asks(cls, fn: Callable[[Env], T]) -> Reader[Env, T]:
        """Given a function it returns a Reader which evaluates that
        function and returns the result.

        asks :: (e -> a) -> R e a
        asks f = do
            e <- ask
            return $ f e

        asks sel = ask >>= return . sel
        """
        return cls.ask().bind(lambda env: cls.unit(fn(env)))

    def local(self, fn: Callable[[Env], Env]) -> Reader[Env, T]:
        r"""local transforms the environment a Reader sees.

        local f c = Reader $ \e -> runReader c (f e)
        """
        return Reader(lambda env: self.run(fn(env)))


# Type assertions for runtime checking
assert isinstance(Reader, Functor)
assert isinstance(Reader, Applicative)
assert isinstance(Reader, Monad)
