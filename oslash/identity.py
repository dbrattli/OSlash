from functools import partial  # type: ignore

from typing import Any, Callable

from .abc import Functor
from .abc import Monad
from .abc import Applicative


class Identity(Monad, Applicative, Functor):

    """The Identity monad.

    The Identity monad is the simplest monad, which attaches no
    information to values.
    """

    def __init__(self, value: "Any"):
        """Initialize a new reader."""
        self._get_value = lambda: value

    def map(self, mapper: Callable[[Any], Any]) -> "Identity":
        """Map a function over wrapped values."""
        value = self._get_value()
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Identity(result)

    def bind(self, func: Callable[[Any], "Identity"]) -> "Identity":
        return func(self._get_value())

    def apply(self, something: "Identity") -> "Identity":
        func = self._get_value()
        return something.map(func)

    def run(self) -> Any:
        return self._get_value()

    def __call__(self) -> Any:
        return self.run()

    def __eq__(self, other: "Identity") -> bool:
        value = self._get_value()
        return value == other.value

    def __str__(self) -> str:
        return "Identity(%s)" % self._get_value()

    def __repr__(self) -> str:
        return str(self)
