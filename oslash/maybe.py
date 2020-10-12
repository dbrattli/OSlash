from abc import abstractmethod
from functools import reduce, partial

from typing import Callable, Any, Generic, TypeVar, cast

from .typing import Applicative
from .typing import Functor
from .typing import Monoid
from .typing import Monad

TSource = TypeVar("TSource")
TResult = TypeVar("TResult")


class Maybe(Generic[TSource]):
    """Encapsulates an optional value.

    The Maybe type encapsulates an optional value. A value of type
    Maybe a either contains a value of (represented as Just a), or it is
    empty (represented as Nothing). Using Maybe is a good way to deal
    with errors or exceptional cases without resorting to drastic
    measures such as error.
    """

    @classmethod
    def empty(cls) -> "Maybe[TSource]":
        return Nothing()

    @abstractmethod
    def __add__(self, other: "Maybe[TSource]") -> "Maybe[TSource]":
        raise NotImplementedError

    @abstractmethod
    def map(self, mapper: Callable[[TSource], TResult]) -> "Maybe[TResult]":
        raise NotImplementedError

    @classmethod
    def pure(cls, value: Callable[[TSource], TResult]) -> "Maybe[Callable[[TSource], TResult]]":
        raise NotImplementedError

    @abstractmethod
    def apply(self: "Maybe[Callable[[TSource], TResult]]", something: "Maybe[TSource]") -> "Maybe[TResult]":
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def unit(cls, a: TSource) -> "Maybe[TSource]":
        raise NotImplementedError

    @abstractmethod
    def bind(self, fn: Callable[[TSource], "Maybe[TResult]"]) -> "Maybe[TResult]":
        raise NotImplementedError

    @classmethod
    def concat(cls, xs):
        """mconcat :: [m] -> m

        Fold a list using the monoid. For most types, the default
        definition for mconcat will be used, but the function is
        included in the class definition so that an optimized version
        can be provided for specific types.
        """

        def reducer(a, b):
            return a + b

        return reduce(reducer, xs, cls.empty())

    def __rmod__(self, fn):
        """Infix version of map.

        Haskell: <$>

        Example:
        >>> (lambda x: x+2) % Just(40)
        42

        Returns a new Functor.
        """
        return self.map(fn)


class Just(Maybe[TSource]):
    """A Maybe that contains a value.

    Represents a Maybe that contains a value (represented as Just a).
    """

    def __init__(self, value: TSource) -> None:
        self._value = value

    # Monoid Section
    # ==============

    def __add__(self, other: Maybe[TSource]) -> Maybe[TSource]:
        # m `append` Nothing = m
        if isinstance(other, Nothing):
            return self

        # Just m1 `append` Just m2 = Just (m1 `append` m2)
        return other.map(
            lambda other_value: cast(Any, self._value) + other_value if hasattr(self._value, "__add__") else Nothing()
        )

    # Functor Section
    # ===============

    def map(self, mapper: Callable[[TSource], TResult]) -> Maybe[TResult]:
        # fmap f (Just x) = Just (f x)

        result = mapper(self._value)

        return Just(result)

    # Applicative Section
    # ===================

    @classmethod
    def pure(cls, value: Callable[[TSource], TResult]) -> "Just[Callable[[TSource], TResult]]":
        return Just(value)

    def apply(self: "Just[Callable[[TSource], TResult]]", something: Maybe[TSource]) -> Maybe[TResult]:
        def mapper(other_value):
            try:
                return self._value(other_value)
            except TypeError:
                return partial(self._value, other_value)

        return something.map(mapper)

    # Monad Section
    # =============

    @classmethod
    def unit(cls, value: TSource) -> Maybe[TSource]:
        return Just(value)

    def bind(self, func: Callable[[TSource], Maybe[TResult]]) -> Maybe[TResult]:
        """Just x >>= f = f x."""

        value = self._value
        return func(value)

    # Utilities Section
    # =================

    def is_just(self) -> bool:
        return True

    def is_nothing(self) -> bool:
        return False

    # Operator Overloads Section
    # ==========================

    def __bool__(self) -> bool:
        """Convert Just to bool."""
        return bool(self._value)

    def __eq__(self, other) -> bool:
        """Return self == other."""

        if isinstance(other, Nothing):
            return False

        return bool(other.map(lambda other_value: other_value == self._value))

    def __str__(self) -> str:
        return "Just %s" % self._value

    def __repr__(self) -> str:
        return str(self)


class Nothing(Maybe[TSource]):

    """Represents an empty Maybe.

    Represents an empty Maybe that holds nothing (in which case it has
    the value of Nothing).
    """

    # Monoid Section
    # ==============

    def __add__(self, other: Maybe) -> Maybe:
        # m `append` Nothing = m
        return other

    # Functor Section
    # ===============

    def map(self, mapper: Callable[[TSource], TResult]) -> Maybe[TResult]:
        return Nothing()

    # Applicative Section
    # ===================

    @classmethod
    def pure(cls, value: Callable[[TSource], TResult]) -> Maybe[Callable[[TSource], TResult]]:
        return Nothing()

    def apply(self: "Nothing[Callable[[TSource], TResult]]", something: Maybe[TSource]) -> Maybe[TResult]:
        return Nothing()

    # Monad Section
    # =============

    @classmethod
    def unit(cls, value: TSource) -> Maybe[TSource]:
        return cls()

    def bind(self, func: Callable[[TSource], Maybe[TResult]]) -> Maybe[TResult]:
        """Nothing >>= f = Nothing

        Nothing in, Nothing out.
        """

        return Nothing()

    # Utilities Section
    # =================

    def is_pure(self) -> bool:
        return False

    def is_nothing(self) -> bool:
        return True

    # Operator Overloads Section
    # ==========================

    def __eq__(self, other) -> bool:
        return isinstance(other, Nothing)

    def __str__(self) -> str:
        return "Nothing"

    def __repr__(self) -> str:
        return str(self)


assert issubclass(Just, Maybe)
assert issubclass(Nothing, Maybe)

assert isinstance(Maybe, Monoid)
assert isinstance(Maybe, Functor)
assert isinstance(Maybe, Applicative)
assert isinstance(Maybe, Monad)

assert isinstance(Just, Monoid)
assert isinstance(Just, Functor)
assert isinstance(Just, Applicative)
assert isinstance(Just, Monad)

assert isinstance(Nothing, Monoid)
assert isinstance(Nothing, Functor)
assert isinstance(Nothing, Applicative)
assert isinstance(Nothing, Monad)
