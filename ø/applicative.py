from abc import ABCMeta, abstractmethod


class Applicative(metaclass=ABCMeta):

    @abstractmethod
    def apply(self, something) -> "Applicative":
        """(<*>) :: f (a -> b) -> f a -> f b"""

        return NotImplemented

    @classmethod
    def pure(cls, x) -> "Applicative":
        return cls(x)
