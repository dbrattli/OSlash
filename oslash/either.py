from abc import ABCMeta, abstractmethod
from functools import partial
from typing import Any

from .applicative import Applicative
from .functor import Functor
from .monad import Monad


class Either(Monad, Applicative, Functor, metaclass=ABCMeta):

    @abstractmethod
    def fmap(self, _) -> "Either":
        return NotImplemented

    @abstractmethod
    def apply(self, something) -> "Either":
        return NotImplemented

    @abstractmethod
    def bind(self, func) -> "Either":
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
    def __init__(self, value: Any):
        self._get_value = lambda: value

    def fmap(self, mapper) -> Either:
        value = self._get_value()
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Right(result)

    def apply(self, something) -> Either:
        return something.fmap(self._get_value())

    def bind(self, func) -> Either:
        return func(self._get_value())

    def __eq__(self, other) -> bool:
        return isinstance(other, Right) and self._get_value() == other.value

    def __str__(self) -> str:
        return "Right %s" % self._get_value()


class Left(Either):
    def apply(self, something) -> Either:
        return Left(self._get_value())

    def __init__(self, value: Any):
        self._get_value = lambda: value

    def fmap(self, mapper) -> Either:
        try:
            mapper(self._get_value())  # TODO: fixme
        except TypeError:
            pass
        return Left(self._get_value())

    def bind(self, func) -> "Either":
        return Left(self._get_value())

    def __eq__(self, other) -> bool:
        return isinstance(other, Left) and self._get_value() == other.value

    def __str__(self) -> str:
        return "Left %s" % self._get_value()
