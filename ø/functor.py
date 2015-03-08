from abc import ABCMeta, abstractmethod


class IFunctor(metaclass=ABCMeta):

    @abstractmethod
    def fmap(self, _) -> "IFunctor":
        return NotImplemented
