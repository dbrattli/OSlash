from abc import ABCMeta, abstractmethod


class IApplicative(metaclass=ABCMeta):

    @abstractmethod
    def apply(self, something) -> "IApplicative":
        """(<*>) :: f (a -> b) -> f a -> f b"""
        return NotImplemented

    @classmethod
    def pure(cls, x) -> "IApplicative":
        return cls(x)
