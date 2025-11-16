"""The Continuation Monad.

* https://wiki.haskell.org/MonadCont_under_the_hood
* http://blog.sigfpe.com/2008/12/mother-of-all-monads.html
* http://www.haskellforall.com/2012/12/the-continuation-monad.html
"""

from __future__ import annotations

from collections.abc import Callable

from .typing import Functor, Monad
from .util import compose, identity  # type: ignore[attr-defined]

# Type alias for continuation
type Continuation[T, R] = Callable[[T], R]


class Cont[T, R]:
    """The Continuation Monad.

    The Continuation monad represents suspended computations in continuation-
    passing style (CPS).
    """

    def __init__(self, comp: Callable[[Continuation[T, R]], R]) -> None:
        """Cont constructor.

        Args:
            comp: A continuation-passing function
        """
        self._comp = comp

    @classmethod
    def unit(cls, value: T) -> Cont[T, R]:
        """Create new continuation.

        Haskell: a -> Cont a
        """
        fn: Callable[[Continuation[T, R]], R] = lambda cont: cont(value)
        return Cont(fn)

    def map[U](self, fn: Callable[[T], U]) -> Cont[U, R]:
        r"""Map a function over a continuation.

        Haskell: fmap f m = Cont $ \c -> runCont m (c . f)
        """

        def comp(cont: Callable[[U], R]) -> R:
            return self.run(compose(cont, fn))

        return Cont(comp)

    def bind[U](self, fn: Callable[[T], Cont[U, R]]) -> Cont[U, R]:
        r"""Chain continuation passing functions.

        Haskell: m >>= k = Cont $ \c -> runCont m $ \a -> runCont (k a) c
        """
        return Cont(lambda cont: self.run(lambda a: fn(a).run(cont)))

    @staticmethod
    def call_cc[T2, U, R2](fn: Callable[[Callable[[T2], Cont[U, R2]]], Cont[T2, R2]]) -> Cont[T2, R2]:
        r"""call-with-current-continuation.

        Haskell: callCC f = Cont $ \c -> runCont (f (\a -> Cont $ \_ -> c a )) c
        """
        return Cont(lambda c: fn(lambda a: Cont(lambda _: c(a))).run(c))  # type: ignore[arg-type]

    def run(self, cont: Callable[[T], R]) -> R:
        """Run the continuation with the given continuation function."""
        return self._comp(cont)

    def __or__[U](self, func: Callable[[T], Cont[U, R]]) -> Cont[U, R]:
        """Use | as operator for bind.

        Provide the | operator instead of the Haskell >>= operator
        """
        return self.bind(func)

    def __call__(self, comp: Callable[[T], R]) -> R:
        """Call the continuation."""
        return self.run(comp)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cont):
            return self(identity) == other(identity)  # type: ignore[arg-type]
        return NotImplemented


# Type assertions for runtime checking
assert isinstance(Cont, Functor)
assert isinstance(Cont, Monad)
