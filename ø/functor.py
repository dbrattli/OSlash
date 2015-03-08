from abc import ABCMeta, abstractmethod


class Functor(metaclass=ABCMeta):

    @abstractmethod
    def fmap(self, _) -> "IFunctor":
        return NotImplemented
