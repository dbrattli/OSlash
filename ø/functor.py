from abc import ABCMeta, abstractmethod


class Functor(metaclass=ABCMeta):

    @abstractmethod
    def fmap(self, _) -> "Functor":
        return NotImplemented
