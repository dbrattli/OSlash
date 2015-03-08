from abc import ABCMeta, abstractmethod
from functools import partial
from typing import Any

from .applicative import Applicative
from .functor import Functor
from .monad import Monad


class Either(Applicative, Functor, metaclass=ABCMeta):

    @abstractmethod
    def apply(self, something) -> "Applicative":
        return NotImplemented

    @abstractmethod
    def fmap(self, _) -> "Either":
        return NotImplemented

    @property
    def value(self: 'Just') -> Any:
        """Uses fmap to gets internal value of Either object
        :param self: Left|Right
        :return: :rtype: Any
        """

        value = None

        def mapper(x):
            nonlocal value
            value = x
        self.fmap(mapper)
        return value

    @abstractmethod
    def __eq__(self, other) -> bool:
        return NotImplemented


class Right(Either):
    def apply(self, something) -> Either:
        return something.fmap(self._get_value())

    def __init__(self, value: Any):
        self._get_value = lambda: value

    def fmap(self, mapper) -> Either:
        return Right(mapper(self._get_value()))

    def __eq__(self, other) -> bool:
        return self._get_value() == other.value

    def __str__(self) -> str:
        return "Right %s" % self._get_value()

class Left(Either):
    def apply(self, something) -> Either:
        return something.fmap(self._get_value())

    def __init__(self, value: Any):
        self._get_value = lambda: value

    def fmap(self, mapper) -> Either:
        mapper(self._get_value()) # TODO: fixme
        return Left(self._get_value())

    def __eq__(self, other) -> bool:
        return self._get_value() == other.value

    def __str__(self) -> str:
        return "Left %s" % self._get_value()
