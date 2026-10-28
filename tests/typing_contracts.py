"""Caller-side type checks for public structural protocols.

Pyright checks this file, while pytest does not collect it as a runtime test.
"""

from collections.abc import Callable
from typing import assert_type

from oslash import Either, Identity, Just, List, Maybe, Reader, Right, Writer, guard, monadic_compose
from oslash.typing import Applicative, Functor, Monad


def check_functor_and_monad() -> None:
    identity_functor: Functor[int] = Identity(1)
    maybe_functor: Functor[int] = Just(1)
    writer_functor: Functor[int] = Writer(1, "")
    identity_functor.map(lambda value: value + 1)
    maybe_functor.map(lambda value: value + 1)
    writer_functor.map(lambda value: value + 1)

    identity_monad: Monad[int, Identity[str]] = Identity(1)
    maybe_monad: Monad[int, Maybe[str]] = Just(1)
    writer_monad: Monad[int, Writer[str, str]] = Writer(1, "")

    assert_type(identity_monad.bind(lambda value: Identity(str(value))), Identity[str])
    assert_type(maybe_monad.bind(lambda value: Just(str(value))), Maybe[str])
    assert_type(writer_monad.bind(lambda value: Writer(str(value), "")), Writer[str, str])


def check_applicative() -> None:
    fn: Callable[[int], str] = str

    identity_fn: Identity[Callable[[int], str]] = Identity(fn)
    identity: Applicative[Callable[[int], str], Identity[int], Identity[str]] = identity_fn
    assert_type(identity.apply(Identity(1)), Identity[str])

    maybe_fn: Just[Callable[[int], str]] = Just(fn)
    maybe: Applicative[Callable[[int], str], Maybe[int], Maybe[str]] = maybe_fn
    assert_type(maybe.apply(Just(1)), Maybe[str])

    either_fn: Right[Callable[[int], str], str] = Right(fn)
    either: Applicative[Callable[[int], str], Either[int, str], Either[str, str]] = either_fn
    assert_type(either.apply(Right(1)), Either[str, str])

    reader_fn: Reader[str, Callable[[int], str]] = Reader(lambda _: fn)
    reader: Applicative[Callable[[int], str], Reader[str, int], Reader[str, str]] = reader_fn
    assert_type(reader.apply(Reader[str, int].unit(1)), Reader[str, str])

    list_fn: List[Callable[[int], str]] = List[Callable[[int], str]].from_iterable([fn])
    list_applicative: Applicative[Callable[[int], str], List[int], List[str]] = list_fn
    assert_type(list_applicative.apply(List[int].from_iterable([1])), List[str])


def check_writer_unit() -> None:
    empty_log: list[str] = []
    assert_type(Writer.unit(1), Writer[int, str])
    assert_type(Writer[int, list[str]].unit(1), Writer[int, str])
    assert_type(Writer[int, list[str]].unit(1, empty_log=empty_log), Writer[int, list[str]])


def check_monadic_compose() -> None:
    def first(value: int) -> Identity[int]:
        return Identity(value + 1)

    def second(value: int) -> Identity[str]:
        return Identity(str(value))

    assert_type(monadic_compose(second, first)(1), Identity[str])


def check_guard() -> None:
    assert_type(guard(List, True), List[tuple[()]])
    assert_type(guard(Just, False), Maybe[tuple[()]])


def check_curried_apply() -> None:
    fn: Callable[[int, int], int] = lambda left, right: left + right

    identity_fn: Identity[Callable[[int, int], int]] = Identity(fn)
    assert_type(identity_fn.apply(Identity(1)).apply(Identity(2)), Identity[int])

    maybe_fn: Just[Callable[[int, int], int]] = Just(fn)
    assert_type(maybe_fn.apply(Just(1)).apply(Just(2)), Maybe[int])

    either_fn: Right[Callable[[int, int], int], str] = Right(fn)
    assert_type(either_fn.apply(Right(1)).apply(Right(2)), Either[int, str])

    reader_fn: Reader[str, Callable[[int, int], int]] = Reader(lambda _: fn)
    assert_type(
        reader_fn.apply(Reader[str, int].unit(1)).apply(Reader[str, int].unit(2)),
        Reader[str, int],
    )

    list_fn: List[Callable[[int, int], int]] = List[Callable[[int, int], int]].from_iterable([fn])
    assert_type(list_fn.apply(List[int].from_iterable([1])).apply(List[int].from_iterable([2])), List[int])
