from abc import ABCMeta, abstractmethod


class Applicative(metaclass=ABCMeta):

    @abstractmethod
    def apply(self, something) -> "Applicative":
        """(<*>) :: f (a -> b) -> f a -> f b"""

        return NotImplemented

    @classmethod
    def pure(cls, x) -> "Applicative":
        """Applicative constructor

        Use pure if you’re dealing with values in an applicative context
        (using them with <*>); otherwise, stick to the default class
        constructor."""

        return cls(x)
