"""Behavioral tests for error-accumulating validation."""

from collections.abc import Callable

import pytest

from oslash import Applicative, Either, Left, List, Right, Validation


def test_validation_pure_and_map() -> None:
    assert Validation.pure(2).map(lambda value: value * 3) == Validation.valid(6)
    invalid: Validation[int, str] = Validation.invalid("bad")
    assert invalid.map(lambda value: value * 3) == invalid
    assert isinstance(Validation, Applicative)


def test_validation_apply_two_successes() -> None:
    function: Validation[Callable[[int], int], str] = Validation.valid(lambda value: value + 1)
    assert function.apply(Validation.valid(2)) == Validation.valid(3)


def test_validation_apply_curries_two_successes() -> None:
    combine: Callable[[int, int], int] = lambda first, second: first + second
    function: Validation[Callable[[int, int], int], str] = Validation.pure(combine)
    assert function.apply(Validation.valid(2)).apply(Validation.valid(3)) == Validation.valid(5)


def test_validation_apply_one_failure() -> None:
    function: Validation[Callable[[int], int], str] = Validation.valid(lambda value: value + 1)
    bad_function: Validation[Callable[[int], int], str] = Validation.invalid("function")
    assert function.apply(Validation.invalid("value")) == Validation.invalid("value")
    assert bad_function.apply(Validation.valid(2)) == Validation.invalid("function")


def test_validation_apply_collects_errors_in_argument_order() -> None:
    combine: Callable[[int, int], int] = lambda first, second: first + second
    function: Validation[Callable[[int, int], int], str] = Validation.pure(combine)
    result = function.apply(Validation.invalid("first")).apply(Validation.invalid("second"))
    assert result.to_either() == Left(List(["first", "second"]))


def test_validation_apply_preserves_three_errors() -> None:
    function: Validation[Callable[[int, int], int], str] = Validation.invalid("function")
    result = function.apply(Validation.invalid("first")).apply(Validation.invalid("second"))
    assert result.to_either() == Left(List(["function", "first", "second"]))


def test_validation_lifts_either_and_exposes_all_errors() -> None:
    good: Either[int, str] = Right(2)
    bad: Either[int, str] = Left("bad")
    assert Validation.from_either(good).to_either() == Right(2)
    assert Validation.from_either(bad).to_either() == Left(List.unit("bad"))


def test_validation_rejects_empty_error_list() -> None:
    with pytest.raises(ValueError, match="at least one error"):
        Validation[int, str](Left(List.empty()))
