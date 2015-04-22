from functools import partial

from .util import compose
from .abc import Functor, Applicative, Monad


class Callable(Monad, Applicative, Functor):
    """The Callable aka function Monad."""

    def __init__(self, fn):
        self.fn = fn

    @classmethod
    def unit(cls, x: 'Any') -> 'Callable':
        r"""return x = \_ -> x"""
        return cls(lambda _: x)
    pure = unit

    def map(self, fn: 'Callable[[Callable], Callable]') -> 'Callable':
        r"""fmap f g = (\x -> f (g x))"""
        return Callable(lambda x: fn(self(x)))

    def bind(self, fn: 'Callable[[Callable], Callable]') -> 'Callable':
        r"""h >>= f = \w -> f (h w) w"""
        return Callable(lambda w: fn(self(w))(w))

    def apply(self, something: 'Callable') -> 'Callable':
        r"""f <*> g = \x -> f x (g x)"""

        def composed(x):
            try:
                ret = self(x)(something(x))
            except TypeError:
                ret = partial(self(x), something(x))
            return ret
        return Callable(composed)

    def __call__(self, *args, **kw):
        return self.fn(*args, **kw)

    def __eq__(self, other):
        return self(42) == other(42)
