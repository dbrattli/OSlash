from functools import partial  # type: ignore

from typing import Any, Callable, Generic, TypeVar

from .abc import Functor
from .abc import Monad
from .abc import Applicative

A = TypeVar('A')
B = TypeVar('B')


class Identity(Generic[A], Monad, Applicative, Functor):
    """Identity monad.

    The Identity monad is the simplest monad, which attaches no
    information to values.
    """

    def __init__(self, value: Any) -> None:
        """Initialize a new reader."""
        self._value = value

    def map(self, mapper: Callable[[Any], Any]) -> 'Identity':
        """Map a function over wrapped values."""
        value = self._value
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Identity(result)

    def bind(self, func: Callable[[Any], 'Identity']) -> 'Identity':
        return func(self._value)

    def apply(self, something: 'Identity') -> 'Identity':
        func = self._value
        return something.map(func)

    def run(self) -> Any:
        return self._value

    def __call__(self) -> Any:
        return self.run()

    def __eq__(self, other) -> bool:
        return self._value == other()

    def __str__(self) -> str:
        return "Identity(%s)" % self._value

    def __repr__(self) -> str:
        return str(self)
