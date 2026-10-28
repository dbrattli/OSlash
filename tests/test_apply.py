"""Regression tests for applicative application across contexts."""

from oslash import Identity, Just, List, Reader, Right


def test_apply_curries_builtin_without_signature() -> None:
    assert Identity(getattr).apply(Identity(str)).apply(Identity("__name__")) == Identity("str")
    assert Just(getattr).apply(Just(str)).apply(Just("__name__")) == Just("str")
    assert Right(getattr).apply(Right(str)).apply(Right("__name__")) == Right("str")
    assert List.unit(getattr).apply(List.unit(str)).apply(List.unit("__name__")) == List.unit("str")
    assert Reader.pure(getattr).apply(Reader.pure(str)).apply(Reader.pure("__name__")).run(None) == "str"
