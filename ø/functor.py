from abc import ABCMeta, abstractmethod


class Functor(metaclass=ABCMeta):
    """The Functor class is used for types that can be mapped over. Instances
    of Functor should satisfy the following laws:

    fmap id  ==  id
    fmap (f . g)  ==  fmap f . fmap g

    The instances of Functor for lists, Maybe and IO satisfy these laws.
    """

    @abstractmethod
    def fmap(self, func) -> "Functor":
        """fmap knows how to apply functions to values that are wrapped in a
        context.

        Keyword arguments:
        :param Functor[A] self: Functor to map
        :param Callable[[A], B] func: Mapper function
        :rtype: Functor[B]
        :returns: New Functor[B]
        """

        return NotImplemented

    def __rmod__(self, other):
        """Infix version of fmap. <$> in Haskell"""

        return self.fmap(other)
