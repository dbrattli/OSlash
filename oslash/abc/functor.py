from abc import ABCMeta, abstractmethod

from typing import Callable, Any


class Functor(metaclass=ABCMeta):
    """The Functor class is used for types that can be mapped over. Instances
    of Functor should satisfy the following laws:

    fmap id  ==  id
    fmap (f . g)  ==  fmap f . fmap g

    The instances of Functor for lists, Maybe and IO satisfy these laws.
    """

    @abstractmethod
    def fmap(self, func: Callable[[Any], Any]) -> "Functor":
        """Map a function over wrapped values.

        fmap knows how to apply functions to values that are wrapped in
        a context.

        Keyword arguments:
        :param Functor[A] self: Functor to map
        :param Callable[[A], B] func: Mapper function
        :rtype: Functor[B]
        :return: New Functor[B]
        """

        return NotImplemented

    def __rmod__(self, other) -> "Functor":
        """Infix version of fmap. <$> in Haskell"""

        return self.fmap(other)

    @property
    def value(self: 'Functor') -> Any:
        """Get value of Functor.

        Uses fmap to extract the internal value of the Functor.

        Keyword arguments:
        :param self: Functor
        :return: :rtype: Any
        """
        value = None  # type: Any

        def mapper(x):
            nonlocal value
            value = x
        self.fmap(mapper)
        return value
