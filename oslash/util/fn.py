from functools import reduce

from typing import Tuple, Callable, Any, TypeVar, overload  # noqa

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")
F = TypeVar("F")
G = TypeVar("G")


@overload
def compose() -> Callable[[A], A]:  # pylint: disable=function-redefined
    ...  # pylint: disable=pointless-statement


@overload
def compose(op1: Callable[[A], B]) -> Callable[[A], B]:  # pylint: disable=function-redefined
    ...  # pylint: disable=pointless-statement


@overload
def compose(op2: Callable[[B], C], op1: Callable[[A], B]) -> Callable[[A], C]:  # pylint: disable=function-redefined
    ...  # pylint: disable=pointless-statement


@overload
def compose(
    op3: Callable[[C], D], op2: Callable[[B], C], op1: Callable[[A], B]  # pylint: disable=function-redefined
) -> Callable[[A], D]:
    ...  # pylint: disable=pointless-statement


@overload
def compose(
    op4: Callable[[D], E],  # pylint: disable=function-redefined
    op3: Callable[[C], D],
    op2: Callable[[B], C],
    op1: Callable[[A], B],
) -> Callable[[A], E]:
    ...  # pylint: disable=pointless-statement


@overload
def compose(
    op5: Callable[[E], F],  # pylint: disable=function-redefined
    op4: Callable[[D], E],
    op3: Callable[[C], D],
    op2: Callable[[B], C],
    op1: Callable[[A], B],
) -> Callable[[A], F]:
    ...  # pylint: disable=pointless-statement


@overload
def compose(
    op1: Callable[[A], B],  # pylint: disable=function-redefined,too-many-arguments
    op2: Callable[[B], C],
    op3: Callable[[C], D],
    op4: Callable[[D], E],
    op5: Callable[[E], F],
    op6: Callable[[F], G],
) -> Callable[[A], G]:
    ...  # pylint: disable=pointless-statement


def compose(*funcs: Callable) -> Callable:  # type: ignore
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

    def _compose(source: Any) -> Any:
        return reduce(lambda acc, f: f(acc), funcs[::-1], source)

    return _compose


fmap = lambda f, g: compose(f, g)  # To force partial application

identity = compose()  # type: Callable
