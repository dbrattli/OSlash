"""Caller-side type checks for public structural protocols.

Pyright checks this file, while pytest does not collect it as a runtime test.
"""

# pyright: reportUnnecessaryTypeIgnoreComment=true

from collections.abc import Callable
from typing import assert_type

from oslash import (
    Either,
    Identity,
    Just,
    List,
    Maybe,
    Reader,
    Right,
    StringWriter,
    Validation,
    Writer,
    guard,
    monadic_compose,
    or_else,
)
from oslash.typing import Applicative, Functor, Monad


def check_functor_and_monad() -> None:
    identity_functor: Functor[int, str, Identity[str]] = Identity(1)
    maybe_functor: Functor[int, str, Maybe[str]] = Just(1)
    writer_functor: Functor[int, str, Writer[str, str]] = Writer(1, "")
    assert_type(identity_functor.map(str), Identity[str])
    assert_type(maybe_functor.map(str), Maybe[str])
    assert_type(writer_functor.map(str), Writer[str, str])

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

    validation_fn: Validation[Callable[[int], str], str] = Validation[Callable[[int], str], str].valid(fn)
    validation: Applicative[Callable[[int], str], Validation[int, str], Validation[str, str]] = validation_fn
    assert_type(validation.apply(Validation[int, str].valid(1)), Validation[str, str])

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

    validation_fn: Validation[Callable[[int, int], int], str] = Validation[Callable[[int, int], int], str].valid(fn)
    assert_type(
        validation_fn.apply(Validation[int, str].valid(1)).apply(Validation[int, str].valid(2)), Validation[int, str]
    )

    reader_fn: Reader[str, Callable[[int, int], int]] = Reader(lambda _: fn)
    assert_type(
        reader_fn.apply(Reader[str, int].unit(1)).apply(Reader[str, int].unit(2)),
        Reader[str, int],
    )

    list_fn: List[Callable[[int, int], int]] = List[Callable[[int, int], int]].from_iterable([fn])
    assert_type(list_fn.apply(List[int].from_iterable([1])).apply(List[int].from_iterable([2])), List[int])


def check_validation_conversions_and_fallback() -> None:
    result: Either[int, str] = Right(1)
    assert_type(or_else(result, Right(2)), Either[int, str])
    assert_type(Validation.from_either(result), Validation[int, str])
    assert_type(Validation.from_either(result).to_either(), Either[int, List[str]])


def check_writer_factories() -> None:
    assert_type(StringWriter.unit(1), Writer[int, str])
    assert_type(StringWriter.unit(True), Writer[bool, str])
    assert_type(StringWriter(1, "log"), Writer[int, str])
    default_writer = Writer.create("DefaultWriter")
    assert_type(default_writer.unit(1), Writer[int, str])
    int_writer = Writer.create("IntWriter", int)
    assert_type(int_writer.unit(1), Writer[int, int])
    list_writer = Writer.create("ListWriter", list[str])
    assert_type(list_writer.unit(1), Writer[int, list[str]])
    assert_type(list_writer("value", ["log"]), Writer[str, list[str]])
    assert_type(list_writer.unit(1).map(str), Writer[str, list[str]])
    assert_type(list_writer.unit(1).bind(lambda value: list_writer(str(value), [])), Writer[str, list[str]])


def map_to_string[Result](functor: Functor[int, str, Result]) -> Result:
    return functor.map(str)


def check_functor_consumers() -> None:
    assert_type(map_to_string(Identity(1)), Identity[str])
    assert_type(map_to_string(Just(1)), Maybe[str])
    assert_type(map_to_string(Writer(1, "log")), Writer[str, str])
    assert_type(map_to_string(List[int].from_iterable([1])), List[str])
    reader = Reader[str, int](len)
    assert_type(map_to_string(reader), Reader[str, str])
    either: Either[int, str] = Right(1)
    assert_type(map_to_string(either), Either[str, str])
    validation = Validation[int, str].valid(1)
    assert_type(map_to_string(validation), Validation[str, str])


def check_rejected_writer_factory_calls() -> None:
    # These ignores must remain necessary: factory log types are fixed, and
    # only the base Writer.unit accepts an explicit log identity.
    empty: list[str] = []
    StringWriter.unit(1, empty_log=empty)  # pyright: ignore[reportCallIssue]
    StringWriter(1, empty)  # pyright: ignore[reportArgumentType]
    int_writer = Writer.create("IntWriter", int)
    int_writer(1, "wrong log")  # pyright: ignore[reportArgumentType]
    int_writer.unit(1, empty_log=0)  # pyright: ignore[reportCallIssue]
