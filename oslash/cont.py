""" The Continuation Monad

* http://blog.sigfpe.com/2008/12/mother-of-all-monads.html
* http://www.haskellforall.com/2012/12/the-continuation-monad.html

"""

from typing import Any, Callable

from .util import identity
from .abc import Monad


class Cont(Monad):
    """The Continuation Monad.

    The Continuation monad represents computations in continuation-
    passing style (CPS).
    """

    def __init__(self, fn: Callable):
        self._get_value = lambda: fn

    @classmethod
    def unit(cls, a: Any) -> 'Cont':
        return cls(lambda k: k(a))

    def bind(self, fn: Callable) -> 'Cont':
        r"""m >>= k = Cont $ \c -> runCont m $ \a -> runCont (k a) c"""

        s = lambda c: self.run(c)
        t = lambda c: lambda a: fn(a).run(c)
        return Cont(lambda c: s(t(c)))

    @staticmethod
    def call_cc(fn: Callable):
        """call-with-current-continuation.

        Haskell: callCC f = Cont $ \c -> runCont (f (\a -> Cont $ \_ -> c a )) c
        """
        return Cont(lambda c: fn(lambda a: Cont(lambda _: c(a))).run(c))

    def run(self, *args):
        return self._get_value()(*args) if args else self._get_value()

    def __call__(self, *args, **kwargs) -> "Any":
        return self.run(*args, **kwargs)

    def __eq__(self, other) -> bool:
        return self(identity) == other(identity)
