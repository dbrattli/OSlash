""" The Continuation Monad

* https://wiki.haskell.org/MonadCont_under_the_hood
* http://blog.sigfpe.com/2008/12/mother-of-all-monads.html
* http://www.haskellforall.com/2012/12/the-continuation-monad.html

"""

from typing import Callable, Generic, TypeVar


from .util import identity, compose
from .typing import Monad, Functor

T = TypeVar('T')
T2 = TypeVar('T2')
TResult = TypeVar('TResult')

TCont = Callable[[T], TResult]


class Cont(Generic[T, TResult]):
    """The Continuation Monad.

    The Continuation monad represents suspended computations in continuation-
    passing style (CPS).
    """

    def __init__(self, comp: Callable[[TCont], TResult]) -> None:
        """Cont constructor.

        Keyword arguments:
        cont -- A callable
        """
        self._comp = comp

    @classmethod
    def unit(cls, value: T) -> 'Cont[T, TResult]':
        """Create new continuation.

        Haskell: a -> Cont a
        """
        fn: Callable[[TCont], TResult] = lambda cont: cont(value)
        return Cont(fn)

    def map(self, fn: Callable[[T], T2]) -> 'Cont[T2, TResult]':
        r"""Map a function over a continuation.

        Haskell: fmap f m = Cont $ \c -> runCont m (c . f)
        """
        def comp(cont: Callable[[T2], TResult]) -> TResult:
            return self.run(compose(cont, fn))
        return Cont(comp)

    def bind(self, fn: Callable[[T], 'Cont[T2, TResult]']) -> 'Cont[T2, TResult]':
        r"""Chain continuation passing functions.

        Haskell: m >>= k = Cont $ \c -> runCont m $ \a -> runCont (k a) c
        """
        return Cont(lambda cont: self.run(lambda a: fn(a).run(cont)))

    @staticmethod
    def call_cc(fn: Callable) -> 'Cont':
        r"""call-with-current-continuation.

        Haskell: callCC f = Cont $ \c -> runCont (f (\a -> Cont $ \_ -> c a )) c
        """
        return Cont(lambda c: fn(lambda a: Cont(lambda _: c(a))).run(c))

    def run(self, cont: Callable[[T], TResult]) -> TResult:
        return self._comp(cont)

    def __or__(self, func):
        """Use | as operator for bind.

        Provide the | operator instead of the Haskell >>= operator
        """
        return self.bind(func)

    def __call__(self, comp: Callable[[T], TResult]) -> TResult:
        return self.run(comp)

    def __eq__(self, other) -> bool:
        return self(identity) == other(identity)


assert isinstance(Cont, Functor)
assert isinstance(Cont, Monad)
