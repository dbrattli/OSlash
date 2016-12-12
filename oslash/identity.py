from functools import partial  # type: ignore

from typing import Any, Callable, Generic, TypeVar

from .abc import Functor
from .abc import Monad
from .abc import Applicative

A = TypeVar('A')
B = TypeVar('B')


class Identity(Generic[A], Monad[A], Applicative[A], Functor[A]):

    """The Identity monad.

    The Identity monad is the simplest monad, which attaches no
    information to values.
    """

    def __init__(self, value: A) -> None:
        """Initialize a new reader."""
        self._value = value

    def map(self, mapper: Callable[[A], B]) -> 'Identity[B]':
        """Map a function over wrapped values."""
        value = self._value
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Identity(result)

    def bind(self, func: Callable[[A], 'Identity[B]']) -> 'Identity[B]':
        return func(self._value)

    def apply(self, something: 'Identity[B]') -> 'Identity[B]':
        func = self._value
        return something.map(func)

    def run(self) -> A:
        return self._value

    def __call__(self) -> A:
        return self.run()

    def __eq__(self, other: 'Identity[B]') -> bool:
        return self._value == other()

    def __str__(self) -> str:
        return "Identity(%s)" % self._value

    def __repr__(self) -> str:
        return str(self)
