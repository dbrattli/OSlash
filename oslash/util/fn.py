"""Function composition utilities."""

from __future__ import annotations

from collections.abc import Callable
from functools import reduce
from typing import Any, overload


@overload
def compose[A]() -> Callable[[A], A]: ...


@overload
def compose[A, B](op1: Callable[[A], B], /) -> Callable[[A], B]: ...


@overload
def compose[A, B, C](op2: Callable[[B], C], op1: Callable[[A], B], /) -> Callable[[A], C]: ...


@overload
def compose[A, B, C, D](op3: Callable[[C], D], op2: Callable[[B], C], op1: Callable[[A], B], /) -> Callable[[A], D]: ...


@overload
def compose[A, B, C, D, E](
    op4: Callable[[D], E], op3: Callable[[C], D], op2: Callable[[B], C], op1: Callable[[A], B], /
) -> Callable[[A], E]: ...


@overload
def compose[A, B, C, D, E, F](
    op5: Callable[[E], F], op4: Callable[[D], E], op3: Callable[[C], D], op2: Callable[[B], C], op1: Callable[[A], B], /
) -> Callable[[A], F]: ...


@overload
def compose[A, B, C, D, E, F, G](
    op6: Callable[[F], G],
    op5: Callable[[E], F],
    op4: Callable[[D], E],
    op3: Callable[[C], D],
    op2: Callable[[B], C],
    op1: Callable[[A], B],
    /,
) -> Callable[[A], G]: ...


def compose[T](*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose multiple functions right to left.

    Composes zero or more functions into a functional composition. The
    functions are composed right to left. A composition of zero
    functions gives back the identity function.

    compose()(x) == x
    compose(f)(x) == f(x)
    compose(g, f)(x) == g(f(x))
    compose(h, g, f)(x) == h(g(f(x)))
    ...

    Returns the composed function.
    """

    def _compose(source: T) -> T:
        return reduce(lambda acc, f: f(acc), funcs[::-1], source)  # type: ignore

    return _compose


# Force partial application for fmap
def fmap[A, B, C](f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    """Map a function over a function (function composition)."""
    return compose(f, g)


# Identity function
def identity[T](x: T) -> T:
    """Return the argument unchanged."""
    return x
