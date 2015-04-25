""" The Continuation Monad

* https://wiki.haskell.org/MonadCont_under_the_hood
* http://blog.sigfpe.com/2008/12/mother-of-all-monads.html
* http://www.haskellforall.com/2012/12/the-continuation-monad.html

"""

from typing import Any, Callable

from .util import identity, compose
from .abc import Monad, Functor


class Cont(Monad, Functor):

    """The Continuation Monad.

    The Continuation monad represents computations in continuation-
    passing style (CPS).
    """

    def __init__(self, fn: Callable[[Callable], Any]):
        self._get_value = lambda: fn

    @classmethod
    def unit(cls, a: Any) -> 'Cont':
        return cls(lambda k: k(a))

    def map(self, fn: Callable[[Any], Any]) -> 'Cont':
        r"""Map a function over a continuation.

        Haskell: fmap f m = Cont $ \c -> runCont m (c . f)
        """
        return Cont(lambda c: self.run(compose(c, fn)))

    def bind(self, fn: Callable[[Any], 'Cont']) -> 'Cont':
        r"""Chain continuation passing functions.

        Haskell: m >>= k = Cont $ \c -> runCont m $ \a -> runCont (k a) c
        """
        return Cont(lambda c: self.run(lambda a: (fn(a).run(c))))

    @staticmethod
    def call_cc(fn: Callable) -> 'Cont':
        r"""call-with-current-continuation.

        Haskell: callCC f = Cont $ \c -> runCont (f (\a -> Cont $ \_ -> c a )) c
        """
        return Cont(lambda c: fn(lambda a: Cont(lambda _: c(a))).run(c))

    def run(self, *args) -> Any:
        return self._get_value()(*args) if args else self._get_value()

    def __call__(self, *args, **kwargs) -> Any:
        return self.run(*args, **kwargs)

    def __eq__(self, other) -> bool:
        return self(identity) == other(identity)
