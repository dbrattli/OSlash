from abc import ABCMeta, abstractmethod
from functools import partial

from typing import Callable, Any, Generic, TypeVar

from .abc import Applicative
from .abc import Functor
from .abc import Monoid
from .abc import Monad


class Maybe(Monad, Monoid, Applicative, Functor, metaclass=ABCMeta):
    """Encapsulates an optional value.

    The Maybe type encapsulates an optional value. A value of type
    Maybe a either contains a value of (represented as Just a), or it is
    empty (represented as Nothing). Using Maybe is a good way to deal
    with errors or exceptional cases without resorting to drastic
    measures such as error.
    """

    @abstractmethod
    def bind(self, func: Callable[[Any], 'Maybe']) -> 'Maybe':
        """Monad bind method."""
        raise NotImplementedError

    @abstractmethod
    def map(self, mapper: Callable[[Any], Any]) -> 'Maybe':
        """Functor map method."""
        raise NotImplementedError

    @abstractmethod
    def apply(self, something: 'Maybe') -> 'Maybe':
        """Applicative apply method."""
        raise NotImplementedError

    @classmethod
    def empty(cls) -> 'Maybe':
        """Create empty maybe."""
        return Nothing()

    @abstractmethod
    def append(self, other: 'Maybe') -> 'Maybe':
        """Append maybe to other maybe."""
        raise NotImplementedError

    @abstractmethod
    def from_just(self) -> Any:
        raise NotImplementedError

    @property
    def is_nothing(self) -> bool:
        return False

    @property
    def is_just(self) -> bool:
        return False

    @abstractmethod
    def from_maybe(self, default: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        return False


class Just(Maybe):

    """A Maybe that contains a value.

    Represents a Maybe that contains a value (represented as Just a).
    """

    def __init__(self, value: Any) -> None:
        self._value = value

    def map(self, mapper: Callable[[Any], Any]) -> 'Just':
        # fmap f (Just x) = Just (f x)

        value = self._value
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)

        return Just(result)

    def apply(self, something: Maybe) -> Maybe:
        return something.map(self._value)

    def append(self, other: Maybe) -> Maybe:
        # m `append` Nothing = m
        if other.is_nothing:
            return self

        other_value = other.from_just()

        # Use + for append if no append
        value = self._value
        if not hasattr(other_value, "append"):
            return Just(value + other_value)

        # Just m1 `append` Just m2 = Just (m1 `append` m2)
        return Just(value.append(other_value))

    def bind(self, func: Callable[[Any], Maybe]) -> Maybe:
        """Just x >>= f = f x."""

        value = self._value
        return func(value)

    def from_just(self) -> Any:
        return self._value

    def from_maybe(self, default: Any) -> Any:
        return self._value

    def is_just(self) -> bool:
        return True

    def __bool__(self) -> bool:
        """Convert Just to bool."""
        return bool(self._value)

    def __eq__(self, other) -> bool:
        """Return self == other."""
        if other.is_nothing:
            return False

        return self._value == other.from_just()

    def __str__(self) -> str:
        return "Just %s" % self._value


class Nothing(Maybe):

    """Represents an empty Maybe.

    Represents an empty Maybe that holds nothing (in which case it has
    the value of Nothing).
    """

    def map(self, mapper: Callable[[Any], Any]) -> Maybe:
        return Nothing()

    def apply(self, other: Maybe) -> Maybe:
        return Nothing()

    def append(self, other: Maybe) -> Maybe:
        return other

    def bind(self, func: Callable[[Any], Maybe]) -> Maybe:
        """Nothing >>= f = Nothing

        Nothing in, Nothing out.
        """

        return Nothing()

    def from_just(self) -> Any:
        raise Exception("Nothing")

    def from_maybe(self, default: Any) -> Any:
        return default

    def is_nothing(self) -> bool:
        return True

    def __eq__(self, other) -> bool:
        return isinstance(other, Nothing)

    def __str__(self) -> str:
        return "Nothing"
