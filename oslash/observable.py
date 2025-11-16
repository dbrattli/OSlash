"""The Observable Monad.

* https://www.youtube.com/watch?v=looJcaeboBY
* https://wiki.haskell.org/MonadCont_under_the_hood
* http://blog.sigfpe.com/2008/12/mother-of-all-monads.html
* http://www.haskellforall.com/2012/12/the-continuation-monad.html
"""

from __future__ import annotations

from collections.abc import Callable

from .typing import Functor, Monad
from .util import compose, identity


class Observable[T]:
    """The Rx Observable Monad.

    The Rx Observable monad is based on the Continuation monad
    representing suspended computations in continuation-passing style
    (CPS).
    """

    def __init__(self, subscribe: Callable[[Callable[[T], None]], object]) -> None:
        """Observable constructor.

        Args:
            subscribe: A callable that takes a callable (on_next)
        """
        self._get_value = lambda: subscribe

    @classmethod
    def unit(cls, x: T) -> Observable[T]:
        """x -> Observable x"""
        return cls(lambda on_next: on_next(x))

    @classmethod
    def just(cls, x: T) -> Observable[T]:
        """Alias for unit."""
        return cls.unit(x)

    def map[U](self, mapper: Callable[[T], U]) -> Observable[U]:
        r"""Map a function over an observable.

        Haskell: fmap f m = Cont $ \c -> runCont m (c . f)
        """
        source = self
        return Observable(lambda on_next: source.subscribe(compose(on_next, mapper)))

    def bind[U](self, fn: Callable[[T], Observable[U]]) -> Observable[U]:
        r"""Chain continuation passing functions.

        Haskell: m >>= k = Cont $ \c -> runCont m $ \a -> runCont (k a) c
        """
        source = self
        return Observable(lambda on_next: source.subscribe(lambda a: fn(a).subscribe(on_next)))  # type: ignore[arg-type,return-value]

    flat_map = bind

    def filter(self, predicate: Callable[[T], bool]) -> Observable[T]:
        """Filter the on_next continuation functions"""
        source = self

        def subscribe(on_next: Callable[[T], None]) -> object:
            def _next(x: T) -> None:
                if predicate(x):
                    on_next(x)

            return source.subscribe(_next)

        return Observable(subscribe)

    @staticmethod
    def call_cc[T2, U](fn: Callable[[Callable[[T2], Observable[U]]], Observable[T2]]) -> Observable[T2]:
        r"""call-with-current-continuation.

        Haskell: callCC f = Cont $ \c -> runCont (f (\a -> Cont $ \_ -> c a )) c
        """

        def subscribe(on_next: Callable[[T2], None]) -> object:
            return fn(lambda a: Observable(lambda _: on_next(a))).subscribe(on_next)

        return Observable(subscribe)

    def subscribe(self, on_next: Callable[[T], None]) -> object:
        """Subscribe to the observable with an on_next callback."""
        return self._get_value()(on_next)

    def __or__[U](self, func: Callable[[T], Observable[U]]) -> Observable[U]:
        """Use | as operator for bind.

        Provide the | operator instead of the Haskell >>= operator
        """
        return self.bind(func)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Observable):
            # identity returns a value, but subscribe expects a function returning None
            # We can't properly compare observables this way, so we suppress the type error
            return self.subscribe(identity) == other.subscribe(identity)  # type: ignore[arg-type]
        return False


# Type assertions for runtime checking
assert isinstance(Observable, Functor)
assert isinstance(Observable, Monad)
