from abc import ABCMeta, abstractmethod


class Monad(metaclass=ABCMeta):
    @abstractmethod
    def bind(self, func) -> "Monad":
        """(>>=) :: m a -> (a -> m b) -> m b"""
        return NotImplemented

    @classmethod
    def return_(cls, x) -> "Applicative":
        return cls(x)