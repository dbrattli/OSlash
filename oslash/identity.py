from functools import partial

from oslash.abc import Functor
from oslash.abc import Monad
from oslash.abc import Applicative


class Identity(Monad, Applicative, Functor):

    """The Identity monad.

    The Identity monad is the simplest monad, which attaches no
    information to values..
    """

    def __init__(self, value: "Any"):
        """Initialize a new reader."""
        self._get_value = lambda: value

    def fmap(self, mapper: "Callable[[Any], Any]") -> "Identity":
        """Map a function over wrapped values."""
        value = self._get_value()
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Identity(result)

    def bind(self, func: "Callable[[Any], Identity]") -> "Monad":
        return func(self._get_value())

    def apply(self, something: "Identity") -> "Identity":
        func = self._get_value()
        x = something.fmap(func)
        return x

    def run_identity(self) -> "Any":
        return self._get_value()

    def __call__(self) -> "Any":
        return self.run_identity()

    def __eq__(self, other):
        value = self._get_value()
        return value == other.value

    def __str__(self):
        return "Identity(%s)" % self._get_value()

    def __repr__(self):
        return str(self)
