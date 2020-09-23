""" The Observable Monad

* https://www.youtube.com/watch?v=looJcaeboBY
* https://wiki.haskell.org/MonadCont_under_the_hood
* http://blog.sigfpe.com/2008/12/mother-of-all-monads.html
* http://www.haskellforall.com/2012/12/the-continuation-monad.html

"""

from typing import Any, Callable, TypeVar, Generic

from .util import identity, compose
from .typing import Monad, Functor

TSource = TypeVar("TSource")
TResult = TypeVar("TResult")


class Observable(Generic[TSource]):

    """The Rx Observable Monad.

    The Rx Observable monad is based on the Continuation monad
    representing suspended computations in continuation-passing style
    (CPS).
    """

    def __init__(self, subscribe: Callable[[Callable], Any]) -> None:
        """Observable constructor.

        Keyword arguments:
        subscribe -- A callable that takes a callable (on_next)
        """
        self._get_value = lambda: subscribe

    @classmethod
    def unit(cls, x: TSource) -> 'Observable[TSource]':
        """x -> Observable x"""
        return cls(lambda on_next: on_next(x))
    just = unit

    def map(self, mapper: Callable[[TSource], TResult]) -> 'Observable[TResult]':
        r"""Map a function over an observable.

        Haskell: fmap f m = Cont $ \c -> runCont m (c . f)
        """
        source = self
        return Observable(lambda on_next: source.subscribe(compose(on_next, mapper)))

    def bind(self, fn: Callable[[TSource], 'Observable[TResult]']) -> 'Observable[TResult]':
        r"""Chain continuation passing functions.

        Haskell: m >>= k = Cont $ \c -> runCont m $ \a -> runCont (k a) c
        """
        source = self
        return Observable(lambda on_next: source.subscribe(lambda a: fn(a).subscribe(on_next)))
    flat_map = bind

    def filter(self, predicate: Callable[[TSource], bool]) -> 'Observable[TSource]':
        """Filter the on_next continuation functions"""
        source = self

        def subscribe(on_next):
            def _next(x):
                if predicate(x):
                    on_next(x)

            return source.subscribe(_next)
        return Observable(subscribe)

    @staticmethod
    def call_cc(fn: Callable) -> 'Observable':
        r"""call-with-current-continuation.

        Haskell: callCC f = Cont $ \c -> runCont (f (\a -> Cont $ \_ -> c a )) c
        """
        def subscribe(on_next):
            return fn(lambda a: Observable(lambda _: on_next(a))).subscribe(on_next)

        return Observable(subscribe)

    def subscribe(self, on_next: Callable[[TSource], None]) -> Any:
        return self._get_value()(on_next)

    def __or__(self, func):
        """Use | as operator for bind.

        Provide the | operator instead of the Haskell >>= operator
        """
        return self.bind(func)

    def __eq__(self, other) -> bool:
        return self.subscribe(identity) == other.subscribe(identity)


assert(isinstance(Observable, Functor))
assert(isinstance(Observable, Monad))
