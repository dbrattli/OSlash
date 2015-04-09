from abc import ABCMeta, abstractmethod

from typing import Callable, Any


class Functor(metaclass=ABCMeta):
    """The Functor class is used for types that can be mapped over.
    Instances of Functor should satisfy the following laws:

    fmap id  ==  id
    fmap (f . g)  ==  fmap f . fmap g

    The instances of Functor for lists, Maybe and IO satisfy these laws.
    """

    @abstractmethod
    def map(self, func: Callable[[Any], Any]) -> "Functor":
        """Map a function over wrapped values.

        fmap knows how to apply functions to values that are wrapped in
        a context.
        """

        return NotImplemented

    def __rmod__(self, other) -> "Functor":
        """Infix version of fmap. <$> in Haskell"""

        return self.map(other)

    @property
    def value(self) -> Any:
        """Get value of Functor.

        Uses fmap to extract the internal value of the Functor.
        """
        value = None  # type: Any

        def mapper(x):
            nonlocal value
            value = x
        self.map(mapper)
        return value
