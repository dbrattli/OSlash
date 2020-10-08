from functools import partial
from typing import TypeVar, Generic, Callable

from .typing import Functor, Monad, Applicative


TSource = TypeVar('TSource')
TResult = TypeVar('TResult')


class Identity(Generic[TSource]):
    """Identity monad.

    The Identity monad is the simplest monad, which attaches no
    information to values.
    """
    def __init__(self, value: TSource) -> None:
        self._value = value

    @classmethod
    def unit(cls, value: TSource) -> 'Identity[TSource]':
        """Initialize a new identity."""
        return Identity(value)

    def map(self, mapper: Callable[[TSource], TResult]) -> 'Identity[TResult]':
        """Map a function over wrapped values."""
        result = mapper(self._value)
        return Identity(result)

    def bind(self, func: Callable[[TSource], 'Identity[TResult]']) -> 'Identity[TResult]':
        return func(self._value)

    @classmethod
    def pure(cls, value: TSource):
        return Identity(value)

    def apply(self: 'Identity[Callable[[TSource], TResult]]', something: 'Identity[TSource]') -> 'Identity[TResult]':
        def mapper(other_value):
            try:
                return self._value(other_value)
            except TypeError:
                return partial(self._value, other_value)
        return something.map(mapper)

    def run(self) -> TSource:
        return self._value

    def __call__(self) -> TSource:
        return self.run()

    def __eq__(self, other) -> bool:
        return self._value == other()

    def __str__(self) -> str:
        return "Identity(%s)" % self._value

    def __repr__(self) -> str:
        return str(self)


assert isinstance(Identity, Functor)
assert isinstance(Identity, Applicative)
assert isinstance(Identity, Monad)
