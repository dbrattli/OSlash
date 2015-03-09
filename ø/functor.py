from abc import ABCMeta, abstractmethod


class Functor(metaclass=ABCMeta):

    @abstractmethod
    def fmap(self, func) -> "Functor":
        """
        :param Functor[A] self: Functor to map
        :param Callable[[A], B] func: Mapper function
        :rtype: Functor[B]
        :returns: New Functor[B]
        """

        return NotImplemented
